from pandas import DataFrame, Series
from pandas_ta import rsi, sma

from src.strategies.ta_indicators.utils.ta_tools import simple_cross


def rsi_sma_cross(df: DataFrame, rsi_len: int, rsi_sma_len: int)  -> tuple[Series, Series]:
    rsi_series_name, rsi_sma_name = f"rsi_{rsi_len}", f"rsi_sma_{rsi_sma_len}"
    rsi_series = rsi(df["close"], rsi_len).round(2)
    df[rsi_series_name] = rsi_series
    rsi_sma_series = sma(rsi_series, rsi_sma_len)
    df[rsi_sma_name] = rsi_sma_series
    return simple_cross(rsi_series, rsi_sma_series)
