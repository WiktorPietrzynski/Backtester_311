import streamlit as st
from src.app.modules.utils.display_charts import display_charts
from src.app.modules.utils.create_selectable_df import create_selectable_df

def display_results():
    if "backtest" in st.session_state and st.session_state["backtest"]:
        column_id_1 = 1
        column_id_2 = 2
        col1, col2 = st.columns(2)
        # col1, col2, col3 = st.columns(3)
        for strategy_name in ["ma_cross", "macd_cross", "stochastic"]:
            with st.container():
                with col1:
                    if f"df_{strategy_name}_{column_id_1}" in st.session_state:
                        st.write(strategy_name)
                        display_editable_df(strategy_name, column_id_1)
                        # display_best_results(strategy_name, column_id_1)
                        # display_compare_results(strategy_name, column_id_1)
                with col2:
                    if f"df_{strategy_name}_{column_id_2}" in st.session_state:
                        st.write(strategy_name)
                        display_editable_df(strategy_name, column_id_2)
                        # display_best_results(strategy_name, column_id_2)
                        # display_compare_results(strategy_name, column_id_2)
                # with col3:
                #     df1 = st.session_state[f"df_{strategy_name}_{column_id_1}"]
                #     df2 = st.session_state[f"df_{strategy_name}_{column_id_2}"]
                #     profit_to_drawdown = df1["average trade"]/df1["drawdown"]
                #     st.write(strategy_name)
                #     st.dataframe(profit_to_drawdown, height=200)


def display_editable_df(strategy_name: str, column_id: int):
    if f"df_{strategy_name}_{column_id}" in st.session_state:
        df = st.session_state[f"df_{strategy_name}_{column_id}"]
        # st.dataframe(df.transpose())
        create_selectable_df(df, strategy_name, column_id)
        if f"selected_row_{strategy_name}_{column_id}" in st.session_state and len(st.session_state[f"selected_row_{strategy_name}_{column_id}"]) == 1:
            backtest = st.session_state[f"selected_row_{strategy_name}_{column_id}"].dropna(axis=1).values.tolist()[0]
            display_charts(backtest, column_id)

# def display_best_results(strategy_name: str, column_id: int):
#     if f"df_{strategy_name}_{column_id}" in st.session_state:
#         df = st.session_state[f"df_{strategy_name}_1"]
#         if column_id == 2:
#             st.dataframe(st.session_state[f"df_{strategy_name}_{column_id}"])
#         else:
#             st.dataframe(df)
#         for column_name in ["profit", "net_profit", "net_profit_to_drawdown", "sortino ratio", "cagr", "mar_ratio"]:
#             best_result = df.sort_values(column_name, ascending=False).head(1).dropna(axis=1)
#             if column_id == 2:
#                 df2 = st.session_state[f"df_{strategy_name}_2"]
#                 index1 = best_result.index
#                 best_result = df2.loc[index1]
#             st.write(column_name)
#             st.dataframe(best_result)
#             backtest = best_result.values.tolist()[0]
#             display_charts(backtest, column_id)

# def display_compare_results(strategy_name: str, column_id: int):
#     if f"df_{strategy_name}_{column_id}" in st.session_state:
#         df1 = st.session_state[f"df_{strategy_name}_1"]
#         df2 = st.session_state[f"df_{strategy_name}_2"]
#         highest_profit = 0.0
#         lowest_drawdown = 50.0
#         top1 = ""
#         top2 = ""
#         for column_name in ["profit", "net_profit", "net_profit_to_drawdown",
#                             "sortino ratio", "rar", "cagr", "mar_ratio"]:
#             best_result1 = df1.sort_values(column_name, ascending=False).head(1).dropna(axis=1)
#             best_result2 = df2.loc[best_result1.index]
#             profit1 = best_result1["profit"].values[0]
#             profit2 = best_result2["profit"].values[0]
#             drawdown1 = best_result1["drawdown"].values[0]
#             drawdown2 = best_result2["drawdown"].values[0]
#             if profit2 > highest_profit:
#                 highest_profit = profit2
#                 top1 = f"profit: {column_name}: {profit2}"
#             if drawdown2 < lowest_drawdown:
#                 lowest_drawdown = drawdown2
#                 top2 = f"drawdown: {column_name}: {drawdown2}"
#             if column_id == 1:
#                 st.write(column_name)
#                 st.dataframe(best_result1)
#                 st.dataframe(best_result2)
#         if column_id == 2:
#             st.write(top1)
#             st.write(top2)