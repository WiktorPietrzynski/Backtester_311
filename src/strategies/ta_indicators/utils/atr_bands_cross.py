from pandas import DataFrame
from pandas_ta import atr, sma
from src.strategies.ta_indicators.utils.ta_tools import chart_bands_cross


def atr_bands_cross(df: DataFrame, sma_len: int, atr_len: int, atr_percent: int, cross_type: str, exit_type: str = None):
    sma_name, atr_name = f"sma_{sma_len}", f"atr_{atr_len}"
    df[atr_name] = atr(df["high"], df["low"], df["close"], atr_len)
    df[sma_name] = sma(df["close"], sma_len)
    df["upper_band"] = df[sma_name] + (df[atr_name] * (atr_percent/100))
    df["lower_band"] = df[sma_name] - (df[atr_name] * (atr_percent/100))

    return chart_bands_cross(df, cross_type, exit_type, "upper_band", sma_name, "lower_band")
