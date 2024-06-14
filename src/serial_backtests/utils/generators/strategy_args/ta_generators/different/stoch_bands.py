def stoch_bands():
    for stoch_k in [*range(5, 31), *range(40, 101, 10)]:
        # for stoch_d in range(3, 31):
        for stoch_d in range(3, 4):
            for stoch_smooth_k in range(3, 31):
                for upper_band in range(60, 91, 5):
                    for down_band in range(10, 41, 5):
                        yield [stoch_k, stoch_d, stoch_smooth_k, upper_band, down_band]
