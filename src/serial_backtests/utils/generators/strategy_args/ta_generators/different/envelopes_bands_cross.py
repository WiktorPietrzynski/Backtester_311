def envelopes_bands_cross():
    for ma_type in ["sma", "ema"]:
        for ma_len in [*range(3, 51), *range(55, 101, 5)]:
            for percent in [*range(10, 26), 30, 35, 40, 45, 50]:
                for cross_type in ["inside", "middle"]:
                    if cross_type == "inside":
                        for exit_type in ["default", "middle", "opposite"]:
                            yield [ma_type, ma_len, percent, cross_type, exit_type]
                    elif cross_type == "middle":
                        for exit_type in ["default", "same", "opposite"]:
                            yield [ma_type, ma_len, percent, cross_type, exit_type]
