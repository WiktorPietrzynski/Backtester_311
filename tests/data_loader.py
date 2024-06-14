from src.data_loader import get_data
from src.data_loader import get_results

def test_data_loader():
    interval_list = ["1h"]
    for interval in interval_list:
        # df = get_data(interval=interval, start_date="2024-01-01", end_date="2024-01-31")
        df = get_data(interval=interval, start_date="2017-09-01", end_date="2020-09-01")
        print("interval:", interval)
        # print(df[:2].to_markdown())
        print(df.to_markdown())

def test_results_loader():
    interval_list = ["1h"]
    strategy_list = ["macd cross"]
    start_date = "2017-09-01"
    end_date = "2022-09-01"
    for interval in interval_list:
        df = get_results(interval, start_date, end_date, strategy_list)
        print(df.to_markdown())

if __name__ == "__main__":
    test_data_loader()
    # test_results_loader()
    print("Done!")
