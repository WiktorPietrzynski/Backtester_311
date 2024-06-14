from src.serial_backtests.serial_advanced_backtest import serial_advanced_backtest
import sys
from streamlit.web import cli
import warnings
warnings.filterwarnings("ignore")


def backtest():
    interval_list = ["1h"]
    # strategy_list = ["macd_cross"]
    strategy_list = ["macd_cross", "ma_cross", "stochastic"]
    # strategy_list = ["stochastic"]
    first_start_date = "2017-09-01"
    first_end_date = "2022-09-01"
    years = 5
    serial_advanced_backtest(interval_list, strategy_list, first_start_date, first_end_date, years, False, True, False)


if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "src/app/app.py"]
    sys.exit(cli.main())


