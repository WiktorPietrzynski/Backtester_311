from src.serial_backtests.utils.generators import ta_generators
from inspect import getmembers, isfunction


if __name__ == "__main__":

    def timings(test_type: str, strategy_count: int, test_time: float):
        if test_type == "single":
            time_s = 1000 * strategy_count * test_time
        else:
            time_s = strategy_count / 1000 * test_time
        time_m = time_s / 60
        time_h = time_m / 60
        return f"{round(time_h, 2)}h", f"{round(time_m, 2)}m", f"{round(time_s, 2)}s"

    def generator_counts(strategy_name: str = None):
        def pretty_numbers(number: float):
            number_str = str(int(number))
            number_str = number_str[::-1]
            new_number_str = ""
            for i in range(0, len(number_str), 3):
                new_number_str += f"{number_str[i:i+3]} "
            return new_number_str[::-1][1:]

        strategy_generators = dict(getmembers(ta_generators, isfunction))
        if strategy_name:
            print(strategy_name)
            count = len(list(strategy_generators[strategy_name]()))
            print(pretty_numbers(count))
            print("")
            strategy_count = count
        else:
            strategy_count = 0
            for name, function in strategy_generators.items():
                print(name)
                count = len(list(function()))
                print(pretty_numbers(count))
                print("")
                strategy_count += count
        print("stc:", pretty_numbers(strategy_count))
        print("btc:", pretty_numbers(1000 * strategy_count))
        s1d = timings("single", strategy_count, 0.000282099936157465)
        s1h = timings("single", strategy_count, 0.002170500112697482)
        print("single - 1d:", *s1d)
        print("single - 1h:", *s1h)
        p1d = timings("parallel", strategy_count, 7.020496299955994)
        p1h = timings("parallel", strategy_count, 141.30598030006513)
        print("parallel - 1d:", *p1d)
        print("parallel - 1d:", *p1h)
    generator_counts()
    # generator_counts("bollinger_bands_cross")
