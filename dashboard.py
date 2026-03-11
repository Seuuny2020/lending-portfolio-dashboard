import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Lending Portfolio Dashboard", page_icon="📊", layout="wide")

st.title("📊 Consumer Lending Portfolio Dashboard")
st.caption("Simulated portfolio · Built by Seun Ismail Adeleke · Credit Data Analyst")
st.markdown("---")

@st.cache_data
def load_data():
    portfolio = pd.read_csv("data/portfolio_metrics.csv", parse_dates=["month"])
    risk_bands = pd.read_csv("data/risk_bands.csv")
    regional   = pd.read_csv("data/regional.csv")
    return portfolio, risk_bands, regional

portfolio, risk_bands, regional = load_data()

latest = portfolio.iloc[-1]
prev   = portfolio.iloc[-2]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Approval Rate",   f"{latest.approval_rate:.1f}%",   f"{latest.approval_rate - prev.approval_rate:.1f}pp")
col2.metric("30d Delinquency", f"{latest.delinquency_30d:.2f}%", f"{latest.delinquency_30d - prev.delinquency_30d:.2f}pp")
col3.metric("Net Loss Rate",   f"{latest.net_loss_rate:.2f}%",   f"{latest.net_loss_rate - prev.net_loss_rate:.2f}pp")
col4.metric("NPS Score",       f"{latest.nps_score:.0f}",        f"{latest.nps_score - prev.nps_score:.1f}")

st.markdown("---")
col_l, col_r = st.columns(2)

with col_l:
    fig = px.line(portfolio, x="month", y=["delinquency_30d", "net_loss_rate"],
                  title="Risk Metrics Over Time",
                  labels={"value": "%", "variable": "Metric", "month": ""})
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    fig2 = px.bar(portfolio, x="month", y="total_originated",
                  title="Monthly Origination Volume",
                  labels={"total_originated": "£ Originated", "month": ""})
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
col_a, col_b = st.columns(2)

with col_a:
    fig3 = px.bar(risk_bands, x="risk_band", y="default_rate",
                  color="risk_band", text="default_rate",
                  title="Default Rate by Risk Band",
                  color_discrete_map={"A":"#48bb78","B":"#ecc94b","C":"#ed8936","D":"#fc8181"})
    fig3.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    st.plotly_chart(fig3, use_container_width=True)

with col_b:
    fig4 = px.scatter(regional, x="loan_volume", y="default_rate",
                      size="avg_loan", color="region", text="region",
                      title="Regional: Loan Volume vs Default Rate")
    st.plotly_chart(fig4, use_container_width=True)

with st.expander("📋 View Raw Data"):
    st.dataframe(portfolio, use_container_width=True)

st.markdown("---")
st.caption("Seun Ismail Adeleke · Credit Data Analyst · seunismailadeleke@gmail.com")
