def stochastic_args(simplified: bool = False):
    if simplified:
        k_period_range = [*range(5, 101, 5)]
        d_period_range = [*range(5, 101, 5)]
        # upper_band_range = [70, 80, 90]
        # down_band_range = [10, 20, 30]
        upper_band_range = [80]
        down_band_range = [20]
    else:
        k_period_range = [*range(3, 31), *range(35, 101, 5)]
        d_period_range = [*range(3, 31), *range(35, 101, 5)]
        upper_band_range = [*range(60, 91, 5)]
        down_band_range = [*range(10, 41, 5)]
    for k_period in k_period_range:
        for d_period in d_period_range:
            for upper_band in upper_band_range:
                for down_band in down_band_range:
                    yield [k_period, d_period, upper_band, down_band]
