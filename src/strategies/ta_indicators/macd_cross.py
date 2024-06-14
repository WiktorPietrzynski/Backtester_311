from pandas import DataFrame
from pandas_ta import macd

from src.strategies.ta_indicators.utils.ta_tools import simple_cross, create_strategy_df


def macd_cross(df: DataFrame, fast_macd: int = 12, slow_macd: int = 26, macd_signal: int = 9) -> DataFrame:
    fast_macd = int(fast_macd)
    slow_macd = int(slow_macd)
    macd_signal = int(macd_signal)
    macds = macd(df.loc[:, 'close'], fast_macd, slow_macd, macd_signal).round(2)
    macds.columns = ["macd", "macd_h", "macd_s"]
    df.loc[:, 'macd'] = macds.loc[:, 'macd']
    df.loc[:, 'macd_h'] = macds.loc[:, 'macd_h']
    df.loc[:, 'macd_s'] = macds.loc[:, 'macd_s']
    entry_long_series, entry_short_series = simple_cross(df.loc[:, 'macd'], df.loc[:, 'macd_s'])
    strategy_df = create_strategy_df(entry_long_series, entry_short_series)
    return strategy_df
