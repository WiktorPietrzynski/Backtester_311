from pandas import DataFrame
import streamlit as st


def create_selectable_df(df: DataFrame, strategy_name: str, column_id: int = 0):
    df_with_selections = df.copy()
    df_with_selections.insert(0, f"Select", False)
    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=False,
        column_config={f"Select": st.column_config.CheckboxColumn(required=True)},
        disabled=df.columns,
        key=f"dff_{strategy_name}_{column_id}",
        height=200,
    )
    selected_row = edited_df[edited_df[f"Select"]]
    st.session_state[f"selected_row_{strategy_name}_{column_id}"] = selected_row.drop(f"Select", axis=1)