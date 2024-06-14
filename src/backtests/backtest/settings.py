class BacktestSettings:
    def __init__(self, leverage: float = 1, stop_loss_type: str = "percent", stop_loss_value: float = 0.00,
                 take_profit_type: str = "percent", take_profit_value: float = 0.00, trailing_stop_limit: float = 0.00,
                 trailing_stop_max: float = 0.00, init_cash: float = 100, fees: float = 0.00) -> None:
        leverage, take_profit_value, stop_loss_value = float(leverage), float(take_profit_value), float(stop_loss_value)
        if leverage <= 0:
            raise ValueError("Leverage should be positive")
        if stop_loss_value < 0:
            raise ValueError("Stop loss should be positive")
        if take_profit_value < 0:
            raise ValueError("Take profit should be positive")
        if init_cash <= 0:
            raise ValueError("Init cash should be positive")
        self.leverage = leverage
        self.stop_loss_type = stop_loss_type
        self.stop_loss_value = stop_loss_value
        self.take_profit_type = take_profit_type
        self.take_profit_value = take_profit_value
        self.init_cash = init_cash
        self.fees = fees / 100

    def get(self) -> dict:
        return vars(self)
