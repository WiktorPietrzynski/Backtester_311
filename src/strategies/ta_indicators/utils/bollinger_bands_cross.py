from pandas import DataFrame
from src.strategies.ta_indicators.utils.ta_tools import chart_bands_cross
from pandas_ta import bbands


def bollinger_bands_cross(df: DataFrame, bb_len: int, bb_std: float, cross_type: str, exit_type: str = None):
    bb_df = bbands(df["close"], length=bb_len, std=bb_std)
    bb_df.columns = ["bb_lower", "bb_mid", "bb_upper", "bb_b", "bb_perc"]
    df["bb_lower"] = bb_df["bb_lower"]
    df["bb_mid"] = bb_df["bb_mid"]
    df["bb_upper"] = bb_df["bb_upper"]

    return chart_bands_cross(df, cross_type, exit_type, "bb_upper", "bb_mid", "bb_lower")
