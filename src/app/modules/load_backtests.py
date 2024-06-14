import streamlit as st
from pandas import DataFrame
from glob import glob
from os import path
from pathlib import Path
from src.data_loader.get_results import get_results
from src.serial_backtests.serial_advanced_backtest import serial_advanced_backtest
from src.serial_backtests.serial_based_backtest import serial_based_backtest


def load_backtests():
    if "backtest" in st.session_state and st.session_state["backtest"]:
        interval = st.session_state['interval']
        start_date1 = str(st.session_state['start_date1'])
        end_date1 = str(st.session_state['end_date1'])
        start_date2 = str(st.session_state['start_date2'])
        end_date2 = str(st.session_state['end_date2'])
        for strategy_name in ["ma_cross", "macd_cross", "stochastic"]:
            # base backtest
            df1 = get_base_backtest(interval, start_date1, end_date1, [strategy_name])
            st.session_state[f"df_{strategy_name}_1"] = df1

            # selected backtest
            df2 = get_selected_backtest(interval, start_date2, end_date2, [strategy_name], df1)
            st.session_state[f"df_{strategy_name}_2"] = df2



def get_base_backtest(interval: str, start_date: str, end_date: str, strategy_list: list) -> DataFrame:
    df = get_results(interval, start_date, end_date, strategy_list)
    if df.empty:
        # st.write("No results found")
        # exit("No results found")
        serial_advanced_backtest([interval], strategy_list, start_date, end_date, 5, True, False)
        df = get_results(interval, start_date, end_date, strategy_list)
    df = filter_base_backtest(df, 25.0)
    return df

def filter_base_backtest(df: DataFrame, max_drawdown: float = 50.0) -> DataFrame:
    # print("base:", len(df))
    df = df[df["drawdown"] < max_drawdown]
    df = df[df["trade count"] > 20]
    # print("filtered:", len(df))
    sort_by_list = ["profit", "cagr", "mar_ratio", "average trade"]
    index_list = [find_index(df, sort_by) for sort_by in sort_by_list]
    index_list = list(set(index_list))
    df = df.loc[index_list].reset_index(drop=True)
    return df

def find_index(df: DataFrame, sort_by: str) -> int:
    return df.sort_values(sort_by, ascending=False).head(1).index.tolist()[0]



def get_selected_backtest(interval: str, start_date: str, end_date: str, strategy_list: list, base_df: DataFrame) -> DataFrame:
    df = get_results(interval, start_date, f"{end_date}_filtered", strategy_list, False)
    if df.empty:
        # st.write("No results found")
        # exit("No results found")
        # print("No results found") 
        serial_based_backtest(interval, strategy_list, start_date, end_date, base_df, 1, False)
        df = get_results(interval, start_date, f"{end_date}_filtered", strategy_list, False)
    return df.round(2)

