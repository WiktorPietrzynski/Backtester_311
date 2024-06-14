from pandas import DataFrame
from pandas_ta import sma, ema
from src.strategies.ta_indicators.utils.ta_tools import chart_bands_cross


def envelopes_bands_cross(df: DataFrame, ma_type: str, ma_len: int, percent: int, cross_type: str, exit_type: str):
    ma_len = int(ma_len)
    if ma_type == "ema":
        df["ma"] = ma_series = ema(df["close"], ma_len)
    else:
        df["ma"] = ma_series = sma(df["close"], ma_len)
    df["upper_band"] = ma_series + (df["ma"] * (percent/100))
    df["lower_band"] = ma_series - (df["ma"] * (percent / 100))

    return chart_bands_cross(df, cross_type, exit_type, "upper_band", "ma", "lower_band")
