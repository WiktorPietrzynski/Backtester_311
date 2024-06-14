from pandas import Series, DataFrame
from pandas_ta import cross


def cross_over(series_1: Series, series_2: Series) -> Series:
    cross_over_series = cross(series_1, series_2)
    return cross_over_series


def cross_under(series_1: Series, series_2: Series) -> Series:
    cross_under_series = cross(series_2, series_1)
    return cross_under_series


def simple_cross(series_1: Series, series_2: Series) -> tuple[Series, Series]:
    cross_over_series = cross(series_1, series_2)
    cross_under_series = cross(series_2, series_1)
    return cross_over_series, cross_under_series


def cross_over_value(series: Series, value: float) -> Series:
    value_series = Series(value, index=series.index)
    cross_over_value_series = cross(series, value_series)
    return cross_over_value_series


def cross_under_value(series: Series, value: float) -> Series:
    value_series = Series(value, index=series.index)
    cross_under_value_series = cross(value_series, series)
    return cross_under_value_series


def simple_cross_value(series: Series, value: float) -> tuple[Series, Series]:
    value_series = Series(value, index=series.index)
    cross_over_value_series = cross(series, value_series)
    cross_under_value_series = cross(value_series, series)
    return cross_over_value_series, cross_under_value_series


def bands_cross_reverse(df: DataFrame, upper_band_name: str, lower_band_name: str, line_name: str) -> tuple[Series, Series]:
    upper_band = df[upper_band_name]
    lower_band = df[lower_band_name]
    series = df[line_name]
    cross_over_band_series = cross(series, lower_band)
    cross_under_band_series = cross(upper_band, series)
    return cross_over_band_series, cross_under_band_series


def bands_cross_trend(df: DataFrame,  upper_band_name: str, lower_band_name: str, line_name: str) -> tuple[Series, Series]:
    upper_band = df[upper_band_name]
    lower_band = df[lower_band_name]
    series = df[line_name]
    cross_over_band_series = cross(series, upper_band)
    cross_under_band_series = cross(lower_band, series)
    return cross_over_band_series, cross_under_band_series


def chart_bands_cross(df: DataFrame, cross_type: str, exit_type: str, upper_band_name: str, middle_band_name: str, lower_band_name: str):
    upper_band = df[upper_band_name]
    lower_band = df[lower_band_name]
    middle_band = df[middle_band_name]
    close_series = df["close"]
    if cross_type == "inside":
        entries_long, entries_short = bands_cross_reverse(df, upper_band, lower_band, close_series)
        if exit_type == "middle":
            exits_short_stop, exits_long_stop = bands_cross_trend(df, upper_band, lower_band, close_series)
            exits_short_take, exits_long_take = simple_cross(middle_band, close_series)
            exits_long, exits_short = exits_long_stop | exits_long_take, exits_short_stop | exits_short_take
            return entries_long, entries_short, exits_long, exits_short
        elif exit_type == "opposite":
            exits_short_stop, exits_long_stop = bands_cross_trend(df, upper_band, lower_band, close_series)
            exits_long_take, exits_short_take = bands_cross_trend(df, upper_band, lower_band, close_series)
            exits_long, exits_short = exits_long_stop | exits_long_take, exits_short_stop | exits_short_take
            return entries_long, entries_short, exits_long, exits_short
        else:
            exits_short, exits_long = bands_cross_trend(df, upper_band, lower_band, close_series)
            return entries_long, entries_short, exits_long, exits_short
    elif cross_type == "middle":
        entries_long, entries_short = simple_cross(close_series, middle_band)
        if exit_type == "opposite":
            exits_long, exits_short = bands_cross_trend(df, upper_band, lower_band, close_series)
            return entries_long, entries_short, exits_long, exits_short
        elif exit_type == "same":
            exits_short, exits_long = bands_cross_reverse(df, upper_band, lower_band, close_series)
            return entries_long, entries_short, exits_long, exits_short
        else:
            return entries_long, entries_short

def create_strategy_df(go_long_series: Series, go_short_series: Series, exit_long_series: Series = None, exit_short_series: Series = None) -> DataFrame:
    strategy_df = DataFrame({
        "go_long": go_long_series.shift(fill_value=0.0),
        "go_short": go_short_series.shift(fill_value=0.0)})
    
    if exit_long_series is not None:
        strategy_df["exit_long"] = (exit_long_series.shift(fill_value=0.0).astype(int) | strategy_df["go_short"].astype(int)).astype(
            float)
    else:
        strategy_df["exit_long"] = strategy_df["go_short"]
    if exit_short_series is not None:
        strategy_df["exit_short"] = (exit_short_series.shift(fill_value=0.0).astype(int) | strategy_df["go_long"].astype(int)).astype(
            float)
    else:
        strategy_df["exit_short"] = strategy_df["go_long"]
    return strategy_df