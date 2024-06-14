from pandas import DataFrame
from pandas_ta import rsi

from src.strategies.ta_indicators.utils.ta_tools import bands_cross_reverse, create_strategy_df


def rsi_bands_reverse(df: DataFrame, rsi_len: int = 14, upper_band: int = 70, down_band: int = 30) -> DataFrame:
    rsi_len = int(rsi_len)
    upper_band = int(upper_band)
    down_band = int(down_band)
    rsi_series_name, rsi_upper_band_name, rsi_lower_band_name = f"rsi_{rsi_len}", f"rsi_upper_band_{upper_band}", f"rsi_lower_band_{down_band}"
    rsi_series = rsi(df["close"], rsi_len).round(2)
    df[rsi_series_name] = rsi_series
    df[rsi_upper_band_name] = upper_band
    df[rsi_lower_band_name] = down_band
    entry_long_series, entry_short_series = bands_cross_reverse(df, rsi_upper_band_name, rsi_lower_band_name, rsi_series_name)
    strategy_df = create_strategy_df(entry_long_series, entry_short_series)
    return strategy_df

