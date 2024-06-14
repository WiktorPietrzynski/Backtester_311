# cython: language_level=3
# cython: nonecheck=False
# cython: cdivision=True
# cython: boundscheck=False
# cython: wraparound=False
from src.data_loader import get_data
from multiprocessing import Pool
from os import path
from pathlib import Path
from src.serial_backtests.utils import display_progress
from src.serial_backtests.utils.generators import get_strategy_args
from src.serial_backtests.utils.generators import get_basic_backtest_args
from src.backtests.advanced_backtest.advanced_backtest import advanced_backtest
from src.strategies import ta_indicators
from inspect import getmembers, isfunction
from pandas import DataFrame, concat
import numpy as np
cimport numpy as np
np.import_array()


cpdef void serial_advanced_backtest(list interval_list, list strategy_list, str start_date = "2017-09-01", str end_date = "2025-01-01", int years = 6, bint reduce_strategies = False, bint reduce_backtests=False):
    cdef str symbol = "BTCUSDT"
    cdef str interval, strategy_name
    cdef object df
    for interval in interval_list:
        df = get_data(symbol, interval, start_date, end_date)
        for strategy_name in strategy_list:
            df = df.copy()
            strategy_name = strategy_name.replace(" ", "_")
            strategy_backtest(symbol, interval, df, strategy_name, start_date, end_date, years, reduce_strategies, reduce_backtests)

cdef void strategy_backtest(str symbol, str interval, object df, str strategy_name, str start_date, str end_date, int years, bint reduce_strategies, bint reduce_backtests):
    cdef int strategy_part_count = 100
    cdef list backtest_args_list = list(get_basic_backtest_args(reduce_backtests))
    cdef list strategy_args_list = list(get_strategy_args(strategy_name, reduce_strategies))
    cdef list args_list = []
    cdef int i, x
    cdef int j = 0
    cdef int index_part = 1
    cdef list strategy_args_list_part, candles_list, backtest_args, backtest_list, args_id_list
    cdef int parts_count = int(len(strategy_args_list)/strategy_part_count)+1
    display_progress(strategy_name, parts_count, 0)
    for i in range(0, len(strategy_args_list), strategy_part_count):
        strategy_args_list_part = strategy_args_list[i: i + strategy_part_count]
        candles_list = parallel_candles(strategy_name, df, strategy_args_list_part)
        for x in range(len(strategy_args_list_part)):
            for backtest_args in backtest_args_list:
                args_list.append([j, backtest_args, candles_list[x], symbol, interval, strategy_name, strategy_args_list_part[x], years])
                j += 1
        backtest_list = multiprocessing_advanced_backtest(args_list)
        args_list = []
        if len(backtest_list) > 0:
            save_backtest(backtest_list, index_part, symbol, interval, strategy_name, strategy_part_count, start_date, end_date)
        display_progress(strategy_name, parts_count, index_part)
        index_part += 1
    print(f"Saved {symbol} - {interval} - {strategy_name}")

cdef list multiprocessing_advanced_backtest(list args_list):
    # cdef list args_list = [[candles_np_array, strategy_settings_list[i], backtest_args, years, reduce_outliners] for i, candles_np_array in enumerate(candles_list) for backtest_args in backtest_args_list]
    with Pool() as pool:
        return pool.map(processing_advanced_backtest, args_list)

cpdef list processing_advanced_backtest(backtest_set):
    cdef int args_id = backtest_set[0]
    cdef list backtest_args = backtest_set[1]
    cdef np.ndarray[double, ndim=2] candles = backtest_set[2]
    cdef str symbol = backtest_set[3]
    cdef str interval = backtest_set[4]
    cdef str strategy_name = backtest_set[5]
    cdef list strategy_args = backtest_set[6]
    cdef int years = backtest_set[7]
    cdef bint reduce_outliners = backtest_set[8]
    cdef list summary = advanced_backtest(candles, backtest_args, True, years, reduce_outliners)
    return [args_id, *summary, *backtest_args, symbol, interval, strategy_name, *strategy_args]


cdef void save_backtest(list backtest_list, int index, str symbol, str interval, str strategy_name, int strategy_part_count, str start_date, str end_date):
    cdef object backtest_df = DataFrame(backtest_list).sort_values(1, ascending=False)
    cdef int args_count = len(backtest_df.columns) - 25
    cdef list args_name_list = [f"arg_{i}" for i in range(1, args_count+1)]
    cdef str file_name, dir_name
    cdef object output_dir
    cdef int df_len
    backtest_df.columns = ["args_id", "profit", "drawdown", "profit_to_drawdown", "trade count", "win rate", "average trade", "average win", "average loss", "max win", "max loss", "sharpe ratio", "sortino ratio", "cagr", "rar", "mar ratio", "mmar ratio", "stop_loss_type", "stop_loss_value", "take_profit_type", "take_profit_value", "fees", "symbol", "interval", "strategy_name", *args_name_list]
    backtest_df = backtest_df[backtest_df["drawdown"] < 50.0]
    # backtest_df = backtest_df[backtest_df["profit"] > 0]
    if backtest_df.empty is False:
        backtest_df = backtest_df.sort_values("profit", ascending=False).reset_index(drop=True).round(2)
        file_name = f"{strategy_name}_{index}.feather"
        file_path = path.dirname(__file__)
        src_path = path.dirname(path.dirname(file_path))
        dir_name = f"{src_path}/data_loader/results/{symbol}/{interval}_{start_date}_{end_date}/{strategy_name}"
        output_dir = Path(dir_name)
        output_dir.mkdir(parents=True, exist_ok=True)
        backtest_df.to_feather(f"{dir_name}/{file_name}")

    # for tests
    # file_name = f"{strategy_name}_{index}.csv"
    # dir_name = str(Path.home() / f"Desktop/data/results/{test_name}/{interval}/{symbol}/{strategy_name}")
    # output_dir = Path(dir_name)
    # output_dir.mkdir(parents=True, exist_ok=True)
    # backtest_df.to_csv(f"{dir_name}/{file_name}")


cdef list get_strategy_args_list_parts(str strategy_name, int strategy_part_count, bint reduce_strategies):
    cdef int i
    cdef list strategy_args_list = list(get_strategy_args(strategy_name, reduce_strategies))
    cdef int strategy_args_list_len = len(strategy_args_list)
    cdef list strategy_args_range = list(range(0, strategy_args_list_len, strategy_part_count))
    cdef list strategy_args_list_parts = [strategy_args_list[i:i + strategy_part_count] for i in strategy_args_range]
    return strategy_args_list_parts


cdef list parallel_candles(str strategy_name, object df, list strategy_args_list):
    cdef object selected_strategy = dict(getmembers(ta_indicators, isfunction))[strategy_name]
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
    cdef np.ndarray strategy_array = main_df.loc[main_df.index[1]:, ['open', 'high', 'low', 'go_long', 'go_short', 'exit_long', 'exit_short']].values
    return strategy_array
