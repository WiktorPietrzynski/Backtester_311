from multiprocessing import Pool
from pandas import DataFrame
from src.backtests import Backtest
from src.strategies import Strategy


def multiprocessing_director(args_list: list, function: callable) -> list:
    with Pool() as pool:
        result = pool.map(function, args_list)
        # clean_result = list(filter(None, result))
    # return clean_result
    return result


def multiprocessing_strategy(symbol: str, interval: str, strategy_name: str, df: DataFrame, strategy_args_part: list) -> list:
    args_list = [(symbol, interval, strategy_name, df, strategy_args) for strategy_args in strategy_args_part]
    strategy_list = multiprocessing_director(args_list, processing_strategy)
    return strategy_list


def processing_strategy(settings_list: list) -> tuple:
    symbol, interval, strategy_name, df, strategy_args = settings_list
    strategy = Strategy(symbol, interval, df)
    strategy.select(strategy_name, strategy_args)
    return strategy.get_data(), strategy.get_settings()


def multiprocessing_backtest(strategy_list: list, backtest_args_list: list) -> list:
    args_list = [(strategy[0], strategy[1], backtest_args) for backtest_args in backtest_args_list for strategy in strategy_list]
    backtest_list = multiprocessing_director(args_list, processing_backtest)
    # print(sorted(backtest_list))
    # print(len(backtest_list))
    return backtest_list


def processing_backtest(backtest_set: list) -> dict:
    strategy_data, strategy_settings, backtest_args = backtest_set
    summary, bt_settings = Backtest(backtest_args, strategy_data).run()
    return {**summary, **bt_settings, **strategy_settings}


def multiprocessing_detailed_backtest(strategy_list: list, backtest_args_list: list):
    args_list = [(strategy[0], strategy[1], backtest_args_list[i]) for i, strategy in enumerate(strategy_list)]
    backtest_list = multiprocessing_director(args_list, processing_backtest)
    return backtest_list
