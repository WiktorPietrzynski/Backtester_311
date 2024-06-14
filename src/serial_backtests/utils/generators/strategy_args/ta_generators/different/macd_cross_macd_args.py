def macd_cross_macd_args():
    fast_macd_range = [*range(3, 21), *range(30, 101, 10)]
    for fast_macd in fast_macd_range:
        slow_macd_range = [range_value for range_value in [*range(8, 31), *range(40, 101, 10)] if range_value > fast_macd]
        for slow_macd in slow_macd_range:
            for macd_signal in range(3, 31):
                yield [fast_macd, slow_macd, macd_signal]