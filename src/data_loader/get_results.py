from os import path
from glob import glob
from pandas import DataFrame, read_feather, concat


def get_results(interval: str = "1d", start_date: str = "2017-09-01", end_date: str = "2025-01-01", strategy_list: list = None, reset_index: bool = True):
    src_path = path.dirname(__file__)
    dir_path = f"{src_path}\\results\\{interval}_{start_date}_{end_date}"
    results_df = DataFrame()
    for strategy_name in strategy_list:
        strategy_results_df = _load_strategy(dir_path, strategy_name)
        results_df = concat([results_df, strategy_results_df])
    if results_df.empty is False and reset_index is True:
        results_df = results_df.sort_values("profit", ascending=False).head(10000).reset_index(drop=True).round(2)
    return results_df


def _load_strategy(dir_path: str, strategy_name: str) -> DataFrame:
    strategy_name = strategy_name.replace(" ", "_")
    strategy_results_df = DataFrame()
    files_path = f"{dir_path}\\{strategy_name}\\*.feather"
    filepath_list = glob(files_path)
    if len(filepath_list) > 0:
        for filepath in filepath_list:
            try:
                df = read_feather(filepath)
                strategy_results_df = concat([strategy_results_df, df])
            except FileNotFoundError:
                return DataFrame()
    else:
        return DataFrame()
    return strategy_results_df
