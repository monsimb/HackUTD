import streamlit as st
import pandas as pd
import numpy as np

st.title('Graph')
chart_data = pd.DataFrame(
    np.random.randn(20, 3), columns=["Monthly Payment", "Current", "Reccomended"]
)

st.line_chart(
    chart_data,
    x="Monthly Payment",
    y=["Current", "Reccomended"],
    color=["#8AD47E", "#F5A3B6"]  # Optional
)