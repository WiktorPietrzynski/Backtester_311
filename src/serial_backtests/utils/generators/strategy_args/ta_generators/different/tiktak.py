def tiktak():
    fast_ma_range = [*range(10, 101, 10)]
    for fast_ma_len in fast_ma_range:
        slow_ma_range = [range_value for range_value in [*range(20, 201, 10)] if range_value > fast_ma_len]
        for slow_ma_len in slow_ma_range:
            fast_macd_range = [*range(4, 21, 2), *range(30, 101, 10)]
            for fast_macd in fast_macd_range:
                slow_macd_range = [range_value for range_value in [*range(8, 31, 2), *range(40, 101, 10)] if range_value > fast_macd]
                for slow_macd in slow_macd_range:
                    for macd_signal in range(3, 31, 3):
                        yield [fast_ma_len, slow_ma_len, fast_macd, slow_macd, macd_signal]
