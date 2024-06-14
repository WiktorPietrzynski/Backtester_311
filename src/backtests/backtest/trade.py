class Trade:
    def __init__(self, side: str, open_date: str, open_price: float, settings: dict):
        self.side = side
        self.open_date = open_date
        self.open_price = open_price
        self.profit = 0.0
        self.max_runup = 0.0
        self.max_drawdown = 0.0
        self.trade_details = []

        self.stop_loss_type = settings["stop_loss_type"]
        self.stop_loss_value = settings["stop_loss_value"]
        self.take_profit_type = settings["take_profit_type"]
        self.take_profit_value = settings["take_profit_value"]
        self.fees = settings["fees"]
        self.leverage = settings["leverage"]
        self.stop_loss_price = None
        self.liquidation_price = None
        self.take_profit_price = None
        self._set_stop_loss_price()
        self._set_liquidation_price()
        self._set_take_profit_price()

    def get_details(self) -> list:
        return self.trade_details

    def _set_stop_loss_price(self) -> None:
        side = self.side
        open_price = self.open_price
        stop_loss_type = self.stop_loss_type
        stop_loss_value = self.stop_loss_value
        if stop_loss_value:
            if side == "short":
                self.stop_loss_value = stop_loss_value = stop_loss_value * (-1)
            if stop_loss_type == "percent":
                self.stop_loss_price = round(open_price * ((100 - stop_loss_value) / 100), 2)
            elif stop_loss_type == "value":
                self.stop_loss_price = round(open_price - stop_loss_value, 2)
            elif stop_loss_type == "trailing":
                self.stop_loss_price = round(open_price * ((100 - stop_loss_value) / 100), 2)
            else:
                raise ValueError(f"Invalid stop loss type: {stop_loss_type}")

    def _set_liquidation_price(self) -> None:
        side = self.side
        leverage = self.leverage
        open_price = self.open_price

        liquidation_percent = 1 / leverage
        if side == "short":
            liquidation_percent = liquidation_percent * (-1)
        self.liquidation_price = round(open_price * (1 - liquidation_percent), 2)

    def _set_take_profit_price(self) -> None:
        side = self.side
        open_price = self.open_price
        take_profit_type = self.take_profit_type
        take_profit_value = self.take_profit_value
        if take_profit_value != 0:
            if side == "short":
                self.take_profit_value = take_profit_value = take_profit_value * (-1)
            if take_profit_type == "percent":
                self.take_profit_price = round(open_price * ((100 + take_profit_value) / 100), 2)
            elif take_profit_type == "value":
                self.take_profit_price = open_price + take_profit_value
            else:
                raise ValueError(f"Invalid take profit type: {take_profit_type}")

    def calc(self, candle_date, candle_high, candle_low) -> str:

        if self._stop_loss(candle_date, candle_high, candle_low):
            side = "wait"
        elif self._liquidation(candle_date, candle_high, candle_low):
            side = "wait"
        elif self._take_profit(candle_date, candle_high, candle_low):
            side = "wait"
        else:
            side = self._update_stats(candle_high, candle_low)
        return side

    def _stop_loss(self, candle_date: str, candle_high: float, candle_low: float) -> bool:
        if self.stop_loss_value:
            side = self.side
            stop_loss_price = self.stop_loss_price
            if side == "long":
                if candle_low <= stop_loss_price:
                    self.exit("stop loss", stop_loss_price, candle_date, candle_high, stop_loss_price)
                    return True
            else:
                if candle_high >= stop_loss_price:
                    self.exit("stop loss", stop_loss_price, candle_date, stop_loss_price, candle_low)
                    return True
        self._update_stop_loss_price(candle_high, candle_low)
        return False

    def _update_stop_loss_price(self, candle_high: float, candle_low: float) -> None:
        stop_loss_value = self.stop_loss_value
        stop_loss_type = self.stop_loss_type
        if stop_loss_type == "trailing" and stop_loss_value:
            side = self.side
            open_price = self.open_price
            stop_loss_price = self.stop_loss_price
            if side == "long":
                if candle_high > open_price:
                    trailing_stop_loss_price = candle_high * ((100 - stop_loss_value) / 100)
                    if trailing_stop_loss_price > stop_loss_price:
                        self.stop_loss_price = trailing_stop_loss_price
            else:
                if candle_low < open_price:
                    trailing_stop_loss_price = candle_low * ((100 - stop_loss_value) / 100)
                    if trailing_stop_loss_price < stop_loss_price:
                        self.stop_loss_price = trailing_stop_loss_price


    def _liquidation(self, candle_date: str, candle_high: float, candle_low: float) -> bool:
        side = self.side
        liquidation_price = self.liquidation_price
        if side == "long":
            if liquidation_price >= candle_low:
                self.exit("liquidation", liquidation_price, candle_date, candle_high, liquidation_price)
                return True
        else:
            if liquidation_price <= candle_high:
                self.exit("liquidation", liquidation_price, candle_date, liquidation_price, candle_low)
                return True
        return False

    def _take_profit(self, candle_date: str, candle_high: float, candle_low: float) -> bool:
        take_profit_value = self.take_profit_value
        if take_profit_value:
            side = self.side
            take_profit_price = self.take_profit_price
            if side == "long":
                if take_profit_price <= candle_high:
                    self.exit("take profit", take_profit_price, candle_date, take_profit_price, candle_low)
                    return True
            else:
                if take_profit_price >= candle_low:
                    self.exit("take profit", take_profit_price, candle_date, candle_high, take_profit_price)
                    return True
        return False

    def _update_stats(self, highest_price: float, lowest_price: float) -> str:
        side = self.side
        open_price = self.open_price
        max_drawdown = self.max_drawdown
        max_runup = self.max_runup

        drawdown = round(100 * ((lowest_price - open_price) / open_price), 2)
        runup = round(100 * ((highest_price - open_price) / open_price), 2)
        if side == "short":
            drawdown, runup = -runup, -drawdown
        if 0 > drawdown < max_drawdown:
            self.max_drawdown = drawdown
        if 0 < runup > max_runup:
            self.max_runup = runup
        return side


    def exit(self, exit_reason: str, exit_price: float, exit_date: str, highest_price: float = None, lowest_price: float = None) -> None:
        if highest_price is not None and lowest_price is not None:
            self._update_stats(highest_price, lowest_price)
        self._calc_profit(exit_price)
        self.trade_details = [self.side, exit_reason, self.open_date, exit_date, self.open_price, exit_price, self.max_drawdown, self.max_runup, self.profit]

    def _calc_profit(self, exit_price: float) -> None:
        side = self.side
        open_price = self.open_price
        leverage = self.leverage
        fees = self.fees
        if side == "long":
            diff = (exit_price - open_price) / open_price
        else:
            diff = (open_price - exit_price) / open_price
        profit = diff * leverage * 100
        enter_fee = 100 * fees
        exit_fee = (100 + profit) * fees
        total_fee = enter_fee + exit_fee
        real_profit = round(profit - total_fee, 2)
        self.profit = real_profit
