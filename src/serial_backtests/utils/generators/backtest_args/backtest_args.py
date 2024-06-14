def get_backtest_args(leverage: str):
    stop_loss_types = ["percent", "trailing"]
    stop_loss_values = get_stop_loss_values(leverage)
    take_profit_types = ["percent"]
    fees = [0.01]

    for stop_loss_type in stop_loss_types:
        for stop_loss_value in stop_loss_values:
            if stop_loss_value == 0.0 and stop_loss_type == "trailing":
                continue
            for take_profit_type in take_profit_types:
                take_profit_values = get_take_profit_values(stop_loss_value)
                for take_profit_value in take_profit_values:
                    for fee in fees:
                        backtest_settings = {"leverage": leverage, "stop_loss_type": stop_loss_type, "stop_loss_value": stop_loss_value, "take_profit_type": take_profit_type, "take_profit_value": take_profit_value, "init_cash": 100.00, "fees": fee}
                        yield backtest_settings


def get_stop_loss_values(leverage: str) -> list:
    leverage = float(leverage)
    stop_loss_values = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 7.5, 10.0, 12.5, 15.0, 20.0, 25.0]
    stop_loss_values = [value for value in stop_loss_values if value * leverage < 100]
    return stop_loss_values


def get_take_profit_values(stop_loss_value: float) -> list:
    take_profit_values = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 7.5, 10.0, 12.5, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0]
    take_profit_values = [take_profit_value for take_profit_value in take_profit_values if take_profit_value <= stop_loss_value * 100]
    return take_profit_values
