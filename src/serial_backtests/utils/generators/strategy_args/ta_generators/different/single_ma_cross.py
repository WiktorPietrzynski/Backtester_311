def single_ma_cross():
    ma_types = ["sma", "ema", "linreg", "dema", "hma", "rma", "sinwma", "tema", "trima", "vidya", "wcp", "fwma", "alma", "jma", "kama", "mcgd", "ssf", "swma", "t3", "vwap", "vwma", "wma", "zlma"]
    # ma_range = [*range(3, 51), *range(55, 101, 5)]
    ma_range = [*range(3, 101)]
    for ma_type in ma_types:
        for ma_len in ma_range:
            yield [ma_type, ma_len]
