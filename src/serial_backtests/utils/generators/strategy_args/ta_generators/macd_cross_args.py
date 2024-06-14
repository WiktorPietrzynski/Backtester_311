def macd_cross_args(simplified: bool = False):
    if simplified:
        fast_macd_range = [*range(5, 101, 5)]
        slow_macd_range = [*range(10, 101, 5)]
        macd_signal_range = [*range(5, 50, 5)]
    else:
        fast_macd_range = [*range(5, 31), *range(35, 101, 5)]
        slow_macd_range = [*range(10, 31), *range(35, 101, 5)]
        macd_signal_range = [*range(5, 50, 1)]
    for fast_macd in fast_macd_range:
        for slow_macd in slow_macd_range:
            if slow_macd > fast_macd:
                for macd_signal in macd_signal_range:
                    yield [fast_macd, slow_macd, macd_signal]

