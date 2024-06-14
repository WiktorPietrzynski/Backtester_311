from src.data_loader import get_data
from src.strategies import Strategy, strategy_select

def test_strategies():
    symbol = "BTCUSDT"
    interval = "1d"
    data = get_data(start_date="01/01/2020", end_date="31/12/2022")
    strategy_name_and_args_list = [
        ["ma cross", ["ema", "ema", 10, 30]],
        ["atr_bands_cross", [30, 30, 150, "inside", "default"]],
        # ["bollinger_bands_cross", [20, 2.5, "sma", "outside"]],
        ["envelopes_bands_cross", ["ema", 30, 150, "middle", "same"]],
        ["envelopes_bands_cross", ["ema", 13, 24, "middle", "opposite"]],
        ["ma_cross", ["ema", "ema", 10, 30]],
        ["ma_cross", ["linreg", "linreg", 24, 35]],
        ["macd cross", [12, 26, 9, "trend"]],
        ["rsi_bands", [14, 70, 30, "opposite"]],
        ["rsi_sma_cross", [14, 14]],
        ["single_ma_cross", ["ema", 33]],
        ["squeeze", [20]],
        ["stoch_bands", [14, 3, 3, 80, 20]],
        ["tiktak", [10, 30, 12, 26, 9]],
        ["willr_bands", [14, -20, -80]]
    ]
    for strategy_name_and_args in strategy_name_and_args_list:
        strategy_name, strategy_args = strategy_name_and_args
        print(strategy_name, strategy_args)
        strategy = Strategy(symbol, interval, data)
        strategy_data = strategy.select(strategy_name, strategy_args)


if __name__=="__main__":
    test_strategies()
    print("Done!")  # Done!
