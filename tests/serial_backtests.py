# from src.serial_backtests import serial_basic_backtest, serial_backtest
from src.serial_backtests.serial_backtest import serial_backtest
from src.serial_backtests.serial_basic_backtest import serial_basic_backtest
from src.serial_backtests.serial_selected_backtest import serial_selected_backtest
from src.serial_backtests.serial_advanced_backtest import serial_advanced_backtest
from timeit import repeat
from time import time

if __name__ == '__main__':
    interval_list = ["1d"]
    leverage_list = ["1"]
    # strategy_list =  ["macd_cross", "ma_cross", "rsi_bands_reverse", "stochastic"]
    # strategy_list = ["macd_cross", "ma_cross", "rsi_bands_reverse"]
    # strategy_list = ["stochastic"]
    # strategy_list = ["bollinger bollinger_bands cross"]
    # strategy_list = ["ma_cross"]
    strategy_list = ["macd cross"]
    # strategy_list = ["bollinger bollinger_bands cross", "envelopes bollinger_bands cross", "ma_cross"]
    # strategy_list = ["macd cross", "rsi bollinger_bands", "rsi sma cross", "single_ma_cross"]
    # strategy_list = ["squeeze", "stoch bollinger_bands", "willr bollinger_bands", "atr_bands_cross"]
    # strategy_list = ["tiktak"]
    # strategy_list = ["bollinger bollinger_bands cross", "envelopes bollinger_bands cross", "ma_cross", "macd cross", "rsi bollinger_bands", "rsi sma cross", "single_ma_cross", "squeeze", "stoch bollinger_bands", "willr bollinger_bands", "atr_bands_cross"]
    # strategy_list = ["bollinger bollinger_bands cross", "envelopes bollinger_bands cross", "ma_cross", "macd cross", "rsi bollinger_bands", "rsi sma cross", "single_ma_cross", "squeeze", "stoch bollinger_bands", "willr bollinger_bands", "atr_bands_cross", "tiktak"]

    def run_serial_backtest():
        test_name = "test_022"
        start_date = "2017-09-01"
        end_date = "2020-09-01"
        serial_backtest(interval_list, leverage_list, strategy_list, test_name, start_date, end_date)


    def run_serial_basic_backtest():
        test_name = "test_05"
        start_date = "2017-09-01"
        end_date = "2020-09-01"
        serial_basic_backtest(interval_list, strategy_list, test_name, start_date, end_date)


    def run_serial_basic_backtest2():
        test_name = "test_04"
        start_date = "2017-09-01"
        end_date = "2023-09-01"
        serial_basic_backtest(interval_list, strategy_list, test_name, start_date, end_date)


    def run_serial_selected_backtest():
        test_name = "test_04"
        start_date = "2020-09-01"
        end_date = "2023-09-01"
        serial_selected_backtest(interval_list, strategy_list, test_name, start_date, end_date)

    def run_serial_selected_backtest2():
        test_name = "test_04"
        start_date1 = "2017-09-01"
        end_date1 = "2021-09-01"
        start_date2 = "2021-09-01"
        end_date2 = "2023-09-01"
        interval = interval_list[0]
        serial_selected_backtest(interval, strategy_list, start_date1, end_date1, start_date2, end_date2)

    def run_serial_advanced_backtest():
        test_name = "test_f2"
        start_date = "2017-09-01"
        end_date = "2020-09-01"
        serial_advanced_backtest(interval_list, strategy_list, start_date, end_date, 3, False, True, False)



    # print(min(repeat("run_serial_backtest('facts')", number=1, repeat=1, globals=globals())))
    # print(min(repeat("run_serial_backtest()", number=1, repeat=1, globals=globals())))
    # print(min(repeat("run_serial_basic_backtest()", number=1, repeat=1, globals=globals())))
    # print(min(repeat("run_serial_selected_backtest2()", number=1, repeat=1, globals=globals())))
    print(min(repeat("run_serial_advanced_backtest()", number=1, repeat=1, globals=globals())))
    # 51.455203299999994
    # 51.1691708999997
    # run_serial_advanced_backtest()
    # 0.026168800000050396 vs 0.0253658000001451
    # 27.12994780000008 vs 27.08980419999989
    # 126.18646330000047 vs 123.82781259999956