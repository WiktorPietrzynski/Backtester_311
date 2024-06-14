from pathlib import Path
from pandas import DataFrame
from src.data_loader import get_data
from src.serial_backtests.utils import multiprocessing_strategy, multiprocessing_backtest
from src.serial_backtests.utils.generators import get_backtest_args
from src.serial_backtests.utils.generators import get_strategy_args
from src.serial_backtests.utils import ConsoleProgress


def serial_backtest(interval_list: list, leverage_list: list, strategy_list: list, test_name: str = "test", start_date: str = "2017-09-01", end_date: str = "2025-01-01", simplify: bool = False) -> None:
    for symbol in ["BTCUSDT"]:
        for interval in interval_list:
            df = get_data(symbol, interval, start_date, end_date)
            for leverage in leverage_list:
                for strategy_name in strategy_list:
                    strategy_backtest = StrategyBacktest(symbol, interval, df)
                    strategy_backtest.set_backtest(leverage)
                    strategy_backtest.set_strategy(strategy_name, simplify, 100)
                    strategy_backtest.run(test_name)


class StrategyBacktest:
    def __init__(self, symbol: str, interval: str, df: DataFrame) -> None:
        self._symbol = symbol
        self._interval = interval
        self._df = df.copy()
        self._backtest_args_list = None
        self._leverage = None
        self._strategy_name = None
        self._slice_size = None
        self._save_count = None
        self._strategy_count = None
        self._strategy_args_list_slices = None

    def set_backtest(self, leverage: str) -> None:
        self._leverage = leverage
        self._backtest_args_list = list(get_backtest_args(leverage))
        return None

    def set_strategy(self, strategy_name: str, simplify: bool, slice_size: int = 10) -> None:
        self._strategy_name = strategy_name
        self._slice_size = slice_size
        self._save_count = int(slice_size * 0.1)
        strategy_args_list = list(get_strategy_args(strategy_name, simplify))
        strategy_args_list = strategy_args_list
        strategy_count = len(strategy_args_list)
        self._strategy_count = strategy_count
        strategy_args_range = range(0, strategy_count, slice_size)
        strategy_args_list_slices = [strategy_args_list[i:i + slice_size] for i in strategy_args_range]
        self._strategy_args_list_slices = strategy_args_list_slices
        return None

    def run(self, test_name: str):
        backtest_args_list = self._backtest_args_list
        strategy_args_list_slices = self._strategy_args_list_slices
        symbol = self._symbol
        interval = self._interval
        leverage = self._leverage
        strategy_name = self._strategy_name
        df = self._df
        progress = ConsoleProgress(self._strategy_count, self._strategy_name)
        for index, strategy_args_list in enumerate(strategy_args_list_slices, 1):
            strategy_list = multiprocessing_strategy(symbol, interval, strategy_name, df, strategy_args_list)
            backtest_list = multiprocessing_backtest(strategy_list, backtest_args_list)
            self._save(test_name, backtest_list, index)
            progress.append(len(strategy_args_list))
            # break for tests
            break
        print(f"Saved {test_name} - {symbol} - {interval} - x{leverage} - {strategy_name}")
        print("")
        return None

    def _save(self, test_name, backtest_list, index):
        if len(backtest_list) > 0:
            symbol = self._symbol
            interval = self._interval
            leverage = self._leverage
            strategy_name = self._strategy_name
            save_count = self._save_count
            result_df = DataFrame(backtest_list)
            result_df = result_df.sort_values(by=['profit', 'percent profitable'], ascending=False).reset_index(drop=True).head(save_count)
            # absolute_path = path.dirname(__file__)
            # file_name = f"{strategy_name}_{index}.feather"
            # dir_name = f"{absolute_path}/data/results/{self.__test_name}/{symbol}/{interval}/x{leverage}/{strategy_name}"
            # output_dir = Path(dir_name)
            # output_dir.mkdir(parents=True, exist_ok=True)
            # result_df.to_feather(f"{dir_name}/{file_name}")

            # for tests
            # file_name = f"{strategy_name}_{index}.csv"
            # dir_name = Path.home() / f"Desktop/results/data/{test_name}/{symbol}/{interval}/{strategy_name}"
            # output_dir = Path(dir_name)
            # output_dir.mkdir(parents=True, exist_ok=True)
            # result_df.to_csv(f"{dir_name}/{file_name}")


