from src.data_loader import get_data
from src.serial_backtests.utils.generators import ta_generators
from src.strategies import ta_indicators
from inspect import getmembers, isfunction
from src.strategies.strategy import Strategy



if __name__ == "__main__":
    symbol = "BTCUSDT"
    interval = "1d"
    data = get_data(start_date="01/01/2020", end_date="31/12/2022")
    # strategy_name = "ma cross"
    # strategy_args = ["ema", "ema", 10, 30]
    # strategy_name, ta_generators = "atr_bands_cross", [30, 30, 150, "inside", "default"]
    # strategy_name, ta_generators = "bollinger_bands_cross", [20, 2.5, "sma", "outside"]
    # strategy_name, ta_generators = "envelopes_bands_cross", ["ema", 30, 150, "middle", "same"]
    # strategy_name, ta_generators = "envelopes_bands_cross", ["ema", 13, 24, "middle", "opposite"]
    # strategy_name, ta_generators = "ma_cross", ["ema", "ema", 10, 30]
    # strategy_name, ta_generators = "ma_cross", ["linreg", "linreg", 24, 35]
    # strategy_name, ta_generators = "macd cross", [12, 26, 9, "trend"]
    # strategy_name, ta_generators = "rsi_bands", [14, 70, 30, "opposite"]
    # strategy_name, ta_generators = "rsi_sma_cross", [14, 14]
    # strategy_name, ta_generators = "single_ma_cross", ["ema", 33]
    # strategy_name, ta_generators = "squeeze", ["20"]
    # strategy_name, ta_generators = "stoch_bands", [14, 3, 3, 80, 20]
    # strategy_name, ta_generators = "tiktak", [10, 30, 12, 26, 9]
    # strategy_name, ta_generators = "willr_bands", [14, -20, -80]
    # strategy = Strategy(symbol, interval, data)
    # strategy_data = strategy.select(strategy_name, ta_generators)
    # print(strategy_data.get_data().to_markdown())

    # print(strategy_select(strategy_name, ta_generators, data).to_markdown())
    strategy_generators = dict(getmembers(ta_indicators, isfunction))
    # strategy_generators = dict(getmembers(ta_generators, isfunction))
    print(len(strategy_generators), "strategies")
    for name, function in strategy_generators.items():
        print(name, function)
        print(function(data))
        # xd = list(function())
        # print(len(xd))
        # s1 = Strategy(data=data)
        # s1.select(name)
        # df1 = s1.get_data()
        # print(len(df1))
        # args_list = list(function())[::10]
        # print(name)
        # print(len(args_list))
        # print(args_list[0])
        # multiprocessing_strategy("BTCUSDT", "1d", name, data, args_list)
