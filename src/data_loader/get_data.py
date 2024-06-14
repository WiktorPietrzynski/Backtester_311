from os import path
import requests
from pandas import DataFrame, to_datetime, read_feather, DatetimeIndex, concat, Timestamp


def get_data(symbol: str = "BTCUSDT", interval: str = "1d", start_date: str = "2017-01-01", end_date: str = "2025-01-01", update_data: bool = False) -> DataFrame:
    try:
        main_df = _get_saved_data(symbol, interval)
        if update_data:
            main_df = _get_updated_data(symbol, interval, main_df)
    except FileNotFoundError:
        start_timestamp = str((Timestamp(start_date).timestamp() - 60) * 1000).split(".")[0]
        main_df = _binance_klines(symbol, interval, start_timestamp)
        # exit("file error")
    main_df.reset_index(drop=True, inplace=True)
    _save_data(symbol, interval, main_df)
    main_df = _data_timeframe(start_date, end_date, main_df)
    main_df = _data_optimization(main_df).iloc[:-1, :]
    return main_df


def _data_optimization(df: DataFrame) -> DataFrame:
    df['date'] = to_datetime(df['timestamp'], unit='ms')
    df = df[["date", "timestamp", "open", 'high', 'low', 'close', 'volume']]
    df[['open', 'high', 'low', 'close', 'volume']] = df[
        ['open', 'high', 'low', 'close', 'volume']].astype(
        float).round(2)
    df.drop_duplicates(subset="timestamp", keep="first", inplace=True)
    df = df.set_index(DatetimeIndex(df['date']))
    return df


def _get_klines(symbol: str, interval: str, start_time: str) -> DataFrame:
    url = f"https://api1.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=1000&startTime={start_time}"
    response = requests.get(url)
    response.raise_for_status()
    json_df = DataFrame(response.json())
    if json_df.empty:
        return json_df
    else:
        df = json_df.iloc[:, :6]
        df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        return df


def _binance_klines(symbol: str = "BTCUSDT", interval: str = "1d", start_time: str = "1484000000000") -> DataFrame:
    main_df = _get_klines(symbol, interval, start_time)
    i = 1
    while True:
        i = i + 1
        new_df = _get_klines(symbol, interval, main_df['timestamp'].iloc[-1] + 1)
        if new_df.empty:
            break
        main_df = concat([main_df, new_df], ignore_index=True)
    main_df = _data_optimization(main_df)
    print("data updated")
    return main_df


def _get_saved_data(symbol: str, interval: str) -> DataFrame:
    absolute_path = path.dirname(__file__)
    file_name = f"{absolute_path}/historical_data/{symbol}/{symbol}_{interval}.feather"
    saved_df = read_feather(file_name)
    return saved_df


def _get_updated_data(symbol: str, interval: str, main_df: DataFrame) -> DataFrame:
    last_timestamp = main_df.iloc[-1, 1]
    latest_df = _binance_klines(symbol, interval, start_time=last_timestamp)
    updated_df = concat([main_df, latest_df])
    updated_df = updated_df.drop_duplicates(subset="timestamp", keep="first")
    return updated_df


def _save_data(symbol: str, interval: str, df: DataFrame) -> None:
    absolute_path = path.dirname(__file__)
    file_name = f"{absolute_path}/historical_data/{symbol}/{symbol}_{interval}.feather"
    df.to_feather(file_name)


def _data_timeframe(start_date: str, end_date: str, df: DataFrame) -> DataFrame:
    start_date = to_datetime(start_date, dayfirst=False)
    end_date = to_datetime(end_date, dayfirst=False)
    main_df = df[to_datetime(df['date']).between(start_date, end_date)]
    return main_df
