def bollinger_bands_cross_args():
    for bb_len in range(5, 51):
        for bb_std in [1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.5, 4, 4.5, 5]:
            for cross_type in ["inside", "middle"]:
                if cross_type == "inside":
                    for exit_type in ["default", "middle", "opposite"]:
                        yield [bb_len, bb_std, cross_type, exit_type]
                elif cross_type == "middle":
                    for exit_type in ["default", "same", "opposite"]:
                        yield [bb_len, bb_std, cross_type, exit_type]
