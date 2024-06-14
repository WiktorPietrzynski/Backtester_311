from setuptools import Extension, setup
from Cython.Build import cythonize
import numpy
import os
from shutil import rmtree


compiler_directives = {'boundscheck': "False", 'cdivision': "True", 'wraparound': "False", 'nonecheck': "False", 'language_level': "3"}

extra_compile_args = ['/Ox', '/openmp', '/arch:AVX2', "/fp:fast"]


advanced_backtest = Extension(name="advanced_backtest", sources=["src/backtests/advanced_backtest/advanced_backtest.pyx"], include_dirs=[numpy.get_include()], extra_compile_args=extra_compile_args)


serial_based_backtest = Extension(name="serial_based_backtest", sources=["src/serial_backtests/serial_based_backtest/serial_based_backtest.pyx"], include_dirs=[numpy.get_include()], extra_compile_args=extra_compile_args)


serial_advanced_backtest = Extension(name="serial_advanced_backtest", sources=["src/serial_backtests/serial_advanced_backtest/serial_advanced_backtest.pyx"], include_dirs=[numpy.get_include()], extra_compile_args=extra_compile_args)


extension_list = [advanced_backtest, serial_based_backtest, serial_advanced_backtest]
annotate = False
# annotate = True

for extension in extension_list:
    build_dir = os.path.split(extension.sources[0])[0]
    setup(name=extension.name,
          ext_modules=cythonize([extension], compiler_directives=compiler_directives, language_level=3, annotate=annotate),
          script_args=['build_ext', '-b', build_dir])

if annotate is False:
    if os.path.exists("build"):
        rmtree("build")
