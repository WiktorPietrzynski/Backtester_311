from pandas import DataFrame, Series
from pandas_ta import willr

from src.strategies.ta_indicators.utils.ta_tools import bands_cross_inside


def willr_bands(df: DataFrame, willr_len: int, upper_band: int, down_band: int) -> tuple[Series, Series]:
    willr_series_name, willr_upper_band_name, willr_down_band_name = f"willr_{willr_len}", f"willr_upper_band_{upper_band}", f"willr_down_band_{down_band}"
    willr_series = willr(df['high'], df['low'], df['close'], willr_len).round(2)
    df[willr_series_name] = willr_series
    df[willr_upper_band_name] = upper_band
    df[willr_down_band_name] = down_band

    return bands_cross_inside(df[willr_series_name], df[willr_upper_band_name], df[willr_down_band_name])
