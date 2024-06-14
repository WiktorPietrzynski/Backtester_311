import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from pandas import DataFrame, concat
import numpy as np

from src.data_loader import get_data
from src.strategies import ta_indicators
from inspect import getmembers, isfunction


class Strategy:
    def __init__(self, symbol: str = "BTCUSDT", interval: str = "1d", data: DataFrame = None, start_date: str = "2017-09-01", end_date: str = "2025-01-01") -> None:
        self.symbol = symbol
        self.interval = interval
        self.df = data
        self.start_date = start_date
        self.end_date = end_date
        self.args = None
        self.strategy_name = None
        self.settings = None
        self.strategy_dict = dict(getmembers(ta_indicators, isfunction))

    def select(self, strategy_name: str, args: list):
        self._data_source()
        self._update_settings(strategy_name, args)
        self._calc_strategy(args)
        return self

    def get_settings(self) -> dict:
        return self.settings

    def get_data(self) -> DataFrame:
        return self.df

    def _data_source(self) -> None:
        if self.df is None:
            self.df = get_data(self.symbol, self.interval, self.start_date, self.end_date)
        else:
            self.df = self.df.copy()

    def _update_settings(self, strategy_name: str, args: list) -> None:
        self.strategy_name = strategy_name
        self.args = args
        settings = {"symbol": self.symbol, "interval": self.interval, "start_date": self.start_date, "end_date": self.end_date, "name": strategy_name}
        for i, arg in enumerate(args, 1):
            settings[f"arg_{i}"] = arg
        self.settings = settings

    def _calc_strategy(self, args) -> None:
        strategy_name = self.strategy_name.replace(" ", "_")
        strategy_dict = self.strategy_dict
        strategy_df = strategy_dict[strategy_name](self.df, *args)
        self.df = concat([self.df, strategy_df], axis=1)
        self._filter_data()

    def _filter_data(self) -> None:
        df = self.df
        df['date'] = df['date'].astype(str)
        df.index = df.index.astype(str)
        self.df = df[1:]


def strategy_select(strategy_name: str, strategy_args: list, data: DataFrame) -> np.ndarray:
    strategy_dict = dict(getmembers(ta_indicators, isfunction))
    df = data.copy()
    strategy_df = strategy_dict[strategy_name](df, *strategy_args)
    df = concat([df, strategy_df], axis=1)
    strategy_array = df.loc[df.index[1]:, ['open', 'high', 'low', 'go_long', 'go_short', 'exit_long', 'exit_short']].values
    return strategy_array
