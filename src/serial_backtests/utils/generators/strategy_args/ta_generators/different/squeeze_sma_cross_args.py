def squeeze_sma_cross_args():
    sma_range = [0, *range(5, 101), *range(105, 201, 5)]
    for sma in sma_range:
        for kc_len in range(5, 201):
            yield [kc_len, sma]
