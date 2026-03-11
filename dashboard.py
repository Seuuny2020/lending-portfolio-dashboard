import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("test")
st.write("hello world")

fig = px.bar(x=["A", "B", "C"], y=[1, 2, 3])
st.plotly_chart(fig)
