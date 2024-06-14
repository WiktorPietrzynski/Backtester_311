import streamlit as st
from src.backtests.advanced_backtest.advanced_backtest import advanced_backtest
from src.data_loader import get_data
from src.strategies.strategy import strategy_select
import numpy as np
from os import path
from pandas import DataFrame, Series, concat, ExcelWriter
# from src.app.modules.charts.display_main_chart import display_profit_chart
import openpyxl
from openpyxl.chart import BarChart, Reference, AreaChart

def display_charts(backtest_data: list, column_id: int = 1):
    if column_id == 1:
        years = 5
        start_date = st.session_state['start_date1']
        end_date = st.session_state['end_date1']
    else:
        years = 1
        start_date = st.session_state['start_date2']
        end_date = st.session_state['end_date2']
        # end_date = "2024-05-13"
        # start_date = "2023-01-03"
        # end_date = "2024-04-01"
        # years = 5
        # start_date = "2017-12-01"
        # end_date = "2022-12-01"
    backtest_settings = backtest_data[17:22]
    symbol = backtest_data[22]
    interval = backtest_data[23]
    strategy_name = backtest_data[24]
    strategy_args = backtest_data[25:]
    df = get_data(symbol, interval, start_date, end_date).copy()
    candles_array = strategy_select(strategy_name, strategy_args, df).copy()
    if strategy_name == "stochastic":
        # print(backtest_settings)
        backtest_settings = [3.0, 0.5, 2.0, 15.0, 0.01]
        # print(backtest_settings)
    trade_list = advanced_backtest(candles_array, backtest_settings, False, years)
    returns_array = np.array(trade_list)
    # returns_array = remove_outliners(returns_array)
    st.write("strategy", strategy_name)
    st.write(start_date, "-", end_date)
    display_trades(returns_array)
    # display_profit_chart(returns_array)
    display_cum_profit(returns_array)
    display_drawdown(returns_array)
    # save_excel(returns_array, strategy_name, start_date, end_date)
    # make_summary(returns_array.tolist(), years)

def display_trades(returns_array):
    st.write("returns")
    st.bar_chart(returns_array)
    # st.write(len(returns_array))
    # st.dataframe(DataFrame(returns_array))

def display_cum_profit(returns_array):
    cum_profit_array = (100 * np.cumprod(1 + returns_array / 100)) - 100
    num = pretty_numbers(cum_profit_array[-1])
    st.write(f"cumulative profit {num} %")
    st.bar_chart(cum_profit_array, color=(0, 220, 0, 0.8))

def display_drawdown(returns_array):
    cum_profit_array = 100 * np.cumprod(1 + returns_array / 100)
    running_max_array = np.maximum.accumulate(cum_profit_array)
    drawdown_array = 100 - (running_max_array - cum_profit_array) / running_max_array * 100
    st.write("drawdown", round(100 - drawdown_array.min(), 2), "%")
    # st.area_chart(drawdown_array, color=(255, 0, 0, 0.8))
    st.bar_chart(drawdown_array, color=(255, 0, 0, 0.8))


def remove_outliners(returns_array):
    # top_threshold = np.percentile(returns_array, 90)
    # bottom_threshold = np.percentile(returns_array, 5)
    # returns_array = returns_array[(returns_array <= top_threshold) & (returns_array >= bottom_threshold)]
    # returns_array = returns_array[(returns_array <= top_threshold)]
    return returns_array

def pretty_numbers(number: float) -> str:
    number_str = str(round(number, 2))
    number_str_list = number_str.split(".")
    number_inverse = number_str_list[0][::-1]
    number_str = " ".join([number_inverse[i:i + 3] for i in range(0, len(number_inverse), 3)])[::-1]
    return f"{number_str}.{number_str_list[1]}"

def save_excel(returns_array, strategy_name, start_date, end_date):
    trades_df = DataFrame(returns_array)
    cum_profit_df = DataFrame((100 * np.cumprod(1 + returns_array / 100)) - 100)
    cum_profit_array = 100 * np.cumprod(1 + returns_array / 100)
    running_max_array = np.maximum.accumulate(cum_profit_array)
    drawdown_array = 100 - (running_max_array - cum_profit_array) / running_max_array * 100

    create_excel_charts(returns_array, cum_profit_array - 100, drawdown_array, strategy_name, start_date, end_date)

def create_excel_charts(returns_array, cum_profit_array, drawdown_array, strategy_name, start_date, end_date):
    # Call a Workbook() function of openpyxl
    # to create a new blank Workbook object
    wb = openpyxl.Workbook()
    # Get workbook active sheet
    # from the active attribute.
    sheet = wb.active
    returns_list = returns_array.tolist()
    cum_profit_list = cum_profit_array.tolist()
    drawdown_list = drawdown_array.tolist()
    max_row = len(returns_list)
    # write o to 9 in 1st column of the active sheet
    for row in zip(returns_list, cum_profit_list, drawdown_list):
        sheet.append(row)

    # create data for plotting
    returns = Reference(sheet, min_col=1, min_row=1, max_col=1, max_row=max_row)
    profits = Reference(sheet, min_col=2, min_row=1, max_col=2, max_row=max_row)
    drawdowns = Reference(sheet, min_col=3, min_row=1, max_col=3, max_row=max_row)
    for i, values in enumerate([returns, profits, drawdowns]):
        if i == 0:
            chart = BarChart()
        else:
            chart = AreaChart()
        # adding data to the Bar chart object
        chart.add_data(values)
        chart.type = "col"
        # set the title of the chart
        # chart.title = " BAR-CHART "
        if i == 0:
            x_axis_tittle = "Numer transakcji"
            y_axis_tittle = "Zwrot z transakcji (w %)"
            bar_color = "89CFF0"
        elif i == 1:
            x_axis_tittle = "Numer transakcji"
            y_axis_tittle = "Zysk całkowity (w %)"
            bar_color = "008000"
        elif i == 2:
            x_axis_tittle = "Numer transakcji"
            y_axis_tittle = "Wielkość kapitału względem najwyższego poziomu (w %)"
            bar_color = "FF0000"
        else:
            exit("error")
        # set the title of the x-axis
        chart.x_axis.title = x_axis_tittle
        # set the title of the y-axis
        chart.y_axis.title = y_axis_tittle
        chart.legend = None

        s = chart.series[0]
        # s.graphicalProperties.line.solidFill = "00000"
        s.graphicalProperties.solidFill = bar_color
        if i == 0:
            chart.x_axis.tickLblPos = "low"
            # chart.x_axis.tickLblSkip = 3  # whatever you like
        elif i == 1:
            chart.x_axis.tickLblPos = "low"
            s.invertIfNegative = True
            s.InvertColor = "FF0000"
            max_profit = max(cum_profit_list)
            min_profit = min(cum_profit_list)
            if max_profit > 15000:
                chart.y_axis.scaling.max = 20000
            elif max_profit > 9000:
                chart.y_axis.scaling.max = 10000
            elif max_profit > 100:
                chart.y_axis.scaling.max = 500
            else:
                chart.y_axis.scaling.max = 100
            if str(end_date) != "2023-09-01":
                chart.y_axis.scaling.min = 0
            else:
                chart.y_axis.scaling.min = -10
            # chart.y_axis.scaling.min = 0
            # chart.y_axis.scaling.max = 20000
        elif i == 2:
            chart.y_axis.scaling.max = 100
            chart.y_axis.scaling.min = 0
        chart.x_axis.majorGridlines = None
        chart.y_axis.majorGridlines = None

        # add chart to the sheet
        # the top-left corner of a chart
        # is anchored to cell E2 .
        sheet.add_chart(chart, "E2")
        # sheet.sheet_view.showGridLines = False

        # save the file
        src_path = f"{path.dirname(path.dirname(path.dirname(path.dirname(path.dirname(path.dirname(path.dirname(__file__)))))))}/desktop"
        file_name = f"{strategy_name}_{start_date}_{end_date}"
        wb.save(f"{src_path}/{file_name}.xlsx")

