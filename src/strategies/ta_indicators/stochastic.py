from pandas import DataFrame
from pandas_ta import stoch
from src.strategies.ta_indicators.utils.ta_tools import simple_cross, cross_over_value, cross_under_value, create_strategy_df

def stochastic(data: DataFrame, k_period: int = 14, d_period: int = 3, upper_band: int = 80, down_band: int = 20) -> DataFrame:
    k_period = int(k_period)
    d_period = int(d_period)
    upper_band = int(upper_band)
    down_band = int(down_band)
    stoch_df = stoch(data["high"], data["low"], data["close"], k=k_period, d=d_period)
    stoch_df.columns = ["stoch_k", "stoch_d", "stoch_h"]
    stoch_k = stoch_df["stoch_k"]
    stoch_d = stoch_df["stoch_d"]
    k_crossover_d, k_crossunder_d = simple_cross(stoch_k, stoch_d)
    k_crossover_20 = cross_over_value(stoch_k, upper_band)
    k_crossunder_80 = cross_under_value(stoch_k, down_band)
    k_above_80 = stoch_k > upper_band
    k_below_20 = stoch_k < down_band
    entry_long_series = (k_crossover_20 | (k_crossover_d & k_below_20) ) * 1
    entry_short_series = (k_crossunder_80 | (k_crossunder_d & k_above_80)) * 1
    strategy_df = create_strategy_df(entry_long_series, entry_short_series)
    return strategy_df
