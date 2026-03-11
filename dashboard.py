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
    portfolio = pd.read_csv("portfolio_metrics.csv", parse_dates=["month"])
    risk_bands = pd.read_csv("risk_bands.csv")
    regional   = pd.read_csv("regional.csv")
    return portfolio, risk_bands, regional
portfolio, risk_bands, regional = load_data()
# ── Sidebar ──────────────────────────────────────────────────
st.sidebar.title("Dashboard Controls")
st.sidebar.markdown("---")
selected_metrics = st.sidebar.multiselect(
    "Risk Metrics to Display",
    ["delinquency_30d", "delinquency_90d", "net_loss_rate", "approval_rate"],
    default=["delinquency_30d", "net_loss_rate"]
)
st.sidebar.markdown("---")
st.sidebar.markdown("""
**Built by**  
Seun Ismail Adeleke  
Credit Data Analyst  
[LinkedIn](https://www.linkedin.com/in/ismail-adeleke-b77556109)  
[GitHub](https://github.com/Seuuny2020)
""")
# ── KPI Cards ────────────────────────────────────────────────
latest = portfolio.iloc[-1]
prev   = portfolio.iloc[-2]
st.markdown("### Portfolio KPIs — Latest Month")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Approval Rate",
            f"{latest.approval_rate:.1f}%",
            f"{latest.approval_rate - prev.approval_rate:.1f}pp")
col2.metric("30d Delinquency",
            f"{latest.delinquency_30d:.2f}%",
            f"{latest.delinquency_30d - prev.delinquency_30d:.2f}pp",
            delta_color="inverse")
col3.metric("90d Delinquency",
            f"{latest.delinquency_90d:.2f}%",
            f"{latest.delinquency_90d - prev.delinquency_90d:.2f}pp",
            delta_color="inverse")
col4.metric("Net Loss Rate",
            f"{latest.net_loss_rate:.2f}%",
            f"{latest.net_loss_rate - prev.net_loss_rate:.2f}pp",
            delta_color="inverse")
col5.metric("NPS Score",
            f"{latest.nps_score:.0f}",
            f"{latest.nps_score - prev.nps_score:.1f}")
st.markdown("---")
# ── Trend Charts ─────────────────────────────────────────────
st.markdown("### Portfolio Trends")
col_l, col_r = st.columns(2)
with col_l:
    if selected_metrics:
        fig = px.line(
            portfolio, x="month", y=selected_metrics,
            title="Risk Metrics Over Time",
            labels={"value": "%", "variable": "Metric", "month": ""},
            markers=True
        )
        fig.update_layout(legend_title="")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Select at least one metric from the sidebar")
with col_r:
    fig2 = px.bar(
        portfolio, x="month", y="total_originated",
        title="Monthly Origination Volume (£)",
        labels={"total_originated": "£ Originated", "month": ""},
        color_discrete_sequence=["#4299e1"]
    )
    st.plotly_chart(fig2, use_container_width=True)
st.markdown("---")
# ── Risk Band & Regional ─────────────────────────────────────
st.markdown("### Risk Segmentation & Regional Breakdown")
col_a, col_b = st.columns(2)
with col_a:
    fig3 = px.bar(
        risk_bands, x="risk_band", y="default_rate",
        color="risk_band", text="default_rate",
        title="Default Rate by Risk Band (%)",
        labels={"default_rate": "Default Rate (%)", "risk_band": "Risk Band"},
        color_discrete_map={"A":"#48bb78","B":"#ecc94b","C":"#ed8936","D":"#fc8181"}
    )
    fig3.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig3.update_layout(showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)
with col_b:
    fig4 = px.scatter(
        regional, x="loan_volume", y="default_rate",
        size="avg_loan", color="region", text="region",
        title="Regional: Loan Volume vs Default Rate",
        labels={"loan_volume": "Total Loan Volume (£)", "default_rate": "Default Rate (%)"}
    )
    fig4.update_traces(textposition="top center")
    fig4.update_layout(showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)
st.markdown("---")
# ── NPS Trend ────────────────────────────────────────────────
st.markdown("### NPS Score Trend")
fig5 = px.line(
    portfolio, x="month", y="nps_score",
    title="NPS Score Over Time",
    labels={"nps_score": "NPS Score", "month": ""},
    markers=True, color_discrete_sequence=["#48bb78"]
)
fig5.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Neutral")
st.plotly_chart(fig5, use_container_width=True)
st.markdown("---")
# ── Raw Data ─────────────────────────────────────────────────
with st.expander("📋 View Raw Portfolio Data"):
    st.dataframe(portfolio, use_container_width=True)
st.markdown("---")
st.caption("Seun Ismail Adeleke · Credit Data Analyst · seunismailadeleke@gmail.com")
