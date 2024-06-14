def ma_cross_args(simplified: bool = False):
    if simplified:
        ma_types = ["sma", "ema"]
        fast_ma_range = [*range(5, 101, 5)]
        slow_ma_range = [*range(10, 201, 5)]
    else:
        # ma_types = ["sma", "ema", "linreg", "dema", "hma", "rma", "sinwma", "tema", "trima", "vidya", "wcp", "fwma", "alma", "jma", "kama", "mcgd", "ssf", "swma", "t3", "vwap", "vwma", "wma", "zlma"]
        ma_types = ["sma", "ema", "linreg"]
        fast_ma_range = [*range(5, 31), *range(35, 101, 5)]
        slow_ma_range = [*range(10, 31), *range(35, 201, 5)]

    for ma_type in ma_types:
        for fast_ma_len in fast_ma_range:
            for slow_ma_len in slow_ma_range:
                if slow_ma_len > fast_ma_len:
                    yield [ma_type, ma_type, fast_ma_len, slow_ma_len]
