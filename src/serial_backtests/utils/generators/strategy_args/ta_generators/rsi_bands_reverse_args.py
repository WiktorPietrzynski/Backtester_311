def rsi_bands_reverse_args(simplified: bool = False):
    if simplified:
        rsi_len_range = [*range(5, 101, 5)]
        upper_band_range = [70, 80, 90]
        down_band_range = [10, 20, 30]
    else:
        rsi_len_range = [*range(5, 31), *range(55, 101, 5)]
        upper_band_range = [*range(60, 91, 1)]
        down_band_range = [*range(10, 41, 1)]
    for rsi_len in rsi_len_range :
        for upper_band in upper_band_range:
            for down_band in down_band_range:
                yield [rsi_len, upper_band, down_band]
