import pandas_ta as ta
from pandas import DataFrame, Series

from src.strategies.ta_indicators.utils.ta_tools import simple_cross


def single_ma_cross(df: DataFrame, ma_type: str, ma_len: int) -> tuple[Series, Series]:
    ma_name = f"{ma_type}_{ma_len}"
    df.ta.cores = 0
    ma_cross_strategy = ta.Strategy(
        name="single ma cross",
        description="single moving average cross",
        ta=[
            {"kind": ma_type, "length": ma_len, "everget": True, "col_names": ma_name},
        ]
    )
    df.ta.study(ma_cross_strategy)
    return simple_cross(df["close"], df[ma_name])
