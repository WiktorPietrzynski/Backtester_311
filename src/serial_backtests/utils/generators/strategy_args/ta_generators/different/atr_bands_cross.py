def atr_bands_cross():
    for sma_len in [*range(3, 31), *range(35, 101, 5)]:
        for atr_len in [*range(3, 31), *range(35, 101, 5)]:
            for percent in [50, 75, 100, 125, 150, 175, 200, 250, 300, 400, 500]:
                for cross_type in ["inside", "middle"]:
                    if cross_type == "inside":
                        for exit_type in ["default", "middle", "opposite"]:
                            yield [sma_len, atr_len, percent, cross_type, exit_type]
                    elif cross_type == "middle":
                        for exit_type in ["default", "same", "opposite"]:
                            yield [sma_len, atr_len, percent, cross_type, exit_type]
