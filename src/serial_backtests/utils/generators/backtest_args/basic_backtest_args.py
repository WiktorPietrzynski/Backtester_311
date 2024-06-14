def get_basic_backtest_args(reduce_backtests: bool = False):
    if reduce_backtests:
        yield[2.0, 0.0, 2.0, 0.0, 0.01]
    else:
        stop_loss_types = [2.0, 3.0]
        stop_loss_values = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 7.5, 10.0, 12.5, 15.0, 20.0, 25.0]
        for stop_loss_type in stop_loss_types:
            for stop_loss_value in stop_loss_values:
                if stop_loss_value == 0.0 and stop_loss_type == 3.0:
                    continue
                take_profit_values = get_take_profit_values(stop_loss_value)
                for take_profit_value in take_profit_values:
                    yield [stop_loss_type, stop_loss_value, 2.0, take_profit_value, 0.01]


def get_take_profit_values(stop_loss_value: float) -> list:
    take_profit_values = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 7.5, 10.0, 12.5, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0]
    take_profit_values = [take_profit_value for take_profit_value in take_profit_values if take_profit_value <= stop_loss_value * 100]
    return take_profit_values
