from pandas import DataFrame, concat
from pandas_ta import sma, linreg

from src.strategies.ta_indicators.utils.ta_tools import simple_cross, create_strategy_df


def squeeze_sma_cross(df: DataFrame, kc_len: int = 20, sma_len: int = 10) -> DataFrame:
    highest_high, lowest_low = df["high"].rolling(kc_len).max(), df["low"].rolling(kc_len).min()
    hl_df = concat([highest_high, lowest_low], axis=1)
    hl_mean, sma_close = hl_df.mean(axis=1), sma(df["close"], kc_len)
    hl_sma_df = concat([hl_mean, sma_close], axis=1)
    hl_sma_mean = hl_sma_df.mean(axis=1)
    sqz_series = df["close"] - hl_sma_mean
    sqz_series = linreg(sqz_series, kc_len).round(2)
    df[f"sqz_{kc_len}"] = sqz_series
    sqz_sma_series = sma(sqz_series, sma_len)
    df[f"sqz_sma_{sma_len}"] = sqz_sma_series
    enter_long_series, enter_short_series = simple_cross(sqz_series, sqz_sma_series)
    strategy_df = create_strategy_df(enter_long_series, enter_short_series)
    return strategy_df
