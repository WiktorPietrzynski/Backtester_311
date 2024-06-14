from . import ta_generators
from inspect import getmembers, isfunction


def get_strategy_args(strategy_name: str, simplify: bool = False) -> list:
    strategy_generators = dict(getmembers(ta_generators, isfunction))
    generator_name = strategy_name.replace(" ", "_")
    strategy_generator_name = f"{generator_name}_args"
    strategy_args_list = strategy_generators[strategy_generator_name](simplify)
    return strategy_args_list