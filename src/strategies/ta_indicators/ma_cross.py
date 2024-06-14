import pandas_ta as ta
from pandas import DataFrame

from src.strategies.ta_indicators.utils.ta_tools import simple_cross, create_strategy_df


def ma_cross(df: DataFrame, fast_ma_type: str = "ema", slow_ma_type: str = "ema", fast_ma_len: int = 10, slow_ma_len: int = 30) -> DataFrame:
    fast_ma_len = int(fast_ma_len)
    slow_ma_len = int(slow_ma_len)
    fast_ma_name, slow_ma_name = f"{fast_ma_type}_{fast_ma_len}", f"{slow_ma_type}_{slow_ma_len}"
    df.ta.cores = 0
    ma_cross_strategy = ta.Strategy(
        name="MA's cross",
        description="Moving averages cross",
        ta=[
            {"kind": fast_ma_type, "length": fast_ma_len, "everget": True, "col_names": fast_ma_name},
            {"kind": slow_ma_type, "length": slow_ma_len, "everget": True, "col_names": slow_ma_name},
        ]
    )
    df.ta.study(ma_cross_strategy)
    entry_long_series, entry_short_series = simple_cross(df[fast_ma_name], df[slow_ma_name])
    strategy_df = create_strategy_df(entry_long_series, entry_short_series)
    return strategy_df
