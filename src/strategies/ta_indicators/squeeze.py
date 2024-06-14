from pandas import DataFrame, concat
from pandas_ta import sma, linreg

from src.strategies.ta_indicators.utils.ta_tools import simple_cross_value, create_strategy_df


def squeeze(df: DataFrame, kc_len: int = 20) -> DataFrame:
    highest_high, lowest_low = df["high"].rolling(kc_len).max(), df["low"].rolling(kc_len).min()
    hl_df = concat([highest_high, lowest_low], axis=1)
    hl_mean, sma_close = hl_df.mean(axis=1), sma(df["close"], kc_len)
    hl_sma_df = concat([hl_mean, sma_close], axis=1)
    hl_sma_mean = hl_sma_df.mean(axis=1)
    sqz_series = df["close"] - hl_sma_mean
    sqz_series = linreg(sqz_series, kc_len).round(2)
    df[f"sqz_{kc_len}"] = sqz_series
    entry_long_series, entry_short_series = simple_cross_value(sqz_series, 0)
    strategy_df = create_strategy_df(entry_long_series, entry_short_series)
    return strategy_df
