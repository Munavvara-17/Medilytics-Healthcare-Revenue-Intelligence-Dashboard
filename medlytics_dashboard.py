"""
╔══════════════════════════════════════════════════════════════════════════════╗
║         MEDLYTICS - Healthcare Revenue Intelligence Dashboard                ║
║         Client: Sanjeevani Multispeciality Hospital                          ║
║         Built with: Python · Streamlit · Plotly · Pandas                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

Run Instructions:
    pip install streamlit pandas plotly numpy
    streamlit run medlytics_dashboard.py

Place your dataset at: updated_cleaned_claim_dataset.csv (same folder)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Medlytics | Revenue Intelligence",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS — DARK MEDICAL THEME
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Global ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp { background-color: #0d1117; color: #e6edf3; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #161b22 0%, #0d1117 100%);
        border-right: 1px solid #21262d;
    }
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #58a6ff !important;
    }

    /* ── KPI Cards ── */
    .kpi-card {
        background: linear-gradient(135deg, #161b22 0%, #1c2128 100%);
        border: 1px solid #21262d;
        border-radius: 12px;
        padding: 20px 18px;
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
        height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(88,166,255,0.15);
        border-color: #388bfd;
    }
    .kpi-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #8b949e;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 26px;
        font-weight: 700;
        color: #e6edf3;
        line-height: 1.1;
    }
    .kpi-delta {
        font-size: 12px;
        margin-top: 6px;
    }
    .delta-up   { color: #3fb950; }
    .delta-down { color: #f85149; }
    .delta-neu  { color: #d29922; }

    /* ── Section Headers ── */
    .section-header {
        font-size: 18px;
        font-weight: 700;
        color: #58a6ff;
        padding: 8px 0 4px 0;
        border-bottom: 2px solid #21262d;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* ── Alert Banners ── */
    .alert-critical {
        background: rgba(248,81,73,0.12);
        border-left: 4px solid #f85149;
        border-radius: 8px;
        padding: 12px 16px;
        color: #ffa198;
        margin: 8px 0;
        font-size: 13px;
    }
    .alert-warning {
        background: rgba(210,153,34,0.12);
        border-left: 4px solid #d29922;
        border-radius: 8px;
        padding: 12px 16px;
        color: #e3b341;
        margin: 8px 0;
        font-size: 13px;
    }
    .alert-ok {
        background: rgba(63,185,80,0.10);
        border-left: 4px solid #3fb950;
        border-radius: 8px;
        padding: 12px 16px;
        color: #56d364;
        margin: 8px 0;
        font-size: 13px;
    }

    /* ── Page Hero ── */
    .hero-header {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%);
        border: 1px solid #21262d;
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .hero-header::before {
        content: '';
        position: absolute;
        top: -60px; right: -60px;
        width: 200px; height: 200px;
        background: radial-gradient(circle, rgba(88,166,255,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-title {
        font-size: 28px;
        font-weight: 700;
        background: linear-gradient(90deg, #58a6ff, #a5d6ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    .hero-subtitle {
        font-size: 14px;
        color: #8b949e;
        margin-top: 4px;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(88,166,255,0.15);
        border: 1px solid #388bfd;
        color: #58a6ff;
        font-size: 11px;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 20px;
        margin-top: 10px;
        margin-right: 6px;
    }

    /* ── Insight Pill ── */
    .insight-box {
        background: rgba(88,166,255,0.07);
        border: 1px solid rgba(88,166,255,0.2);
        border-radius: 10px;
        padding: 12px 16px;
        font-size: 13px;
        color: #a5d6ff;
        margin: 6px 0;
    }
    .insight-box b { color: #58a6ff; }

    /* ── Tables ── */
    .dataframe { background: #161b22 !important; color: #e6edf3 !important; }
    .dataframe th { background: #21262d !important; color: #58a6ff !important; font-weight: 600 !important; }
    .dataframe td { color: #e6edf3 !important; }

    /* ── Metrics ── */
    [data-testid="metric-container"] {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 10px;
        padding: 12px;
    }
    [data-testid="metric-container"] label { color: #8b949e !important; }
    [data-testid="metric-container"] div[data-testid="metric-value"] { color: #e6edf3 !important; }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] { background: #161b22; border-radius: 10px; padding: 4px; }
    .stTabs [data-baseweb="tab"] { background: transparent; color: #8b949e; border-radius: 8px; font-weight: 500; }
    .stTabs [aria-selected="true"] { background: #21262d !important; color: #58a6ff !important; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0d1117; }
    ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #388bfd; }

    /* ── Hide Streamlit watermarks ── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PLOTLY BASE LAYOUT (consistent dark theme)
# ─────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#c9d1d9", size=12),
    margin=dict(l=40, r=20, t=50, b=40),
    hoverlabel=dict(bgcolor="#161b22", bordercolor="#388bfd", font=dict(color="#e6edf3")),
)

# Default legend style — use fig.update_layout(legend=LEGEND_STYLE) separately
LEGEND_STYLE = dict(bgcolor="rgba(22,27,34,0.9)", bordercolor="#30363d",
                    borderwidth=1, font=dict(color="#c9d1d9"))
AXIS_STYLE   = dict(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
AXIS_NO_GRID = dict(gridcolor="rgba(0,0,0,0)", linecolor="#30363d")


def apply_layout(fig, title="", **kwargs):
    """Central helper — always applies base theme. Never pass legend/xaxis/yaxis here."""
    fig.update_layout(**PLOTLY_LAYOUT, title=title, **kwargs)
    fig.update_layout(legend=LEGEND_STYLE)
COLOR_SEQ = ["#58a6ff","#3fb950","#d29922","#f85149","#a5d6ff","#7ee787","#ffa657","#ff7b72"]
COLOR_DEPT = {
    "General Medicine": "#58a6ff",
    "Emergency":        "#f85149",
    "Orthopedics":      "#3fb950",
    "Cardiology":       "#ffa657",
    "Neurology":        "#d2a8ff",
}

# ─────────────────────────────────────────────────────────────
# DATA LOADING & CACHING
# ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Parse dates
    for col in ["Admission_Date", "Discharge_Date", "Claim_Submission_Date", "Settlement_Date"]:
        df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")

    # Ensure boolean
    df["High_Risk_Claim"] = df["High_Risk_Claim"].astype(bool)
    df["Denial_Flag"]     = df["Denial_Flag"].astype(int)

    # Month as period for sorting
    df["Month_Period"] = pd.to_datetime(df["Month"], format="%Y-%m", errors="coerce")

    return df

# ─────────────────────────────────────────────────────────────
# SIDEBAR  — FILTERS
# ─────────────────────────────────────────────────────────────
def sidebar(df: pd.DataFrame):
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center; padding:10px 0 20px 0;'>
            <div style='font-size:32px;'>🏥</div>
            <div style='font-size:16px; font-weight:700; color:#58a6ff;'>Medlytics</div>
            <div style='font-size:11px; color:#8b949e; margin-top:2px;'>Revenue Intelligence</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🔍 Filters")
        st.markdown("---")

        # ── Date range via Month selector
        months_sorted = sorted(df["Month_Period"].dropna().unique())
        month_labels  = [m.strftime("%b %Y") for m in months_sorted]
        selected_range = st.select_slider(
            "📅 Time Period",
            options=month_labels,
            value=(month_labels[0], month_labels[-1]),
        )
        start_idx = month_labels.index(selected_range[0])
        end_idx   = month_labels.index(selected_range[1])
        selected_months = months_sorted[start_idx : end_idx + 1]

        # ── Departments
        depts = sorted(df["Department"].dropna().unique())
        selected_depts = st.multiselect("🏬 Department", depts, default=depts)

        # ── Insurance Type
        ins_types = sorted(df["Insurance_Type"].dropna().unique())
        selected_ins = st.multiselect("🛡️ Insurance Type", ins_types, default=ins_types)

        # ── Admission Type
        adm_types = sorted(df["Admission_Type"].dropna().unique())
        selected_adm = st.multiselect("🚪 Admission Type", adm_types, default=adm_types)

        # ── High Risk Only toggle
        show_high_risk = st.checkbox("⚠️ High-Risk Claims Only", value=False)

        # ── Denial toggle
        show_denied = st.checkbox("🚫 Denied Claims Only", value=False)

        st.markdown("---")
        st.markdown(
            "<div style='font-size:11px; color:#8b949e; text-align:center;'>"
            "Sanjeevani Multispeciality Hospital<br>© 2025 Medlytics Analytics</div>",
            unsafe_allow_html=True,
        )

    # Apply filters
    mask = (
        df["Month_Period"].isin(selected_months)
        & df["Department"].isin(selected_depts)
        & df["Insurance_Type"].isin(selected_ins)
        & df["Admission_Type"].isin(selected_adm)
    )
    if show_high_risk: mask &= df["High_Risk_Claim"]
    if show_denied:    mask &= df["Denial_Flag"] == 1

    return df[mask].copy()


# ─────────────────────────────────────────────────────────────
# HELPER: format large numbers
# ─────────────────────────────────────────────────────────────
def fmt(n, prefix="₹"):
    if n >= 1e7:  return f"{prefix}{n/1e7:.2f} Cr"
    if n >= 1e5:  return f"{prefix}{n/1e5:.2f} L"
    if n >= 1e3:  return f"{prefix}{n/1e3:.1f} K"
    return f"{prefix}{n:.0f}"

def pct(n): return f"{n:.1f}%"


# ─────────────────────────────────────────────────────────────
# PAGE 1 — EXECUTIVE OVERVIEW
# ─────────────────────────────────────────────────────────────
def page_overview(df: pd.DataFrame):
    # ── Hero Header ──────────────────────────────────────────
    st.markdown("""
    <div class='hero-header'>
        <p class='hero-title'>🏥 Medlytics — Revenue Intelligence Dashboard</p>
        <p class='hero-subtitle'>Sanjeevani Multispeciality Hospital · Claim Cycle Analytics</p>
        <span class='hero-badge'>📊 Descriptive Analytics</span>
        <span class='hero-badge'>⚠️ Risk Monitoring</span>
        <span class='hero-badge'>💡 Actionable Insights</span>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI CARDS ─────────────────────────────────────────────
    st.markdown("<div class='section-header'>📌 Key Performance Indicators</div>", unsafe_allow_html=True)

    total_claims     = len(df)
    avg_approval     = df["Approval_Rate"].mean() * 100
    total_rev_loss   = df["Revenue_Loss"].sum()
    avg_claim_gap    = df["Claim_Gap"].mean()
    avg_payment_gap  = df["Payment_Gap"].mean()
    high_risk_count  = df["High_Risk_Claim"].sum()
    avg_proc_time    = df["Processing_Time"].mean()
    avg_billing      = df["Billing_Amount"].mean()

    def kpi(label, value, delta_html="", color="#e6edf3"):
        return f"""
        <div class='kpi-card'>
            <div class='kpi-label'>{label}</div>
            <div class='kpi-value' style='color:{color};'>{value}</div>
            <div class='kpi-delta'>{delta_html}</div>
        </div>"""

    cols = st.columns(4)
    with cols[0]:
        st.markdown(kpi("Total Claims Processed", f"{total_claims:,}",
            "<span class='delta-neu'>All filtered claims</span>", "#58a6ff"), unsafe_allow_html=True)
    with cols[1]:
        clr = "#3fb950" if avg_approval >= 80 else "#f85149"
        st.markdown(kpi("Avg Claim Approval Rate", pct(avg_approval),
            "<span class='delta-up'>Target: ≥ 80%</span>", clr), unsafe_allow_html=True)
    with cols[2]:
        st.markdown(kpi("Total Revenue Loss", fmt(total_rev_loss),
            "<span class='delta-down'>Leakage from billing</span>", "#f85149"), unsafe_allow_html=True)
    with cols[3]:
        st.markdown(kpi("Avg Claim Gap", fmt(avg_claim_gap),
            "<span class='delta-neu'>Billing – Claim amt</span>", "#d29922"), unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    cols2 = st.columns(4)
    with cols2[0]:
        st.markdown(kpi("Avg Payment Gap", fmt(avg_payment_gap),
            "<span class='delta-neu'>Approved – Received</span>", "#d29922"), unsafe_allow_html=True)
    with cols2[1]:
        clr = "#f85149" if high_risk_count > 500 else "#d29922"
        st.markdown(kpi("High-Risk Claims", f"{high_risk_count:,}",
            f"<span class='delta-down'>{pct(high_risk_count/total_claims*100)} of total</span>", clr), unsafe_allow_html=True)
    with cols2[2]:
        clr = "#3fb950" if avg_proc_time < 30 else "#f85149"
        st.markdown(kpi("Avg Processing Time", f"{avg_proc_time:.1f} days",
            "<span class='delta-neu'>Submission → Settlement</span>", clr), unsafe_allow_html=True)
    with cols2[3]:
        st.markdown(kpi("Avg Billing Amount", fmt(avg_billing),
            "<span class='delta-neu'>Per claim billed</span>", "#a5d6ff"), unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── Intelligent Alerts ────────────────────────────────────
    st.markdown("<div class='section-header'>🚨 Intelligent Alerts</div>", unsafe_allow_html=True)
    a1, a2, a3 = st.columns(3)
    denial_rate = df["Denial_Flag"].mean() * 100
    with a1:
        if denial_rate > 20:
            st.markdown(f"<div class='alert-critical'>🔴 <b>High Denial Rate:</b> {denial_rate:.1f}% of claims denied — immediate review required.</div>", unsafe_allow_html=True)
        elif denial_rate > 10:
            st.markdown(f"<div class='alert-warning'>🟡 <b>Moderate Denial Rate:</b> {denial_rate:.1f}% — monitor billing documentation.</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='alert-ok'>🟢 <b>Denial Rate Healthy:</b> {denial_rate:.1f}% — within acceptable range.</div>", unsafe_allow_html=True)
    with a2:
        rev_loss_pct = total_rev_loss / df["Billing_Amount"].sum() * 100
        if rev_loss_pct > 20:
            st.markdown(f"<div class='alert-critical'>🔴 <b>Revenue Leakage Critical:</b> {rev_loss_pct:.1f}% of billed revenue lost.</div>", unsafe_allow_html=True)
        elif rev_loss_pct > 10:
            st.markdown(f"<div class='alert-warning'>🟡 <b>Revenue Leakage Elevated:</b> {rev_loss_pct:.1f}% — investigate top departments.</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='alert-ok'>🟢 <b>Revenue Capture Good:</b> {rev_loss_pct:.1f}% leakage rate.</div>", unsafe_allow_html=True)
    with a3:
        if high_risk_count > 1000:
            st.markdown(f"<div class='alert-critical'>🔴 <b>High-Risk Volume:</b> {high_risk_count} claims flagged — pre-submission audit needed.</div>", unsafe_allow_html=True)
        elif high_risk_count > 300:
            st.markdown(f"<div class='alert-warning'>🟡 <b>Risk Alert:</b> {high_risk_count} high-risk claims in current period.</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='alert-ok'>🟢 <b>Low Risk Volume:</b> {high_risk_count} high-risk claims flagged.</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Row 1: Revenue trend + Department revenue bar ─────────
    st.markdown("<div class='section-header'>📈 Revenue Trend & Department Performance</div>", unsafe_allow_html=True)
    c1, c2 = st.columns([3, 2])

    with c1:
        # Monthly Revenue Trend — Expected vs Actual vs Revenue Loss
        # WHY: Shows the growing gap between expected and received revenue over time.
        # Critical for CFO to see financial trajectory at a glance.
        monthly = (
            df.groupby("Month_Period")[["Expected_Revenue", "Actual_Revenue", "Revenue_Loss"]]
            .sum()
            .reset_index()
            .sort_values("Month_Period")
        )
        monthly["Month_Label"] = monthly["Month_Period"].dt.strftime("%b %Y")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly["Month_Label"], y=monthly["Expected_Revenue"],
            name="Expected Revenue", mode="lines+markers",
            line=dict(color="#58a6ff", width=2.5),
            marker=dict(size=5),
            fill=None,
        ))
        fig.add_trace(go.Scatter(
            x=monthly["Month_Label"], y=monthly["Actual_Revenue"],
            name="Actual Revenue", mode="lines+markers",
            line=dict(color="#3fb950", width=2.5),
            marker=dict(size=5),
            fill="tonexty", fillcolor="rgba(248,81,73,0.08)",
        ))
        fig.add_trace(go.Bar(
            x=monthly["Month_Label"], y=monthly["Revenue_Loss"],
            name="Revenue Loss", marker_color="rgba(248,81,73,0.55)",
            yaxis="y2",
        ))
        apply_layout(fig, "Monthly Revenue: Expected vs Actual vs Loss",
            yaxis2=dict(title="Revenue Loss (₹)", overlaying="y", side="right", showgrid=False))
        fig.update_layout(legend=dict(orientation="h", y=1.08, x=0,
                        bgcolor="rgba(22,27,34,0.9)", bordercolor="#30363d",
                        borderwidth=1, font=dict(color="#c9d1d9")))
        fig.update_xaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_layout(yaxis=dict(title="Amount (₹)", gridcolor="#21262d",
                                     linecolor="#30363d", zerolinecolor="#30363d"))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # Department Revenue Comparison — Horizontal Bar
        # WHY: Immediately shows which departments drive revenue and which leak it.
        # Enables department heads to benchmark performance.
        dept_rev = (
            df.groupby("Department")[["Actual_Revenue", "Revenue_Loss"]]
            .sum()
            .reset_index()
            .sort_values("Actual_Revenue", ascending=True)
        )
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=dept_rev["Department"], x=dept_rev["Actual_Revenue"],
            name="Actual Revenue", orientation="h",
            marker_color=[COLOR_DEPT.get(d, "#58a6ff") for d in dept_rev["Department"]],
        ))
        fig.add_trace(go.Bar(
            y=dept_rev["Department"], x=dept_rev["Revenue_Loss"],
            name="Revenue Loss", orientation="h",
            marker_color="rgba(248,81,73,0.65)",
        ))
        apply_layout(fig, "Revenue by Department", barmode="stack")
        fig.update_xaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_yaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_xaxes(title_text="Amount (₹)", gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_yaxes(gridcolor="rgba(0,0,0,0)", linecolor="#30363d")
        st.plotly_chart(fig, use_container_width=True)

    # ── Row 2: Claims distribution + Approval Rate by Dept ────
    c3, c4 = st.columns(2)
    with c3:
        # Claims Volume by Insurance Type — Donut
        # WHY: Insurance mix drives reimbursement risk. Private pays faster; Government claims
        # have higher denial risk. Understanding this mix informs revenue strategy.
        ins_counts = df["Insurance_Type"].value_counts().reset_index()
        ins_counts.columns = ["Insurance_Type", "Count"]
        fig = go.Figure(go.Pie(
            labels=ins_counts["Insurance_Type"],
            values=ins_counts["Count"],
            hole=0.55,
            marker=dict(colors=COLOR_SEQ, line=dict(color="#0d1117", width=2)),
            textinfo="label+percent",
            textfont=dict(color="#e6edf3", size=11),
        ))
        fig.add_annotation(
            text=f"<b>{total_claims:,}</b><br><span style='font-size:10px'>Claims</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="#e6edf3"),
        )
        apply_layout(fig, "Claims by Insurance Type")
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        # Approval Rate by Department — Horizontal bar with threshold line
        # WHY: Low approval rate = high denial = revenue lost. Departments below 80%
        # threshold need immediate billing process investigation.
        dept_approval = (
            df.groupby("Department")["Approval_Rate"]
            .mean()
            .mul(100)
            .reset_index()
            .sort_values("Approval_Rate")
        )
        colors = ["#f85149" if v < 70 else "#d29922" if v < 80 else "#3fb950"
                  for v in dept_approval["Approval_Rate"]]
        fig = go.Figure(go.Bar(
            y=dept_approval["Department"],
            x=dept_approval["Approval_Rate"],
            orientation="h",
            marker_color=colors,
            text=dept_approval["Approval_Rate"].map(lambda x: f"{x:.1f}%"),
            textposition="outside",
            textfont=dict(color="#e6edf3"),
        ))
        fig.add_vline(x=80, line_dash="dash", line_color="#d29922",
                      annotation_text="Target 80%", annotation_position="top right",
                      annotation_font_color="#d29922")
        apply_layout(fig, "Avg Approval Rate by Department")
        fig.update_xaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_yaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_xaxes(title_text="Approval Rate (%)", range=[0, 115], gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_yaxes(gridcolor="rgba(0,0,0,0)", linecolor="#30363d")
        st.plotly_chart(fig, use_container_width=True)

    # ── Insights Panel ────────────────────────────────────────
    st.markdown("<div class='section-header'>💡 Auto-Generated Insights</div>", unsafe_allow_html=True)
    top_loss_dept = df.groupby("Department")["Revenue_Loss"].sum().idxmax()
    worst_approval = dept_approval.iloc[0]
    monthly_peak   = monthly.loc[monthly["Revenue_Loss"].idxmax(), "Month_Label"]
    ic1, ic2, ic3 = st.columns(3)
    with ic1:
        st.markdown(f"<div class='insight-box'>🔴 <b>{top_loss_dept}</b> has the highest total revenue loss — prioritize billing audit in this department.</div>", unsafe_allow_html=True)
    with ic2:
        st.markdown(f"<div class='insight-box'>📉 <b>{worst_approval['Department']}</b> shows the lowest approval rate at <b>{worst_approval['Approval_Rate']:.1f}%</b> — review claim documentation workflow.</div>", unsafe_allow_html=True)
    with ic3:
        st.markdown(f"<div class='insight-box'>📅 Revenue loss peaked in <b>{monthly_peak}</b> — investigate claim volume spike or denial surge in that period.</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# PAGE 2 — CLAIM ANALYSIS
# ─────────────────────────────────────────────────────────────
def page_claims(df: pd.DataFrame):
    st.markdown("""
    <div class='hero-header'>
        <p class='hero-title'>📋 Claim-Level Analysis</p>
        <p class='hero-subtitle'>Processing efficiency, denial patterns, and gap analysis</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Row 1: Denial Analysis ────────────────────────────────
    st.markdown("<div class='section-header'>🚫 Denial Pattern Analysis</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    with c1:
        # Denial Rate by Department — stacked bar
        # WHY: Denial rate reveals where billing process breaks down.
        # Higher denials → more rework, delayed revenue, operational cost.
        dept_denial = (
            df.groupby("Department")
            .agg(Total=("Denial_Flag","count"), Denied=("Denial_Flag","sum"))
            .reset_index()
        )
        dept_denial["Approved"] = dept_denial["Total"] - dept_denial["Denied"]
        dept_denial["Denial_Rate"] = dept_denial["Denied"] / dept_denial["Total"] * 100
        dept_denial = dept_denial.sort_values("Denial_Rate", ascending=False)

        fig = go.Figure()
        fig.add_trace(go.Bar(name="Approved", y=dept_denial["Department"], x=dept_denial["Approved"],
                             orientation="h", marker_color="#3fb950"))
        fig.add_trace(go.Bar(name="Denied",   y=dept_denial["Department"], x=dept_denial["Denied"],
                             orientation="h", marker_color="#f85149"))
        apply_layout(fig, "Claim Status by Department", barmode="stack")
        fig.update_xaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_yaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_xaxes(title_text="No. of Claims", gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_yaxes(gridcolor="rgba(0,0,0,0)", linecolor="#30363d")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # Denial Rate by Insurance Type
        # WHY: Government schemes typically have higher documentation requirements
        # and thus higher denial rates. This chart exposes systemic payer-side risk.
        ins_denial = (
            df.groupby("Insurance_Type")
            .agg(Total=("Denial_Flag","count"), Denied=("Denial_Flag","sum"))
            .reset_index()
        )
        ins_denial["Denial_Rate"] = ins_denial["Denied"] / ins_denial["Total"] * 100
        ins_denial = ins_denial.sort_values("Denial_Rate", ascending=True)

        fig = go.Figure(go.Bar(
            y=ins_denial["Insurance_Type"],
            x=ins_denial["Denial_Rate"],
            orientation="h",
            marker_color=[
                "#f85149" if v > 20 else "#d29922" if v > 10 else "#3fb950"
                for v in ins_denial["Denial_Rate"]
            ],
            text=ins_denial["Denial_Rate"].map(lambda x: f"{x:.1f}%"),
            textposition="outside",
            textfont=dict(color="#e6edf3"),
        ))
        fig.add_vline(x=16.5, line_dash="dash", line_color="#d29922",
                      annotation_text="Avg", annotation_font_color="#d29922")
        apply_layout(fig, "Denial Rate by Insurance Type")
        fig.update_xaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_yaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_xaxes(title_text="Denial Rate (%)", gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_yaxes(gridcolor="rgba(0,0,0,0)", linecolor="#30363d")
        st.plotly_chart(fig, use_container_width=True)

    with c3:
        # Admission Type vs Denial Count — Grouped bar
        # WHY: Emergency admissions may have documentation rushed,
        # increasing denial probability. Helps process improvement teams.
        adm_denial = (
            df.groupby(["Admission_Type","Denial_Flag"])
            .size().reset_index(name="Count")
        )
        adm_denial["Status"] = adm_denial["Denial_Flag"].map({0:"Approved", 1:"Denied"})
        fig = px.bar(adm_denial, x="Admission_Type", y="Count", color="Status",
                     color_discrete_map={"Approved":"#3fb950","Denied":"#f85149"},
                     barmode="group", title="Claims by Admission Type vs Status")
        apply_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # ── Row 2: Processing Time & Gap Analysis ─────────────────
    st.markdown("<div class='section-header'>⏱️ Processing Time & Gap Analysis</div>", unsafe_allow_html=True)
    c4, c5 = st.columns(2)

    with c4:
        # Processing Time Distribution — Box plot by Department
        # WHY: Box plots show the full spread (min, median, IQR, outliers) of processing time.
        # Outliers indicate claims stuck in processing — representing delayed cash flow.
        fig = px.box(df, x="Department", y="Processing_Time", color="Department",
                     color_discrete_map=COLOR_DEPT,
                     title="Processing Time Distribution by Department",
                     labels={"Processing_Time": "Days"})
        apply_layout(fig, showlegend=False)
        fig.add_hline(y=df["Processing_Time"].mean(), line_dash="dot",
                      line_color="#58a6ff", annotation_text="Mean",
                      annotation_font_color="#58a6ff")
        st.plotly_chart(fig, use_container_width=True)

    with c5:
        # Claim Gap vs Payment Gap — Scatter with color by department
        # WHY: Claim Gap (Billing–Claim) reveals underbilling or charge capture losses.
        # Payment Gap (Approved–Received) reveals collection inefficiency.
        # Together they pin-point where in the cycle money is lost.
        sample = df.sample(min(3000, len(df)), random_state=42)
        fig = px.scatter(
            sample, x="Claim_Gap", y="Payment_Gap",
            color="Department", color_discrete_map=COLOR_DEPT,
            opacity=0.55, size_max=6,
            title="Claim Gap vs Payment Gap (Sample 3,000)",
            labels={"Claim_Gap":"Claim Gap (₹)", "Payment_Gap":"Payment Gap (₹)"},
            hover_data=["Department","Insurance_Type","Approval_Rate"],
        )
        apply_layout(fig)
        fig.add_hline(y=0, line_color="#30363d", line_width=1)
        fig.add_vline(x=0, line_color="#30363d", line_width=1)
        st.plotly_chart(fig, use_container_width=True)

    # ── Row 3: Documentation Delay vs Denial ──────────────────
    st.markdown("<div class='section-header'>📄 Documentation Delay Impact</div>", unsafe_allow_html=True)
    c6, c7 = st.columns(2)

    with c6:
        # Denial rate by Documentation Delay Days — Line
        # WHY: One of the biggest controllable drivers of denials.
        # If denial rates spike at delay > 3 days, the hospital should set a 3-day SLA.
        doc_denial = (
            df.groupby("Documentation_Delay_Days")
            .agg(Total=("Denial_Flag","count"), Denied=("Denial_Flag","sum"))
            .reset_index()
        )
        doc_denial["Denial_Rate"] = doc_denial["Denied"] / doc_denial["Total"] * 100
        doc_denial = doc_denial[doc_denial["Documentation_Delay_Days"] <= 20]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=doc_denial["Documentation_Delay_Days"],
            y=doc_denial["Denial_Rate"],
            mode="lines+markers",
            line=dict(color="#f85149", width=2.5),
            marker=dict(size=6, color="#f85149"),
            fill="tozeroy", fillcolor="rgba(248,81,73,0.07)",
        ))
        apply_layout(fig, "Denial Rate by Documentation Delay (Days)")
        fig.update_xaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_yaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_xaxes(title_text="Delay Days", gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_yaxes(title_text="Denial Rate (%)", gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        st.plotly_chart(fig, use_container_width=True)

    with c7:
        # Previous Denial Count vs Approval Rate — Bar
        # WHY: Claims from patients/accounts with prior denials are far more likely to be denied
        # again. Identifying repeat-denial accounts allows proactive review.
        prev_denial = (
            df.groupby("Previous_Denial_Count")["Approval_Rate"]
            .mean()
            .mul(100)
            .reset_index()
        )
        prev_denial = prev_denial[prev_denial["Previous_Denial_Count"] <= 10]
        fig = px.bar(prev_denial, x="Previous_Denial_Count", y="Approval_Rate",
                     title="Approval Rate vs Prior Denial History",
                     labels={"Previous_Denial_Count":"Prior Denials","Approval_Rate":"Avg Approval Rate (%)"},
                     color="Approval_Rate",
                     color_continuous_scale=["#f85149","#d29922","#3fb950"])
        apply_layout(fig, coloraxis_showscale=False)
        fig.add_hline(y=80, line_dash="dash", line_color="#d29922",
                      annotation_text="Target 80%", annotation_font_color="#d29922")
        st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# PAGE 3 — REVENUE INTEGRITY
# ─────────────────────────────────────────────────────────────
def page_revenue(df: pd.DataFrame):
    st.markdown("""
    <div class='hero-header'>
        <p class='hero-title'>💰 Revenue Integrity Monitoring</p>
        <p class='hero-subtitle'>Leakage sources, charge capture efficiency, and risk exposure</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Revenue Lifecycle Funnel ──────────────────────────────
    st.markdown("<div class='section-header'>🔽 Revenue Lifecycle Funnel</div>", unsafe_allow_html=True)

    # WHY: The funnel is the most powerful single visualization for the CFO.
    # It shows exactly where money drops off from billing → claim → approval → payment.
    total_billing  = df["Billing_Amount"].sum()
    total_claim    = df["Claim_Amount"].sum()
    total_approved = df["Approved_Amount"].sum()
    total_payment  = df["Payment_Received"].sum()

    fig = go.Figure(go.Funnel(
        y=["Total Billed", "Total Claimed", "Total Approved", "Payment Received"],
        x=[total_billing, total_claim, total_approved, total_payment],
        textinfo="value+percent initial",
        textfont=dict(color="#e6edf3", size=13),
        marker=dict(color=["#58a6ff","#a5d6ff","#3fb950","#d29922"],
                    line=dict(width=2, color="#0d1117")),
        connector=dict(line=dict(color="#30363d", dash="dot", width=2)),
    ))
    apply_layout(fig, "Revenue Lifecycle Funnel — End-to-End", height=380)
    st.plotly_chart(fig, use_container_width=True)

    # ── Row 1: Leakage Heatmap + Charge Capture ──────────────
    st.markdown("<div class='section-header'>🔥 Revenue Leakage Deep Dive</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        # Revenue Leakage by Dept × Insurance Type — Heatmap
        # WHY: Heatmap cross-tabs two categorical dimensions simultaneously.
        # Quickly surfaces which dept+insurer combos are chronic leakage hotspots.
        heat_data = df.pivot_table(
            values="Revenue_Leakage", index="Department",
            columns="Insurance_Type", aggfunc="sum"
        ).fillna(0)
        fig = go.Figure(go.Heatmap(
            z=heat_data.values,
            x=heat_data.columns.tolist(),
            y=heat_data.index.tolist(),
            colorscale=[[0,"#0d1117"],[0.5,"#d29922"],[1,"#f85149"]],
            text=heat_data.values,
            texttemplate="₹%{z:,.0f}",
            hovertemplate="Dept: %{y}<br>Insurer: %{x}<br>Leakage: ₹%{z:,.0f}<extra></extra>",
        ))
        apply_layout(fig, "Revenue Leakage Heatmap: Dept × Insurance")
        fig.update_xaxes(title_text="Insurance Type")
        fig.update_yaxes(title_text="Department")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # Charge Capture Efficiency Distribution — Histogram
        # WHY: Charge Capture Efficiency (CCE) measures how well the hospital
        # converts services into billed claims. <95% signals systematic underbilling.
        fig = go.Figure(go.Histogram(
            x=df["Charge_Capture_Efficiency"],
            nbinsx=50,
            marker_color="#58a6ff",
            opacity=0.8,
        ))
        fig.add_vline(x=95, line_dash="dash", line_color="#3fb950",
                      annotation_text="95% Target", annotation_font_color="#3fb950")
        fig.add_vline(x=df["Charge_Capture_Efficiency"].mean(), line_dash="dot",
                      line_color="#d29922",
                      annotation_text=f"Mean {df['Charge_Capture_Efficiency'].mean():.1f}%",
                      annotation_font_color="#d29922")
        apply_layout(fig, "Charge Capture Efficiency Distribution")
        fig.update_xaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_yaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_xaxes(title_text="CCE (%)", gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_yaxes(title_text="Claims", gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        st.plotly_chart(fig, use_container_width=True)

    # ── Row 2: Revenue at Risk + Monthly Leakage Trend ────────
    c3, c4 = st.columns(2)

    with c3:
        # Revenue at Risk by Admission Type — Stacked bar
        # WHY: Revenue at Risk = approved amount not yet received.
        # Emergency claims often have highest risk because documentation is rushed.
        risk_adm = (
            df.groupby(["Admission_Type","Department"])["Revenue_At_Risk"]
            .sum().reset_index()
        )
        fig = px.bar(risk_adm, x="Admission_Type", y="Revenue_At_Risk",
                     color="Department", color_discrete_map=COLOR_DEPT,
                     title="Revenue at Risk by Admission Type",
                     labels={"Revenue_At_Risk":"Revenue at Risk (₹)"},
                     barmode="stack")
        apply_layout(fig)
        fig.update_xaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_yaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        # Monthly Leakage Index Trend — Area chart
        # WHY: The Revenue Leakage Index (0-100) is a normalized metric that allows
        # fair comparison across months regardless of claim volume differences.
        monthly_rli = (
            df.groupby("Month_Period")["Revenue_Leakage_Index"]
            .mean().reset_index().sort_values("Month_Period")
        )
        monthly_rli["Month_Label"] = monthly_rli["Month_Period"].dt.strftime("%b %Y")
        fig = go.Figure(go.Scatter(
            x=monthly_rli["Month_Label"],
            y=monthly_rli["Revenue_Leakage_Index"],
            mode="lines+markers",
            fill="tozeroy",
            line=dict(color="#f85149", width=2.5),
            fillcolor="rgba(248,81,73,0.08)",
            marker=dict(size=5),
        ))
        apply_layout(fig, "Monthly Avg Revenue Leakage Index")
        fig.update_xaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_yaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_xaxes(title_text="Month", gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_yaxes(title_text="RLI Score", gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        st.plotly_chart(fig, use_container_width=True)

    # ── Top 10 Revenue Leakage Claims ─────────────────────────
    st.markdown("<div class='section-header'>🔎 Top 20 Revenue Leakage Claims</div>", unsafe_allow_html=True)

    # WHY: Actionable table surfacing the individual claims with the largest leakage
    # enables the RCM team to directly target accounts for recovery.
    top_leakage = (
        df.nlargest(20, "Revenue_Leakage")
        [["Claim_ID","Patient_ID","Department","Insurance_Type","Billing_Amount",
          "Approved_Amount","Payment_Received","Revenue_Leakage","Denial_Flag","High_Risk_Claim"]]
        .reset_index(drop=True)
    )
    top_leakage.index += 1
    top_leakage["Revenue_Leakage"] = top_leakage["Revenue_Leakage"].map(lambda x: f"₹{x:,.0f}")
    top_leakage["Billing_Amount"]   = top_leakage["Billing_Amount"].map(lambda x: f"₹{x:,.0f}")
    top_leakage["Approved_Amount"]  = top_leakage["Approved_Amount"].map(lambda x: f"₹{x:,.0f}")
    top_leakage["Payment_Received"] = top_leakage["Payment_Received"].map(lambda x: f"₹{x:,.0f}")
    top_leakage["Denial_Flag"]      = top_leakage["Denial_Flag"].map({0:"✅ No",1:"❌ Yes"})
    top_leakage["High_Risk_Claim"]  = top_leakage["High_Risk_Claim"].map({True:"⚠️ Yes",False:"No"})
    st.dataframe(top_leakage, use_container_width=True, height=420)


# ─────────────────────────────────────────────────────────────
# PAGE 4 — HIGH-RISK & ANOMALY DETECTION
# ─────────────────────────────────────────────────────────────
def page_risk(df: pd.DataFrame):
    st.markdown("""
    <div class='hero-header'>
        <p class='hero-title'>⚠️ High-Risk Claims & Billing Anomalies</p>
        <p class='hero-subtitle'>Detect irregular billing patterns before they cause revenue loss</p>
    </div>
    """, unsafe_allow_html=True)

    high_risk = df[df["High_Risk_Claim"]].copy()
    normal    = df[~df["High_Risk_Claim"]].copy()

    # ── Summary Metrics ───────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("High-Risk Claims",  f"{len(high_risk):,}", f"{len(high_risk)/len(df)*100:.1f}% of total")
    col2.metric("Avg Billing (HR)",  fmt(high_risk["Billing_Amount"].mean()), f"vs {fmt(normal['Billing_Amount'].mean())} normal")
    col3.metric("Denial Rate (HR)",  pct(high_risk["Denial_Flag"].mean()*100), f"vs {pct(normal['Denial_Flag'].mean()*100)} normal")
    col4.metric("Avg Rev Loss (HR)", fmt(high_risk["Revenue_Loss"].mean()), f"vs {fmt(normal['Revenue_Loss'].mean())} normal")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        # High-Risk vs Normal Billing Distribution — Violin
        # WHY: Violin plots show the full distribution shape (not just median).
        # High-risk claims often have multimodal billing (very low = underbilling,
        # very high = overbilling) which a box plot would hide.
        df_plot = df.copy()
        df_plot["Risk_Label"] = df_plot["High_Risk_Claim"].map({True:"High Risk", False:"Normal"})
        fig = px.violin(df_plot, y="Billing_Amount", x="Risk_Label",
                        color="Risk_Label", box=True, points=False,
                        color_discrete_map={"High Risk":"#f85149","Normal":"#3fb950"},
                        title="Billing Amount: High Risk vs Normal Claims")
        apply_layout(fig, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # High-Risk by Department — Treemap
        # WHY: Treemaps convey both count (area) and proportional risk (colour) in one view.
        # Perfect for spotting which departments are contributing disproportionate risk.
        hr_dept = (
            df.groupby("Department")
            .agg(High_Risk=("High_Risk_Claim","sum"), Total=("High_Risk_Claim","count"))
            .reset_index()
        )
        hr_dept["HR_Rate"] = hr_dept["High_Risk"] / hr_dept["Total"] * 100
        fig = px.treemap(hr_dept, path=["Department"], values="High_Risk",
                         color="HR_Rate",
                         color_continuous_scale=[[0,"#0d1117"],[0.5,"#d29922"],[1,"#f85149"]],
                         title="High-Risk Claim Distribution by Department",
                         custom_data=["HR_Rate","Total"])
        fig.update_traces(
            texttemplate="<b>%{label}</b><br>%{value} HR Claims<br>%{customdata[0]:.1f}% rate",
            hovertemplate="<b>%{label}</b><br>High-Risk: %{value}<br>Rate: %{customdata[0]:.1f}%<extra></extra>",
        )
        apply_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # ── Row 2: Anomaly Scatter + Processing Time vs Risk ──────
    c3, c4 = st.columns(2)

    with c3:
        # Billing Amount vs Length of Stay — coloured by Risk
        # WHY: Unusually high billing for short stays or very low billing for long stays
        # are classic anomaly signals. This scatter helps audit teams spot outliers instantly.
        sample = df.sample(min(4000, len(df)), random_state=99)
        sample["Risk_Label"] = sample["High_Risk_Claim"].map({True:"High Risk", False:"Normal"})
        fig = px.scatter(
            sample, x="Length_of_Stay", y="Billing_Amount",
            color="Risk_Label",
            color_discrete_map={"High Risk":"#f85149","Normal":"rgba(88,166,255,0.35)"},
            size="Revenue_Leakage", size_max=15, opacity=0.65,
            title="Billing Anomaly: Length of Stay vs Billing Amount",
            labels={"Length_of_Stay":"Length of Stay (days)", "Billing_Amount":"Billing Amount (₹)"},
            hover_data=["Department","Insurance_Type","Denial_Flag"],
        )
        apply_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        # High-Risk Monthly Trend — Bar + Line overlay
        # WHY: Tracking high-risk claims over time detects emerging systemic issues
        # (e.g., a new insurer requirement, a new doctor's billing habits).
        hr_monthly = (
            df.groupby("Month_Period")
            .agg(Total=("High_Risk_Claim","count"), High_Risk=("High_Risk_Claim","sum"))
            .reset_index()
            .sort_values("Month_Period")
        )
        hr_monthly["HR_Rate"] = hr_monthly["High_Risk"] / hr_monthly["Total"] * 100
        hr_monthly["Month_Label"] = hr_monthly["Month_Period"].dt.strftime("%b %Y")

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=hr_monthly["Month_Label"], y=hr_monthly["High_Risk"],
                             name="High-Risk Count", marker_color="rgba(248,81,73,0.7)"),
                      secondary_y=False)
        fig.add_trace(go.Scatter(x=hr_monthly["Month_Label"], y=hr_monthly["HR_Rate"],
                                 name="HR Rate %", mode="lines+markers",
                                 line=dict(color="#d29922", width=2), marker=dict(size=5)),
                      secondary_y=True)
        apply_layout(fig, "Monthly High-Risk Claims Trend")
        fig.update_yaxes(title_text="Count", secondary_y=False, gridcolor="#21262d")
        fig.update_yaxes(title_text="HR Rate (%)", secondary_y=True, showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

    # ── Risk Table ────────────────────────────────────────────
    st.markdown("<div class='section-header'>📋 Top High-Risk Claims — Action Required</div>", unsafe_allow_html=True)
    risk_table = (
        df[df["High_Risk_Claim"]]
        .nlargest(15, "Revenue_At_Risk")
        [["Claim_ID","Department","Doctor_Name","Insurance_Type","Admission_Type",
          "Billing_Amount","Revenue_At_Risk","Revenue_Leakage","Denial_Flag","Processing_Time"]]
        .reset_index(drop=True)
    )
    risk_table.index += 1
    risk_table["Billing_Amount"]  = risk_table["Billing_Amount"].map(lambda x: f"₹{x:,.0f}")
    risk_table["Revenue_At_Risk"] = risk_table["Revenue_At_Risk"].map(lambda x: f"₹{x:,.0f}")
    risk_table["Revenue_Leakage"] = risk_table["Revenue_Leakage"].map(lambda x: f"₹{x:,.0f}")
    risk_table["Denial_Flag"]     = risk_table["Denial_Flag"].map({0:"✅","1":"❌",1:"❌"})
    st.dataframe(risk_table, use_container_width=True, height=420)


# ─────────────────────────────────────────────────────────────
# PAGE 5 — DOCTOR & DEPARTMENT DEEP DIVE
# ─────────────────────────────────────────────────────────────
def page_department(df: pd.DataFrame):
    st.markdown("""
    <div class='hero-header'>
        <p class='hero-title'>🏬 Department & Doctor Performance</p>
        <p class='hero-subtitle'>Granular performance benchmarking across departments and physicians</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Select department ─────────────────────────────────────
    selected_dept = st.selectbox(
        "🔍 Select Department to Drill Down",
        sorted(df["Department"].unique()),
        index=0,
    )
    dept_df = df[df["Department"] == selected_dept]

    # Department KPIs
    d1, d2, d3, d4, d5 = st.columns(5)
    d1.metric("Claims",        f"{len(dept_df):,}")
    d2.metric("Approval Rate", pct(dept_df["Approval_Rate"].mean()*100))
    d3.metric("Avg Rev Loss",  fmt(dept_df["Revenue_Loss"].mean()))
    d4.metric("Denial Rate",   pct(dept_df["Denial_Flag"].mean()*100))
    d5.metric("Avg Proc Time", f"{dept_df['Processing_Time'].mean():.1f}d")
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        # Doctor-level Approval Rate — Horizontal bar
        # WHY: Identifies specific doctors with persistently low approval rates,
        # which may indicate individual coding/documentation issues requiring training.
        doc_perf = (
            dept_df.groupby("Doctor_Name")
            .agg(Approval=("Approval_Rate","mean"), Claims=("Claim_ID","count"),
                 Rev_Loss=("Revenue_Loss","sum"))
            .reset_index()
        )
        doc_perf["Approval"] *= 100
        doc_perf = doc_perf.sort_values("Approval")

        fig = go.Figure(go.Bar(
            y=doc_perf["Doctor_Name"], x=doc_perf["Approval"],
            orientation="h",
            marker_color=["#f85149" if v < 70 else "#d29922" if v < 80 else "#3fb950"
                          for v in doc_perf["Approval"]],
            text=doc_perf["Approval"].map(lambda x: f"{x:.1f}%"),
            textposition="outside", textfont=dict(color="#e6edf3"),
            customdata=doc_perf[["Claims","Rev_Loss"]].values,
            hovertemplate="<b>%{y}</b><br>Approval: %{x:.1f}%<br>Claims: %{customdata[0]}<br>Rev Loss: ₹%{customdata[1]:,.0f}<extra></extra>",
        ))
        fig.add_vline(x=80, line_dash="dash", line_color="#d29922",
                      annotation_text="Target", annotation_font_color="#d29922")
        apply_layout(fig, f"Doctor Approval Rates — {selected_dept}")
        fig.update_xaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_yaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_xaxes(range=[0,115], title_text="Approval Rate (%)", gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_yaxes(gridcolor="rgba(0,0,0,0)", linecolor="#30363d")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # Revenue Loss by Doctor — Bubble chart
        # WHY: Revenue loss size = bubble area; Approval Rate = X axis.
        # Doctors in the bottom-right (low approval, high loss) need intervention.
        fig = px.scatter(
            doc_perf, x="Approval", y="Rev_Loss",
            size="Claims", color="Rev_Loss",
            color_continuous_scale=["#3fb950","#d29922","#f85149"],
            hover_name="Doctor_Name",
            size_max=40,
            title=f"Revenue Loss vs Approval Rate — {selected_dept}",
            labels={"Approval":"Avg Approval Rate (%)","Rev_Loss":"Total Revenue Loss (₹)"},
        )
        apply_layout(fig, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        # Monthly claim volume for selected dept
        dept_monthly = (
            dept_df.groupby("Month_Period")
            .agg(Claims=("Claim_ID","count"), Rev_Loss=("Revenue_Loss","sum"))
            .reset_index().sort_values("Month_Period")
        )
        dept_monthly["Month_Label"] = dept_monthly["Month_Period"].dt.strftime("%b %Y")
        fig = px.area(dept_monthly, x="Month_Label", y="Claims",
                      title=f"Monthly Claim Volume — {selected_dept}",
                      color_discrete_sequence=["#58a6ff"])
        apply_layout(fig)
        fig.update_xaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_yaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        # Insurance mix for selected department — Pie
        dept_ins = dept_df["Insurance_Type"].value_counts().reset_index()
        dept_ins.columns = ["Insurance_Type","Count"]
        fig = px.pie(dept_ins, names="Insurance_Type", values="Count", hole=0.5,
                     color_discrete_sequence=COLOR_SEQ,
                     title=f"Insurance Mix — {selected_dept}")
        apply_layout(fig)
        st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# PAGE 6 — FORECASTING (Simple Trend)
# ─────────────────────────────────────────────────────────────
def page_forecast(df: pd.DataFrame):
    st.markdown("""
    <div class='hero-header'>
        <p class='hero-title'>📡 Revenue Forecasting Engine</p>
        <p class='hero-subtitle'>Projected revenue & denial trends for upcoming months</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div class='insight-box'>ℹ️ Forecasting uses <b>linear trend extrapolation</b> on historical monthly aggregates. "
        "For production deployment, replace with ARIMA / Prophet models.</div>",
        unsafe_allow_html=True
    )
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    horizon = st.slider("📅 Forecast Horizon (months)", 1, 12, 6)

    # Aggregate monthly
    monthly = (
        df.groupby("Month_Period")
        .agg(
            Actual_Revenue=("Actual_Revenue","sum"),
            Revenue_Loss=("Revenue_Loss","sum"),
            Claims=("Claim_ID","count"),
            Denial_Count=("Denial_Flag","sum"),
        )
        .reset_index().sort_values("Month_Period")
    )
    monthly["Month_Num"] = np.arange(len(monthly))
    monthly["Month_Label"] = monthly["Month_Period"].dt.strftime("%b %Y")

    # Future months
    last_month   = monthly["Month_Period"].max()
    future_dates = pd.date_range(
        start=last_month + pd.offsets.MonthBegin(1),
        periods=horizon, freq="MS"
    )
    future_labels = [d.strftime("%b %Y") for d in future_dates]
    future_nums   = np.arange(len(monthly), len(monthly) + horizon)

    def linear_forecast(series, future_nums):
        x = monthly["Month_Num"].values
        y = series.values
        coef = np.polyfit(x, y, 1)
        return np.polyval(coef, future_nums)

    # Revenue forecast
    rev_forecast    = linear_forecast(monthly["Actual_Revenue"], future_nums)
    loss_forecast   = linear_forecast(monthly["Revenue_Loss"], future_nums)
    claims_forecast = linear_forecast(monthly["Claims"], future_nums)

    all_labels  = monthly["Month_Label"].tolist() + future_labels
    all_rev_act = monthly["Actual_Revenue"].tolist() + [None]*horizon
    all_rev_fct = [None]*(len(monthly)-1) + [monthly["Actual_Revenue"].iloc[-1]] + rev_forecast.tolist()
    all_loss_fct = [None]*(len(monthly)-1) + [monthly["Revenue_Loss"].iloc[-1]] + loss_forecast.tolist()

    c1, c2 = st.columns(2)
    with c1:
        # Revenue Actual + Forecast
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=all_labels, y=all_rev_act, name="Actual Revenue",
                                 mode="lines+markers", line=dict(color="#58a6ff", width=2.5)))
        fig.add_trace(go.Scatter(x=all_labels, y=all_rev_fct, name="Forecasted Revenue",
                                 mode="lines+markers", line=dict(color="#3fb950", width=2, dash="dot"),
                                 marker=dict(symbol="diamond", size=7)))
        # shaded confidence band (±10%)
        upper = [v*1.1 if v else None for v in all_rev_fct]
        lower = [v*0.9 if v else None for v in all_rev_fct]
        fig.add_trace(go.Scatter(x=all_labels+all_labels[::-1],
                                 y=upper+lower[::-1],
                                 fill="toself", fillcolor="rgba(63,185,80,0.07)",
                                 line=dict(color="rgba(0,0,0,0)"), showlegend=False, name="±10% CI"))
        # Vertical separator
        fig.add_vline(x=monthly["Month_Label"].iloc[-1], line_dash="dash", line_color="#30363d")
        apply_layout(fig, "Actual vs Forecasted Revenue")
        fig.update_xaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_yaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_xaxes(title_text="Month", gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_yaxes(title_text="Revenue (₹)", gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # Revenue Loss Forecast
        all_loss_act = monthly["Revenue_Loss"].tolist() + [None]*horizon
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=all_labels, y=all_loss_act, name="Actual Loss",
                                 mode="lines+markers", line=dict(color="#f85149", width=2.5)))
        fig.add_trace(go.Scatter(x=all_labels, y=all_loss_fct, name="Forecasted Loss",
                                 mode="lines+markers", line=dict(color="#d29922", width=2, dash="dot"),
                                 marker=dict(symbol="diamond", size=7)))
        fig.add_vline(x=monthly["Month_Label"].iloc[-1], line_dash="dash", line_color="#30363d")
        apply_layout(fig, "Actual vs Forecasted Revenue Loss")
        fig.update_xaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_yaxes(gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_xaxes(title_text="Month", gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        fig.update_yaxes(title_text="Revenue Loss (₹)", gridcolor="#21262d", linecolor="#30363d", zerolinecolor="#30363d")
        st.plotly_chart(fig, use_container_width=True)

    # Forecast table
    st.markdown("<div class='section-header'>📋 Forecast Summary Table</div>", unsafe_allow_html=True)
    forecast_table = pd.DataFrame({
        "Month": future_labels,
        "Projected Revenue (₹)": [f"₹{v:,.0f}" for v in rev_forecast],
        "Projected Rev Loss (₹)": [f"₹{v:,.0f}" for v in loss_forecast],
        "Projected Claims":       [f"{v:.0f}" for v in claims_forecast],
    })
    st.dataframe(forecast_table.set_index("Month"), use_container_width=True)


# ─────────────────────────────────────────────────────────────
# MAIN — NAVIGATION
# ─────────────────────────────────────────────────────────────
def main():
    DATA_PATH = "updated_cleaned_claim_dataset.csv"

    with st.spinner("🔄 Loading Medlytics dataset..."):
        df = load_data(DATA_PATH)

    filtered_df = sidebar(df)

    if len(filtered_df) == 0:
        st.warning("⚠️ No data matches the current filters. Please adjust your filter selections.")
        return

    # Navigation
    pages = {
        "🏠 Executive Overview":    page_overview,
        "📋 Claim Analysis":        page_claims,
        "💰 Revenue Integrity":     page_revenue,
        "⚠️ Risk & Anomalies":      page_risk,
        "🏬 Dept & Doctor Drilldown": page_department,
        "📡 Revenue Forecast":      page_forecast,
    }

    # Horizontal top nav via radio
    page_name = st.radio(
        "",
        list(pages.keys()),
        horizontal=True,
        label_visibility="collapsed",
    )
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    pages[page_name](filtered_df)


if __name__ == "__main__":
    main()
