def willr_bands():
    for willr_len in [*range(5, 31), *range(40, 201, 5)]:
        for upper_band in range(-10, -36, -1):
            for down_band in range(-65, -91, -1):
                yield [willr_len, upper_band, down_band]
