import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Lending Portfolio Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .metric-card {
        background: #1a1f2e;
        border: 1px solid #2d3748;
        border-radius: 8px;
        padding: 16px 20px;
        margin: 4px 0;
    }
    .metric-label {
        font-size: 11px;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #e2e8f0;
    }
    .metric-delta-up   { font-size: 12px; color: #48bb78; }
    .metric-delta-down { font-size: 12px; color: #fc8181; }
    .section-title {
        font-size: 13px;
        color: #4299e1;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 12px;
        border-bottom: 1px solid #2d3748;
        padding-bottom: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ── Load data ────────────────────────────────────────────────
@st.cache_data
def load_data():
    portfolio = pd.read_csv("data/portfolio_metrics.csv", parse_dates=["month"])
    risk_bands = pd.read_csv("data/risk_bands.csv")
    regional   = pd.read_csv("data/regional.csv")
    return portfolio, risk_bands, regional

portfolio, risk_bands, regional = load_data()

# ── Sidebar filters ──────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/fluency/96/combo-chart.png", width=60)
st.sidebar.title("Dashboard Controls")
st.sidebar.markdown("---")

date_range = st.sidebar.select_slider(
    "Date Range",
    options=portfolio["month"].dt.strftime("%b %Y").tolist(),
    value=(
        portfolio["month"].dt.strftime("%b %Y").tolist()[0],
        portfolio["month"].dt.strftime("%b %Y").tolist()[-1]
    )
)

selected_metrics = st.sidebar.multiselect(
    "Trend Metrics to Display",
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

# ── Filter data ──────────────────────────────────────────────
start_idx = portfolio["month"].dt.strftime("%b %Y").tolist().index(date_range[0])
end_idx   = portfolio["month"].dt.strftime("%b %Y").tolist().index(date_range[1])
filtered  = portfolio.iloc[start_idx:end_idx+1]

# ── Header ───────────────────────────────────────────────────
st.title("📊 Consumer Lending Portfolio Dashboard")
st.caption("Simulated portfolio · Built by Seun Ismail Adeleke · Credit Data Analyst")
st.markdown("---")

# ── KPI Row ──────────────────────────────────────────────────
st.markdown('<div class="section-title">// Portfolio KPIs — Latest Month</div>',
            unsafe_allow_html=True)

latest  = filtered.iloc[-1]
prev    = filtered.iloc[-2] if len(filtered) > 1 else latest

col1, col2, col3, col4, col5 = st.columns(5)

def delta_color(val, positive_is_good=True):
    if positive_is_good:
        return "metric-delta-up" if val >= 0 else "metric-delta-down"
    else:
        return "metric-delta-up" if val <= 0 else "metric-delta-down"

def kpi_card(col, label, value, delta, positive_is_good=True):
    arrow = "↑" if delta >= 0 else "↓"
    css   = delta_color(delta, positive_is_good)
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="{css}">{arrow} {abs(delta):.1f} MoM</div>
    </div>
    """, unsafe_allow_html=True)

kpi_card(col1, "Approval Rate",
         f"{latest.approval_rate:.1f}%",
         latest.approval_rate - prev.approval_rate,
         positive_is_good=True)

kpi_card(col2, "30d Delinquency",
         f"{latest.delinquency_30d:.2f}%",
         latest.delinquency_30d - prev.delinquency_30d,
         positive_is_good=False)

kpi_card(col3, "90d Delinquency",
         f"{latest.delinquency_90d:.2f}%",
         latest.delinquency_90d - prev.delinquency_90d,
         positive_is_good=False)

kpi_card(col4, "Net Loss Rate",
         f"{latest.net_loss_rate:.2f}%",
         latest.net_loss_rate - prev.net_loss_rate,
         positive_is_good=False)

kpi_card(col5, "NPS Score",
         f"{latest.nps_score:.0f}",
         latest.nps_score - prev.nps_score,
         positive_is_good=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Trend Charts ─────────────────────────────────────────────
st.markdown('<div class="section-title">// Portfolio Trend Analysis</div>',
            unsafe_allow_html=True)

col_left, col_right = st.columns(2)

with col_left:
    if selected_metrics:
        fig = px.line(
            filtered, x="month", y=selected_metrics,
            title="Risk Metrics Over Time",
            labels={"value": "%", "variable": "Metric", "month": ""},
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(
            plot_bgcolor="#1a1f2e", paper_bgcolor="#1a1f2e",
            font_color="#e2e8f0", legend_title="",
            title_font_size=13,
            margin=dict(t=40, b=20, l=20, r=20)
        )
        fig.update_xaxes(gridcolor="#2d3748")
        fig.update_yaxes(gridcolor="#2d3748")
        st.plotly_chart(fig, use_container_width=True)

with col_right:
    fig2 = px.bar(
        filtered, x="month", y="total_originated",
        title="Monthly Origination Volume (£)",
        labels={"total_originated": "£ Originated", "month": ""},
        color_discrete_sequence=["#4299e1"]
    )
    fig2.update_layout(
        plot_bgcolor="#1a1f2e", paper_bgcolor="#1a1f2e",
        font_color="#e2e8f0", title_font_size=13,
        margin=dict(t=40, b=20, l=20, r=20)
    )
    fig2.update_xaxes(gridcolor="#2d3748")
    fig2.update_yaxes(gridcolor="#2d3748")
    st.plotly_chart(fig2, use_container_width=True)

# ── Risk Band & Regional ─────────────────────────────────────
st.markdown('<div class="section-title">// Risk Segmentation & Regional Breakdown</div>',
            unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    fig3 = px.bar(
        risk_bands, x="risk_band", y="default_rate",
        color="risk_band",
        title="Default Rate by Risk Band (%)",
        labels={"default_rate": "Default Rate (%)", "risk_band": "Risk Band"},
        color_discrete_map={"A":"#48bb78","B":"#ecc94b","C":"#ed8936","D":"#fc8181"},
        text="default_rate"
    )
    fig3.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig3.update_layout(
        plot_bgcolor="#1a1f2e", paper_bgcolor="#1a1f2e",
        font_color="#e2e8f0", showlegend=False,
        title_font_size=13,
        margin=dict(t=40, b=20, l=20, r=20)
    )
    fig3.update_xaxes(gridcolor="#2d3748")
    fig3.update_yaxes(gridcolor="#2d3748")
    st.plotly_chart(fig3, use_container_width=True)

with col_b:
    fig4 = px.scatter(
        regional, x="loan_volume", y="default_rate",
        size="avg_loan", color="region", text="region",
        title="Regional: Loan Volume vs Default Rate",
        labels={"loan_volume": "Total Loan Volume (£)",
                "default_rate": "Default Rate (%)"}
    )
    fig4.update_traces(textposition="top center")
    fig4.update_layout(
        plot_bgcolor="#1a1f2e", paper_bgcolor="#1a1f2e",
        font_color="#e2e8f0", showlegend=False,
        title_font_size=13,
        margin=dict(t=40, b=20, l=20, r=20)
    )
    fig4.update_xaxes(gridcolor="#2d3748")
    fig4.update_yaxes(gridcolor="#2d3748")
    st.plotly_chart(fig4, use_container_width=True)

# ── Raw Data Table ───────────────────────────────────────────
with st.expander("📋 View Raw Portfolio Data"):
    st.dataframe(
        filtered.set_index("month").style.format({
            "approval_rate":    "{:.1f}%",
            "delinquency_30d":  "{:.2f}%",
            "delinquency_90d":  "{:.2f}%",
            "net_loss_rate":    "{:.2f}%",
            "avg_loan_value":   "£{:,.0f}",
            "total_originated": "£{:,.0f}",
            "nps_score":        "{:.1f}",
        }),
        use_container_width=True
    )

st.markdown("---")
st.caption("Seun Ismail Adeleke · Credit Data Analyst · seunismailadeleke@gmail.com")
