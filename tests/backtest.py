from src.data_loader import get_data
from src.strategies import Strategy, strategy_select
from src.backtests import *
from timeit import repeat
from pandas import DataFrame


def select_data():
    symbol = "BTCUSDT"
    interval = "1h"
    data = get_data(symbol, interval, start_date="2017-09-01", end_date="2022-09-01")
    # data = get_data(symbol, interval, start_date="2020-09-01", end_date="2023-09-01")
    # data = get_data(symbol, interval, start_date="2017-09-01", end_date="2023-09-01")
    return symbol, interval, data


def select_strategy():
    symbol, interval, data = select_data()
    # strategy_name, strategy_args = "atr_bands_cross", [30, 30, 150, "inside", "default"]
    # strategy_name, strategy_args = "bollinger_bands_cross", [20, 2.5, "sma", "outside"]
    # strategy_name, strategy_args = "envelopes_bands_cross", ["ema", 30, 150, "middle", "same"]
    # strategy_name, strategy_args = "envelopes_bands_cross", ["ema", 13, 24, "middle", "opposite"]
    strategy_name, strategy_args = "ma_cross", ["sma", "sma", 10, 30]
    # strategy_name, strategy_args = "ma_cross", ["ema", "ema", 10, 30]
    # strategy_name, strategy_args = "macd cross", [12, 26, 9]
    # strategy_name, strategy_args = "stochastic", [20, 30, 80, 30]
    # strategy_name, strategy_args = "macd cross", [40, 80, 15]
    # strategy_name, strategy_args = "rsi_bands", [14, 70, 30, "opposite"]
    # strategy_name, strategy_args = "rsi_sma_cross", [14, 14]
    # strategy_name, strategy_args = "single_ma_cross", ["ema", 33]
    # strategy_name, strategy_args = "squeeze", [20]
    # strategy_name, strategy_args = "stoch_bands", [14, 3, 3, 80, 20]
    # strategy_name, strategy_args = "tiktak", [10, 30, 12, 26, 9]
    # strategy_name, strategy_args = "willr_bands", [14, -20, -80]
    # strategy_name, strategy_args = "rsi_bands", [80, 50, 45, "default"]
    strategy = Strategy(symbol, interval, data)
    strategy.select(strategy_name, strategy_args)
    strategy_data = strategy.get_data()
    # strategy_data = strategy_select(strategy_name, strategy_args, data)
    return strategy_data


def select_backtest_settings() -> dict:
    # backtest_settings = {'leverage': '1', 'stop_loss_type': 'percent', 'stop_loss_value': 12.5, 'take_profit_type': 'percent', 'take_profit_value': 50.0, 'init_cash': 100.0, 'fees': 0.01}
    # backtest_settings = {"leverage": 1, "stop_loss_type": "percent", "stop_loss_value": 0.25, "take_profit_type": "percent", "take_profit_value": 0.25, "fees": 0.0}
    # backtest_settings = {'leverage': '1', 'stop_loss_type': 'trailing', 'stop_loss_value': 12.5, 'take_profit_type': 'percent', 'take_profit_value': 0.0, 'init_cash': 100.0, 'fees': 0.01}
    # backtest_settings = {'leverage': '1', 'stop_loss_type': 'percent', 'stop_loss_value': 10.0, 'take_profit_type': 'percent', 'take_profit_value': 10.0, 'init_cash': 100.0, 'fees': 0.0}
    # backtest_settings = {'leverage': '1', 'stop_loss_type': 'trailing', 'stop_loss_value': 0.0, 'take_profit_type': 'percent', 'take_profit_value': 0.0, 'init_cash': 100.0, 'fees': 0.0}
    # backtest_settings = {'leverage': '1', 'stop_loss_type': 'percent', 'stop_loss_value': 4.0, 'take_profit_type': 'percent', 'take_profit_value': 0.0, 'init_cash': 100.0, 'fees': 0.0}
    # backtest_settings = {'leverage': '1', 'stop_loss_type': 'percent', 'stop_loss_value': 40.0, 'take_profit_type': 'percent', 'take_profit_value': 0.0, 'init_cash': 100.0, 'fees': 0.01}
    backtest_settings = {'leverage': '1', 'stop_loss_type': 'trailing', 'stop_loss_value': 2.5, 'take_profit_type': 'percent', 'take_profit_value': 25, 'init_cash': 100.0, 'fees': 0.01}

    return backtest_settings


def run_backtest(settings, data) -> dict:
    summary, bt_settings = Backtest(settings, data).run()
    # print("profit:", summary["profit"])
    # print("[", summary["profit"], summary["average trade"], summary["closed trades"], summary["percent profitable"], summary["cash drawdown"], "]")
    # print(summary, bt_settings)
    print(DataFrame.from_dict(summary, orient='index').transpose().to_markdown())
    return summary


def run_advanced_backtest(data, settings) -> float:
    summary = advanced_backtest(data, settings, True, 5, False)
    # profit = summary[0]
    # print("profit:", profit)
    print([round(value, 2) for value in summary])
    profit = 9.99
    return profit


# def run_simple_cython_backtest(backtest_settings, strategy):
#     settings_list = CythonBacktestSettings(**backtest_settings).get_list()
#     candles = strategy.get_data()[['open', 'high', 'low', 'go_long', 'go_short', 'exit_long', 'exit_short']].values
#     profit = basic_backtest(candles, settings_list)
#     print("profit:", profit)
#     # return profit


# def compare_backtests():
#     summary1 = run_backtest()
#     summary2 = run_backtest2()
#     keys = summary1.keys()
#     for key in keys:
#         value1 = round(summary1[key], 4)
#         value2 = round(summary2[key], 4)
#         if value1 != value2:
#             raise ValueError(f"{key}: {value1} != {value2}")
#     print("test_passed")



if __name__ == "__main__":
    backtest_settings = select_backtest_settings()
    backtest_data = select_strategy()
    # basic_backtest_settings = BasicBacktestSettings(**backtest_settings).get_list()
    basic_backtest_data = select_strategy()[['open', 'high', 'low', 'go_long', 'go_short', 'exit_long', 'exit_short']].values
    number = 1
    repeats = 1
    print(min(repeat("run_backtest(backtest_settings, backtest_data)", number=number, repeat=repeats, globals=globals())))
    print("")
    # print(min(repeat("run_basic_backtest(basic_backtest_data, basic_backtest_settings)", number=number, repeat=repeats, globals=globals())))
    # print("")
    print(min(repeat("run_advanced_backtest(basic_backtest_data, basic_backtest_settings)", number=number, repeat=repeats, globals=globals())))
    print("")
    # print(min(repeat("run_advanced_backtest2(basic_backtest_data, basic_backtest_settings)", number=number, repeat=repeats, globals=globals())))
    # print("")
    # 0.00031630000012228265
    # 0.00034540000001470617
    # 0.00024999999959618435
    # 0.00994829999990543
    # profit: 350.9130905027858
    # 3.909999986717594e-05
    # profit: 350.9130905027858
    # 4.7200000153679866e-05

    # 0.003982700000051409
    # 0.0004921999998259707
    # 0.0013361999999688123
    # 0.008382199999687145
    # 0.04257589999906486
    # 0.004910199999358156

    # compare_backtests()



    # test_strategies()