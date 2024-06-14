from pandas import DataFrame, Series
from pandas_ta import stoch

from src.strategies.ta_indicators.utils.ta_tools import bands_cross_inside


def stoch_bands(df: DataFrame, stoch_k: int, stoch_d: int, stoch_smooth_k: int, upper_band: int, down_band: int)  -> tuple[Series, Series]:
    stoch_upper_band_name, stoch_down_band_name = f"stoch_upper_band_{upper_band}", f"stoch_down_band_{down_band}"
    stochs = stoch(df["high"], df["low"], df["close"], stoch_k, stoch_d, stoch_smooth_k).round(2)
    stochs.columns = ["stoch_k", "stoch_d", "stoch_h"]
    df["stoch_k"] = stochs["stoch_k"]
    df[stoch_upper_band_name] = upper_band
    df[stoch_down_band_name] = down_band

    return bands_cross_inside(df["stoch_k"], df[stoch_upper_band_name], df[stoch_down_band_name])
