from pandas import DataFrame
from pandas_ta import macd, above_value, below_value

from src.strategies.ta_indicators.utils.ta_tools import simple_cross, simple_cross_value, create_strategy_df


def macd_cross_signal(df: DataFrame, fast_macd: int = 12, slow_macd: int = 26, macd_signal: int = 9) -> DataFrame:
    macds = macd(df.loc[:, 'close'], fast_macd, slow_macd, macd_signal).round(2)
    macds.columns = ["macd", "macd_h", "macd_s"]
    df.loc[:, 'macd'] = macds.loc[:, 'macd']
    df.loc[:, 'macd_h'] = macds.loc[:, 'macd_h']
    df.loc[:, 'macd_s'] = macds.loc[:, 'macd_s']
    entries_long1, entries_short1 = simple_cross_value(df.loc[:, 'macd_s'], 0)
    above, below = above_value(df.loc[:, 'macd'], 0), below_value(df.loc[:, 'macd'], 0)
    cross_over, cross_under = simple_cross(df.loc[:, 'macd'], df.loc[:, 'macd_s'])
    entry_long_series = (cross_over & below) | entries_long1
    entry_short_series = (cross_under & above) | entries_short1
    exit_short_series, exits_long_series = simple_cross(df.loc[:, 'macd'], df.loc[:, 'macd_s'])
    strategy_df = create_strategy_df(entry_long_series, entry_short_series, exits_long_series, exit_short_series)
    return strategy_df
