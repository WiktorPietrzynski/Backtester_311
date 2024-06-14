def rsi_bands_trend_args():
    for rsi_len in [*range(5, 51), *range(55, 101, 5)]:
        for upper_band in range(50, 91, 5):
            for down_band in range(10, 51, 5):
                yield [rsi_len, upper_band, down_band]
