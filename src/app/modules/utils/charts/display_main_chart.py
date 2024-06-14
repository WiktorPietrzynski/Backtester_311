from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts
from pyecharts.globals import ThemeType
import pandas as pd
# from pyecharts.charts import Kline, Line, Scatter
# from pyecharts import options as opts
import numpy as np


def display_profit_chart(series):
    series = (100 * np.cumprod(1 + series / 100)) - 100
    series = pd.Series(series)
    bar_chart = (Bar()
        .add_xaxis(series.index.tolist())
        .add_yaxis("Cum profit", series.values.tolist(), label_opts=opts.LabelOpts(is_show=False))
        # .add_yaxis("商家B", [20, 10, 40, 30, 40, 50])
        .set_global_opts(

            title_opts=opts.TitleOpts(title="Cum profit"),
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(is_scale=True),
            datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100), opts.DataZoomOpts(type_="inside")]
        )
    )

    st_pyecharts(bar_chart, theme=ThemeType.DARK)

# def display_trades_chart(series: pd.Series, series2: pd.Series):
#     bar_chart = (Bar()
#         .add_xaxis(series.index.tolist())
#         .add_yaxis("trade count", series.values.tolist(), gap="0%", label_opts=opts.LabelOpts(is_show=False))
#         .add_yaxis("percent profitable", series.values.tolist(), gap="0%", label_opts=opts.LabelOpts(is_show=False))
#         .set_global_opts(
#
#             title_opts=opts.TitleOpts(title="Cum profit"),
#             xaxis_opts=opts.AxisOpts(is_scale=True),
#             yaxis_opts=opts.AxisOpts(is_scale=True),
#             datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100), opts.DataZoomOpts(type_="inside")]
#         )
#     )
#
#     st_pyecharts(bar_chart, theme=ThemeType.DARK)



# def get_chart(df: pd.DataFrame, trades: pd.DataFrame):
#     # Create a Kline chart object
#     kline_chart = Kline(init_opts=opts.InitOpts(height="500px", theme=ThemeType.DARK))
#
#     # Add x and y data to the chart object using the Pandas dataframe
#     kline_chart.add_xaxis(df['date'].tolist())
#     kline_chart.add_yaxis('OHLC', df[['open', 'close', 'low', 'high']].values.tolist())
#
#     # Set chart options
#     kline_chart.set_global_opts(
#         title_opts=opts.TitleOpts(title="OHLC Chart"),
#         xaxis_opts=opts.AxisOpts(is_scale=True),
#         yaxis_opts=opts.AxisOpts(is_scale=True),
#         datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100), opts.DataZoomOpts(type_="inside")],
#     )
#     add_trade_markers(trades, kline_chart)
#     return kline_chart
#
#
# def add_trade_markers(trade_df: pd.DataFrame, kline_chart: Kline) -> None:
#     long_trades = trade_df.loc[trade_df["side"] == "long"]
#     short_trades = trade_df.loc[trade_df["side"] == "short"]
#     long_data = split_data_part(long_trades)
#     short_data = split_data_part(short_trades)
#     big_data = split_data_part(trade_df)
#
#     kline_chart.set_series_opts(
#             markarea_opts=opts.MarkAreaOpts(is_silent=True, data=big_data)
#         )
#
#     # kline_chart.set_series_opts(
#     #         markarea_opts=opts.MarkAreaOpts(is_silent=True, data=long_data, itemstyle_opts=opts.ItemStyleOpts(color="green"))
#     #     )
#     #
#     # kline_chart.set_series_opts(
#     #         markarea_opts=opts.MarkAreaOpts(is_silent=True, data=short_data)
#     #     )
#
#
# def split_data_part(trade_df):
#     mark_area_list = []
#     for trade_id, trade in trade_df.iterrows():
#         side = trade["side"]
#         open_date = trade["open date"]
#         exit_date = trade["exit date"]
#         open_price = trade["open price"]
#         exit_price = trade["exit price"]
#         # mark_area = [
#         #     {
#         #         "xAxis": open_date,
#         #         "yAxis": open_price,
#         #     },
#         #     {
#         #         "xAxis": exit_date,
#         #         "yAxis": exit_price,
#         #     },
#         # ]
#         mark_area = opts.MarkAreaItem(
#                     x=(open_date, exit_date),
#                     y=(open_price, exit_price),
#                     label_opts=opts.LabelOpts(is_show=False),
#                     itemstyle_opts=opts.ItemStyleOpts(color="red" if side == "short" else "green", opacity=0.5))
#
#         mark_area_list.append(mark_area)
#     return mark_area_list
#
#
#
# def add_ma(df, kline_chart):
#     # Add moving average lines
#     ma5 = df['close'].rolling(window=5).mean().tolist()
#     ma10 = df['close'].rolling(window=10).mean().tolist()
#     ma20 = df['close'].rolling(window=20).mean().tolist()
#     dates = df['date'].tolist()
#
#     line_chart = Line().add_xaxis(dates)
#     line_chart.set_global_opts(
#         xaxis_opts=opts.AxisOpts(type_="category"),
#         yaxis_opts=opts.AxisOpts(type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)),
#         tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
#         title_opts=opts.TitleOpts(title="AAPL Candlestick Chart with Moving Averages"),
#     )
#     line_chart.set_series_opts(
#         label_opts=opts.LabelOpts(is_show=False),
#         linestyle_opts=opts.LineStyleOpts(width=5, opacity=0.5)
#     )
#     line_chart.add_yaxis('MA5', ma5, is_smooth=True, is_symbol_show=False)
#     line_chart.add_yaxis('MA10', ma10, is_smooth=True, is_symbol_show=False)
#     line_chart.add_yaxis('MA20', ma20, is_smooth=True, is_symbol_show=False)
#
#     # Add the Line and Scatter charts to the Kline chart using the overlap() method
#     kline_chart.overlap(line_chart)
