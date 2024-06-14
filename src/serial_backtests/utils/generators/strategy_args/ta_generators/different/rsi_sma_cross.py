def rsi_sma_cross():
    # sma_range = [*range(8, 51), *range(55, 101, 5)]
    sma_range = [*range(8, 101)]
    # rsi_range = [*range(5, 51), *range(55, 101, 5)]
    rsi_range = [*range(5, 101)]
    for rsi_len in rsi_range:
        for sma_len in sma_range:
            yield [rsi_len, sma_len]
