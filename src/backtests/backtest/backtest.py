from pandas import DataFrame
from .settings import BacktestSettings
from .trade import Trade


class Backtest:
    def __init__(self, settings: dict, df: DataFrame):
        self.settings = BacktestSettings(**settings).get()
        self.cash = self.settings["init_cash"]
        self.candles = df[['date', 'open', 'high', 'low', 'go_long', 'go_short', "exit_long", "exit_short"]].values
        self.trade_list = []
        self.trade_df = None
        self.cum_profit = 100.0
        self.trade = None
        self.side = "wait"

    def run(self):
        return self._calc()

    def get_trades(self) -> DataFrame:
        return self.trade_df

    def _calc(self):
        candles = self.candles
        settings = self.settings
        for candle in candles:
            side = self.side
            if side == "wait":
                if candle[4]:
                    # open long
                    self._open_long(candle[0], candle[1], settings, candle[2], candle[3])
                elif candle[5]:
                    # open short
                    self._open_short(candle[0], candle[1], settings, candle[2], candle[3])
                else:
                    continue
            elif side == "long":
                if candle[5]:
                    # exit long open short
                    self._exit_trade("swap", candle[1], candle[0])
                    self._open_short(candle[0], candle[1], settings, candle[2], candle[3])
                else:
                    if candle[6]:
                        # exit long
                        self._exit_trade("exit", candle[1], candle[0])
                    else:
                        # calc long
                        self._calc_trade(candle[0], candle[2], candle[3])
            elif side == "short":
                if candle[4]:
                    # exit short open long
                    self._exit_trade("swap", candle[1], candle[0])
                    self._open_long(candle[0], candle[1], settings, candle[2], candle[3])
                else:
                    if candle[7]:
                        # exit short
                        self._exit_trade("exit", candle[1], candle[0])
                    else:
                        # calc short
                        self._calc_trade(candle[0], candle[2], candle[3])
            if self.cum_profit <= 0:
                break
        self._create_trade_df(self.trade_list)
        # print(self.trade_df.to_markdown())
        return self._make_summary(), settings

    def _open_long(self, open_date, open_price, settings, candle_high, candle_low):
        self.trade = Trade("long", open_date, open_price, settings)
        self._calc_trade(open_date, candle_high, candle_low)

    def _open_short(self, open_date, open_price, settings, candle_high, candle_low):
        self.trade = Trade("short", open_date, open_price, settings)
        self._calc_trade(open_date, candle_high, candle_low)

    def _exit_trade(self, exit_reason, exit_price, exit_date):
        trade = self.trade
        trade.exit(exit_reason, exit_price, exit_date)
        details = trade.get_details()
        self._trade_list_update(details)

    def _calc_trade(self, candle_date, candle_high, candle_low):
        trade = self.trade
        side = trade.calc(candle_date, candle_high, candle_low)
        if side == "wait":
            details = trade.get_details()
            self._trade_list_update(details)
        else:
            self.side = side

    def _trade_list_update(self, details) -> None:
        profit = details[8]
        self.trade_list.append(details)
        self.cum_profit = self.cum_profit * (1 + profit / 100)
        self.side = "wait"

    def _make_summary(self):
        trade_df = self.trade_df
        closed_trades = trade_df.shape[0]
        if closed_trades > 0:
            percent_profitable = round((trade_df['profit'] > 0).sum()/closed_trades * 100, 2)
            max_runup = trade_df['max runup'].max()
            average_runup = round(trade_df['max runup'].mean(), 2)
            max_drawdown = trade_df['max drawdown'].min()
            average_drawdown = round(trade_df['max drawdown'].mean(), 2)
            average_trade = round((trade_df['profit'].mean()), 2)
            cash_drawdown = round(trade_df["cash diff"].min(), 2)
            if trade_df['cash'].iloc[closed_trades-1] == 0:
                profit = -100.00
            else:
                profit = self.cum_profit - 100
            summary_values = (closed_trades, percent_profitable, max_runup, average_runup, max_drawdown, average_drawdown, average_trade, profit, cash_drawdown)
        else:
            summary_values = (0, 0, 0, 0, 0, 0, 0, 0, 0)
        summary_keys = ("closed trades", "percent profitable", "max runup", "average runup", "max drawdown", "average drawdown", "average trade", "profit", "cash drawdown")
        summary = dict(zip(summary_keys, summary_values))
        return summary

    def _create_trade_df(self, trade_list: list) -> None:
        init_cash = self.settings["init_cash"]
        trade_df = DataFrame(trade_list, columns=['side', 'exit reason', 'open date', 'exit date', 'open price', 'exit price', 'max drawdown', 'max runup', 'profit'])
        trade_df.index += 1
        cum_profit_series = (1 + (trade_df['profit'] / 100)).cumprod()
        trade_df["cash"] = init_cash * cum_profit_series
        first_profit = trade_list[0][8]
        if first_profit > -100:
            cash_ath = trade_df['cash'].shift(1, fill_value=init_cash).expanding().max()
            trade_df['cash diff'] = -(cash_ath - trade_df['cash']) / cash_ath * 100
        else:
            trade_df['cash diff'] = 0.00
        trade_df = trade_df.round({'max drawdown': 2, 'max runup': 2, 'cash': 2, 'profit': 2, 'cash diff': 2})
        self.trade_df = trade_df
