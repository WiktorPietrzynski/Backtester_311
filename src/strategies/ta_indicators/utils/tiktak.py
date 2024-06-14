from pandas import DataFrame, Series
from pandas_ta import ema, macd, above, below
from src.strategies.ta_indicators.utils.ta_tools import simple_cross

def tiktak(df: DataFrame, fast_ma_len: int = 10, slow_ma_len: int = 30, fast_macd: int = 12, slow_macd: int = 26, macd_signal: int = 9) -> tuple[Series, Series]:
    fast_ma_len = int(fast_ma_len)
    slow_ma_len = int(slow_ma_len)
    fast_macd = int(fast_macd)
    slow_macd = int(slow_macd)
    macd_signal = int(macd_signal)

    df["fast_ma"] = ema(df["close"], fast_ma_len)
    df["slow_ma"] = ema(df["close"], slow_ma_len)

    macds = macd(df["close"], fast_macd, slow_macd, macd_signal).round(2)
    macds.columns = ["macd", "macd_h", "macd_s"]
    df["macd"] = macds["macd"]
    df["macd_h"] = macds["macd_h"]
    df["macd_s"] = macds["macd_s"]
    macd_cross_over, macd_cross_under= simple_cross(df["macd"], df["macd_s"])
    macd_above = above(df["macd"], df["macd_s"])
    macd_below = below(df["macd"], df["macd_s"])
    ma_cross_over, ma_cross_under = simple_cross(df["fast_ma"], df["slow_ma"])
    ma_above = above(df["fast_ma"], df["slow_ma"])
    ma_below = below(df["fast_ma"], df["slow_ma"])
    longs = (macd_above & ma_cross_over) | (ma_above & macd_cross_over)
    shorts = (macd_below & ma_cross_under) | (ma_below & macd_cross_under)
    return longs, shorts
