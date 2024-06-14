# cython: language_level=3
# cython: nonecheck=False
# cython: cdivision=True
# cython: boundscheck=False
# cython: wraparound=False
from src.data_loader import get_data
from multiprocessing import Pool
from os import path
from pathlib import Path
from src.strategies import ta_indicators
from src.backtests.advanced_backtest.advanced_backtest import advanced_backtest
from inspect import getmembers, isfunction
from pandas import DataFrame, concat, read_feather
from glob import glob
import numpy as np
cimport numpy as np
np.import_array()


cpdef object serial_based_backtest(str interval, list strategy_list, str start_date, str end_date, object base_results_df, int years, bint reduce_outliners, bint reset_index = True):
        cdef str symbol = "BTCUSDT"
        cdef list backtest_id_list, args_id_list, backtest_args_list, strategy_args_list, candles_list, strategy_settings_list, backtest_list
        cdef str strategy_name
        cdef object strategy_results_df, backtest_df, backtest_data, df
        # cdef object main_df = DataFrame()
        # base_results_df = base_results_df.sort_values("profit", ascending=False).reset_index(drop=True)
        backtest_data = get_data(symbol, interval, start_date, end_date)
        for strategy_name in strategy_list:
            strategy_results_df = base_results_df[base_results_df["strategy_name"] == strategy_name]
            if len(strategy_results_df):
                df = backtest_data.copy()
                backtest_id_list = strategy_results_df.index.tolist()
                args_id_list = strategy_results_df.loc[:, "args_id"].values.tolist()
                # backtest_profit_list = strategy_results_df.iloc[:, 0].values.tolist()
                backtest_args_list = strategy_results_df.iloc[:, 17:22].values.tolist()
                strategy_args_list = strategy_results_df.iloc[:, 25:].dropna(axis=1).values.tolist()
                candles_list = parallel_candles(strategy_name, df, strategy_args_list)
                strategy_settings_list = [[symbol, interval, strategy_name, *strategy_args] for strategy_args in strategy_args_list]
                
                backtest_list = multiprocessing_selected_backtest(backtest_id_list, args_id_list, backtest_args_list, candles_list, strategy_settings_list, years, reduce_outliners)

                backtest_df = save_results(start_date, end_date, symbol, backtest_list, interval, strategy_name)
                # main_df = concat([main_df, backtest_df])
        # main_df = main_df.sort_values("backtest_id", ascending=True).reset_index(drop=True)
        # if reset_index is False:
        #     main_df.index = main_df.loc[:, "backtest_id"].values
        # main_df = main_df.iloc[:, 1:]
        # return main_df


def save_results(start_date: str, end_date: str, symbol: str, backtest_list: list, interval: str, strategy_name: str):
    backtest_df = DataFrame(backtest_list)
    args_count = len(backtest_df.columns) - 26
    # args_count = len(backtest_df.columns) - 21
    args_name_list = [f"arg_{i}" for i in range(1, args_count+1)]
    backtest_df.columns = ["backtest_id", "args_id", "profit", "drawdown", "profit_to_drawdown", "trade count", "win rate", "average trade", "average win", "average loss", "max win", "max loss", "sharpe ratio", "sortino ratio", "cagr", "rar", "mar ratio", "mmar ratio", "stop_loss_type", "stop_loss_value", "take_profit_type", "take_profit_value", "fees", "symbol", "interval", "strategy_name", *args_name_list]
    # return backtest_df
    file_name = f"{strategy_name}.feather"
    file_path = path.dirname(__file__)
    src_path = path.dirname(path.dirname(file_path))
    dir_name = f"{src_path}/data_loader/results/{symbol}/{interval}_{start_date}_{end_date}_based/{strategy_name}"
    output_dir = Path(dir_name)
    output_dir.mkdir(parents=True, exist_ok=True)
    backtest_df.to_feather(f"{dir_name}/{file_name}")



cdef list parallel_candles(str strategy_name, object df, list strategy_args_list):
    cdef dict strategy_dict = dict(getmembers(ta_indicators, isfunction))
    cdef object selected_strategy = strategy_dict[strategy_name]
    cdef list args_list = [[selected_strategy, strategy_args, df] for strategy_args in strategy_args_list]
    with Pool() as pool:
        return pool.map(strategy_processing, args_list)


cpdef np.ndarray[double, ndim=2] strategy_processing(list settings_list):
    cdef object selected_strategy = settings_list[0]
    cdef list strategy_args = settings_list[1]
    cdef object strategy_df = settings_list[2]
    return strategy_select(selected_strategy, strategy_args, strategy_df)


cdef np.ndarray[double, ndim=2] strategy_select(object selected_strategy, list strategy_args, object data):
    cdef object main_df = data.copy()
    cdef object strategy_df = selected_strategy(main_df, *strategy_args)
    main_df = concat([main_df, strategy_df], axis=1)
    cdef np.ndarray strategy_array = main_df.loc[main_df.index[1]:,
                     ['open', 'high', 'low', 'go_long', 'go_short', 'exit_long', 'exit_short']].values
    return strategy_array


cdef list multiprocessing_selected_backtest(list backtest_id_list, list args_id_list, list backtest_args_list, list candles_list, list strategy_settings_list, int years, bint reduce_outliners):
    cdef list args_list = [[backtest_id_list[i], args_id_list[i], candles_np_array, strategy_settings_list[i], backtest_args_list[i], years, reduce_outliners] for i, candles_np_array in enumerate(candles_list)]
    with Pool() as pool:
        return pool.map(processing_advanced_backtest, args_list)


cpdef list processing_advanced_backtest(list backtest_set):
    cdef int backtest_id = backtest_set[0]
    cdef int args_id = backtest_set[1]
    cdef np.ndarray[double, ndim=2] strategy_data = backtest_set[2]
    cdef list strategy_settings = backtest_set[3]
    cdef list backtest_args = backtest_set[4]
    cdef int years = backtest_set[5]
    cdef bint reduce_outliners = backtest_set[6]
    cdef list summary = advanced_backtest(strategy_data, backtest_args, True, years, reduce_outliners)
    return [backtest_id, args_id, *summary, *backtest_args, *strategy_settings]
