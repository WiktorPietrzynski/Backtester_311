from pandas import DataFrame, concat, read_feather
from src.data_loader import get_data
from src.serial_backtests.utils.python_multiprocessing import multiprocessing_strategy, multiprocessing_detailed_backtest
from os import path
from pathlib import Path
from glob import glob

def save_results(backtest_list: list, interval: str, strategy_name: str, test_name: str):
    backtest_df = DataFrame(backtest_list).sort_values("profit", ascending=False).reset_index(drop=True)
    file_name = f"{strategy_name}.feather"
    file_path = path.dirname(__file__)
    src_path = path.dirname(path.dirname(file_path))
    dir_name = f"{src_path}/results/{test_name}_compare/{interval}/{strategy_name}"
    output_dir = Path(dir_name)
    output_dir.mkdir(parents=True, exist_ok=True)
    backtest_df.to_feather(f"{dir_name}/{file_name}")
    print(backtest_df)

def load_args(strategy_name: str, interval: str, test_name: str):
    results_df = DataFrame()
    strategy_name = strategy_name.replace(" ", "_")
    file_path = path.dirname(__file__)
    src_path = path.dirname(path.dirname(file_path))
    dir_name = f"{src_path}/results/{test_name}/{interval}/{strategy_name}/*.feather"
    filepath_list = glob(dir_name)
    for filepath in filepath_list:
        try:
            df = read_feather(filepath)
            results_df = concat([results_df, df])
        except FileNotFoundError:
            print(filepath)
            exit("Result not found")
    rows_count = len(results_df)
    column_count = len(results_df.columns)
    results_df = results_df.sort_values(by=['profit'], ascending=False).reset_index(drop=True).head(
        int(rows_count * 0.1))
    results_df["stop_loss_type"] = results_df["stop_loss_type"].replace(2.0, "percent").replace(3.0, "trailing")
    results_df["take_profit_type"] = results_df["take_profit_type"].replace(2.0, "percent")
    backtest_args_list = results_df.iloc[:, 1:5].to_dict('records')
    strategy_args_list = results_df.iloc[:, 8:column_count].values.tolist()
    return backtest_args_list, strategy_args_list


def serial_detailed_backtest(interval_list: list, strategy_list: list, test_name: str, start_date: str = "2017-09-01", end_date: str = "2025-01-01"):
    symbol = "BTCUSDT"
    for interval in interval_list:
        for strategy_name in strategy_list:
            backtest_args_list, strategy_args_list = load_args(strategy_name, interval, test_name)
            df = get_data(symbol, interval, start_date, end_date)
            strategy_list = multiprocessing_strategy(symbol, interval, strategy_name, df, strategy_args_list)
            backtest_list = multiprocessing_detailed_backtest(strategy_list, backtest_args_list)
            save_results(backtest_list, interval, strategy_name, test_name)

if __name__ == "__main__":
    serial_detailed_backtest(["1d"], ["ma cross"], "test_01")