import datetime
import streamlit as st
from src.strategies import ta_indicators
from inspect import isfunction, getmembers


def create_sidebar():
    with st.sidebar.form("serial_backtester"):
        if "backtest" not in st.session_state:
            st.session_state["backtest"] = False
        strategy_name_list = [member[0] for member in getmembers(ta_indicators, isfunction)]
        backtest_button = st.form_submit_button("Backtest")
        interval_list = ['1d', '1h']
        st.selectbox("Select interval", interval_list, index=1, key="interval")
        st.write("Select strategies")
        st.session_state["strategy_list"] = []
        for strategy_name in strategy_name_list:
            st.toggle(strategy_name.replace("_", " "), value=True, key=strategy_name)
        st.date_input("Select start date 1", datetime.date(2017, 9, 1), key="start_date1")
        st.date_input("Select end date 1", datetime.date(2022, 9, 1), key="end_date1")
        st.date_input("Select start date 2", datetime.date(2022, 9, 1), key="start_date2")
        st.date_input("Select end date 2", datetime.date(2023, 9, 1), key="end_date2")
        if backtest_button:
            st.session_state["backtest"] = True
            update_strategy_list(strategy_name_list)


def update_strategy_list(strategy_name_list: list):
    strategy_list = st.session_state["strategy_list"]
    for strategy_name in strategy_name_list:
        if st.session_state[strategy_name]:
            strategy_list.append(strategy_name)
    st.session_state["strategy_list"] = strategy_list

