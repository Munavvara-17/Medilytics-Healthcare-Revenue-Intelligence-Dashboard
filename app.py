import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Medilytics | Revenue Intelligence",
    page_icon="Medlogo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CREDENTIALS ───────────────────────────────────────────────────────────────
USERS = {
    "cfo_admin":     {"password":"CFO@2024!",  "role":"CFO",         "name":"Sarah Mitchell",    "title":"Chief Financial Officer"},
    "dept_williams": {"password":"Dept#Head1", "role":"Dept_Head",   "name":"Dr. James Williams","title":"Department Head"},
    "billing_chen":  {"password":"Billing$23", "role":"Billing_Team","name":"Rachel Chen",       "title":"Billing & Coding Lead"},
    "analyst_patel": {"password":"Analyst@99", "role":"Analyst",     "name":"Arjun Patel",       "title":"Revenue Analyst"},
    "auditor_kim":   {"password":"Audit!2024", "role":"Auditor",     "name":"Ji-Won Kim",        "title":"Compliance Auditor"},
}
ROLE_PAGES = {
    "CFO":          ["Executive Overview","Revenue Leakage","Revenue Forecasting","Denial Intelligence","Billing Anomalies"],
    "Dept_Head":    ["Department Overview","Dept Revenue Trends","Patient & LOS Analytics","Revenue Forecasting"],
    "Billing_Team": ["Billing Dashboard","Anomaly Detection","Denial Management","Insurance & Collections"],
    "Analyst":      ["Analytics Hub","Revenue Performance","Revenue Forecasting","Leakage Deep Dive","Procedure Analysis"],
    "Auditor":      ["Compliance Overview","Anomaly Audit","Denial Root Cause","AR & Settlement"],
}

# ── GLOBAL CSS  (theme-aware) ────────────────────────────────────────────────
DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Rajdhani:wght@500;600;700&family=IBM+Plex+Sans:wght@300;400;500;600&family=Share+Tech+Mono&display=swap');
:root{
  --bg:#060B16; --bg2:#0D1528; --bg3:#111E38;
  --sidebar-bg:linear-gradient(180deg,#03060F,#060B16,#040810);
  --border:rgba(0,212,170,.2); --border2:rgba(0,212,170,.35);
  --text:#E8F0FE; --text2:#8892B0; --text3:#5a7a96;
  --primary:#00D4AA; --accent:#4FC3F7;
  --card-bg:linear-gradient(135deg,#0D1528 0%,#111E38 100%);
  --insight-bg:linear-gradient(135deg,rgba(0,212,170,.04),rgba(30,58,95,.18));
  --plot-bg:rgba(15,22,41,0.7);
  --grid:rgba(255,255,255,.04); --gridl:rgba(255,255,255,.08);
}
html,body,[class*="css"]{font-family:'IBM Plex Sans',sans-serif;}
.stApp{background:var(--bg)!important;}
.main .block-container{padding:1.4rem 1.8rem!important;max-width:100%!important;}
[data-testid="stSidebar"]{background:var(--sidebar-bg)!important;border-right:1px solid var(--border);}
[data-testid="stSidebar"] *{color:var(--text)!important;}
@keyframes kpiBorderGlow{0%,100%{border-color:rgba(0,212,170,.2);}50%{border-color:rgba(0,212,170,.55);}}
.kpi-card{background:var(--card-bg);border:1px solid var(--border);border-radius:16px;padding:18px 20px;position:relative;overflow:hidden;transition:transform .2s,box-shadow .2s;animation:kpiBorderGlow 4s ease-in-out infinite;}
.kpi-card:hover{transform:translateY(-3px) scale(1.02);box-shadow:0 0 28px rgba(0,212,170,.25),0 8px 32px rgba(0,0,0,.5);}
.kpi-card::before{content:'';position:absolute;top:0;left:0;width:3px;height:100%;background:linear-gradient(180deg,#00D4AA,#0096c7,transparent);border-radius:16px 0 0 16px;}
.kpi-card::after{content:'';position:absolute;top:-50%;right:-30%;width:100px;height:180%;background:radial-gradient(ellipse,rgba(0,212,170,.06) 0%,transparent 70%);pointer-events:none;}
.kpi-label{font-family:'IBM Plex Sans',sans-serif;font-size:10px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:var(--text3);margin-bottom:8px;}
.kpi-value{font-family:'Rajdhani',sans-serif;font-size:28px;font-weight:700;color:var(--primary);line-height:1;margin-bottom:6px;text-shadow:0 0 20px rgba(0,212,170,.4);letter-spacing:1px;}
.kpi-delta{font-size:11px;font-weight:500;padding:2px 8px;border-radius:20px;display:inline-block;}
.kpi-delta.pos{background:rgba(0,212,170,.15);color:#00D4AA;box-shadow:0 0 8px rgba(0,212,170,.15);}
.kpi-delta.neg{background:rgba(255,71,87,.15);color:#FF4757;box-shadow:0 0 8px rgba(255,71,87,.15);}
.kpi-delta.warn{background:rgba(255,193,7,.15);color:#FFC107;box-shadow:0 0 8px rgba(255,193,7,.15);}
.section-hdr{font-family:'Space Grotesk',sans-serif;font-size:17px;font-weight:700;color:var(--text);margin:18px 0 10px;display:flex;align-items:center;gap:10px;}
.section-hdr::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(0,212,170,.3),transparent);}
.insight{background:var(--insight-bg);border:1px solid rgba(0,212,170,.2);border-left:3px solid #00D4AA;border-radius:10px;padding:14px 16px;margin:12px 0;font-size:13px;color:#C8D8E8;line-height:1.7;box-shadow:inset 0 0 30px rgba(0,212,170,.03),0 2px 12px rgba(0,0,0,.3);}
.insight-ttl{font-weight:700;color:#00D4AA;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:6px;}
@keyframes titleShimmer{0%{background-position:0% 50%}100%{background-position:200% 50%}}
.ptitle{font-family:'Space Grotesk',sans-serif;font-size:28px;font-weight:700;background:linear-gradient(90deg,#00D4AA,#4FC3F7,#00D4AA,#a78bfa,#00D4AA);background-size:300% 100%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:titleShimmer 6s linear infinite;margin-bottom:3px;text-align:center;}
.psub{font-size:13px;color:var(--text3);margin-bottom:18px;text-align:center;}
.sdiv{height:1px;background:linear-gradient(90deg,transparent,var(--border),transparent);margin:10px 0;}
div[data-testid="stRadio"] > div{gap:2px!important;}
div[data-testid="stRadio"] label{background:transparent!important;border-radius:6px!important;padding:7px 10px!important;font-size:13px!important;color:var(--text3)!important;transition:all .15s!important;border:none!important;}
div[data-testid="stRadio"] label:hover{background:rgba(0,212,170,.07)!important;color:#C5D5E8!important;}
div[data-testid="stRadio"] label[data-checked="true"]{background:rgba(0,212,170,.12)!important;color:var(--text)!important;font-weight:600!important;border-left:3px solid #00D4AA!important;}
[data-testid="stSelectbox"]>div>div,[data-testid="stMultiSelect"]>div>div{background:var(--bg2)!important;border:1px solid var(--border)!important;color:var(--text)!important;border-radius:8px!important;}
::-webkit-scrollbar{width:4px;}::-webkit-scrollbar-thumb{background:rgba(0,212,170,.25);border-radius:4px;}
/* Chart border glow — dark mode */
@keyframes chartGlowD{0%,100%{box-shadow:0 0 0 1.5px rgba(0,212,170,.12),0 8px 32px rgba(0,0,0,.35);}50%{box-shadow:0 0 0 2px rgba(0,212,170,.3),0 8px 36px rgba(0,0,0,.4),0 0 24px rgba(0,212,170,.08);}}
[data-testid="stPlotlyChart"]{border-radius:12px;overflow:hidden;border:1.5px solid rgba(0,212,170,.15);animation:chartGlowD 5s ease-in-out infinite;}
[data-testid="stPlotlyChart"]:hover{border-color:rgba(0,212,170,.45)!important;box-shadow:0 0 0 2px rgba(0,212,170,.3),0 8px 40px rgba(0,0,0,.5),0 0 36px rgba(0,212,170,.1)!important;animation:none;}
[data-testid="stDataFrame"]{border-radius:10px;overflow:hidden;border:1.5px solid rgba(0,212,170,.12);box-shadow:0 4px 20px rgba(0,0,0,.3);}
/* ── Dropdown popup — the floating list portal (renders outside sidebar) for DARK MODE ── */
[data-baseweb="popover"]{background:#0D1528!important;border-radius:10px!important;box-shadow:0 8px 36px rgba(0,0,0,.4)!important;border:1.5px solid rgba(0,212,170,.2)!important;}
[data-baseweb="popover"] *{background:#0D1528!important;color:#E8F0FE!important;}
[data-baseweb="menu"]{background:#0D1528!important;border-radius:10px!important;}
[data-baseweb="menu"] ul{background:#0D1528!important;padding:4px!important;}
[data-baseweb="menu"] li{background:#0D1528!important;color:#E8F0FE!important;font-size:13px!important;border-radius:6px!important;padding:9px 12px!important;margin:1px 0!important;}
[data-baseweb="menu"] li:hover{background:rgba(0,212,170,.15)!important;color:#00D4AA!important;}
[data-baseweb="menu"] li[aria-selected="true"]{background:rgba(0,212,170,.25)!important;color:#00D4AA!important;font-weight:600!important;}
[data-baseweb="menu"] li:first-child{font-weight:700!important;color:#00D4AA!important;border-bottom:1px solid rgba(0,212,170,.2)!important;margin-bottom:3px!important;}
[role="listbox"]{background:#0D1528!important;color:#E8F0FE!important;border-radius:10px!important;box-shadow:0 8px 36px rgba(0,0,0,.4)!important;}
[role="listbox"] *{background:#0D1528!important;color:#E8F0FE!important;}
[role="option"]{background:#0D1528!important;color:#E8F0FE!important;font-size:13px!important;padding:9px 12px!important;}
[role="option"]:hover,[role="option"][aria-selected="true"]{background:rgba(0,212,170,.2)!important;color:#00D4AA!important;}
div[data-testid="stMultiSelect"] ul,div[data-testid="stMultiSelect"] li{background:#0D1528!important;color:#E8F0FE!important;}
div[data-testid="stSelectbox"] ul,div[data-testid="stSelectbox"] li{background:#0D1528!important;color:#E8F0FE!important;}

/* ── All buttons in dark mode — matching aesthetic ── */
.stButton>button{
  background:#0D1528!important;
  border:1.5px solid rgba(0,212,170,.3)!important;
  color:#E8F0FE!important;
  border-radius:8px!important;
  font-size:13px!important;
  font-weight:600!important;
  transition:all .2s!important;
  box-shadow:0 1px 4px rgba(0,0,0,.2)!important;
}
.stButton>button:hover{
  background:rgba(0,212,170,.08)!important;
  border-color:rgba(0,212,170,.6)!important;
  color:#00D4AA!important;
  box-shadow:0 3px 12px rgba(0,212,170,.25)!important;
}
.stButton>button[kind="primary"]{
  background:linear-gradient(135deg,#00D4AA 0%,#0096c7 100%)!important;
  border:none!important;color:#FFFFFF!important;
  box-shadow:0 4px 16px rgba(0,212,170,.4)!important;
}
.stButton>button[kind="primary"]:hover{
  box-shadow:0 6px 24px rgba(0,212,170,.6)!important;
  transform:translateY(-1px)!important;
  color:#FFFFFF!important;
}
</style>
"""

LIGHT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Rajdhani:wght@500;600;700&family=IBM+Plex+Sans:wght@300;400;500;600&family=Share+Tech+Mono&display=swap');
:root{
  --bg:#F0F4F8; --bg2:#FFFFFF; --bg3:#E8EEF4;
  --sidebar-bg:linear-gradient(180deg,#F8FAFB,#FFFFFF,#F4F8FC);
  --border:rgba(0,130,105,.22); --border2:rgba(0,130,105,.4);
  --text:#1A2744; --text2:#4A6080; --text3:#6080A0;
  --primary:#009B7D; --accent:#0077A8;
  --card-bg:linear-gradient(135deg,#FFFFFF 0%,#F5F9FF 100%);
  --insight-bg:linear-gradient(135deg,rgba(0,155,125,.05),rgba(0,100,180,.05));
  --plot-bg:rgba(248,252,255,0.98);
  --grid:rgba(0,0,0,.06); --gridl:rgba(0,0,0,.1);
}
html,body,[class*="css"]{font-family:'IBM Plex Sans',sans-serif;}
.stApp{background:var(--bg)!important;}
.main .block-container{padding:1.4rem 1.8rem!important;max-width:100%!important;}

/* ── Sidebar — light ── */
[data-testid="stSidebar"]{background:var(--sidebar-bg)!important;border-right:1.5px solid rgba(0,130,105,.18)!important;}
[data-testid="stSidebar"] *{color:#1A2744!important;}

/* ── KPI cards ── */
.kpi-card{background:#FFFFFF;border:1.5px solid rgba(0,130,105,.2);border-radius:16px;padding:18px 20px;position:relative;overflow:hidden;transition:transform .2s,box-shadow .2s;box-shadow:0 2px 12px rgba(0,0,0,.07);}
.kpi-card:hover{transform:translateY(-3px) scale(1.02);box-shadow:0 6px 24px rgba(0,130,105,.15);}
.kpi-card::before{content:'';position:absolute;top:0;left:0;width:3px;height:100%;background:linear-gradient(180deg,#009B7D,#0077A8,transparent);border-radius:16px 0 0 16px;}
.kpi-label{font-size:10px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:#7090A0;margin-bottom:8px;}
.kpi-value{font-family:'Rajdhani',sans-serif;font-size:28px;font-weight:700;color:#009B7D;line-height:1;margin-bottom:6px;letter-spacing:1px;}
.kpi-delta{font-size:11px;font-weight:500;padding:2px 8px;border-radius:20px;display:inline-block;}
.kpi-delta.pos{background:rgba(0,130,105,.12);color:#007A62;}
.kpi-delta.neg{background:rgba(200,40,40,.1);color:#B03020;}
.kpi-delta.warn{background:rgba(180,120,0,.1);color:#906000;}

/* ── Section headers ── */
.section-hdr{font-family:'Space Grotesk',sans-serif;font-size:17px;font-weight:700;color:#1A2744;margin:18px 0 10px;display:flex;align-items:center;gap:10px;}
.section-hdr::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(0,130,105,.25),transparent);}

/* ── Insight box ── */
.insight{background:linear-gradient(135deg,rgba(0,130,105,.05),rgba(0,80,160,.04));border:1px solid rgba(0,130,105,.2);border-left:3px solid #009B7D;border-radius:10px;padding:14px 16px;margin:12px 0;font-size:13px;color:#2A3F5A;line-height:1.7;}
.insight-ttl{font-weight:700;color:#009B7D;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:6px;}

/* ── Page title ── */
@keyframes titleShimmerL{0%{background-position:0% 50%}100%{background-position:200% 50%}}
.ptitle{font-family:'Space Grotesk',sans-serif;font-size:28px;font-weight:700;background:linear-gradient(90deg,#009B7D,#0077A8,#009B7D,#5050C0,#009B7D);background-size:300% 100%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:titleShimmerL 6s linear infinite;margin-bottom:3px;text-align:center;}
.psub{font-size:13px;color:#6080A0;margin-bottom:18px;text-align:center;}
.sdiv{height:1px;background:linear-gradient(90deg,transparent,rgba(0,130,105,.2),transparent);margin:10px 0;}

/* ── Sidebar nav ── */
div[data-testid="stRadio"] > div{gap:2px!important;}
div[data-testid="stRadio"] label{background:transparent!important;border-radius:6px!important;padding:7px 10px!important;font-size:13px!important;color:#4A6080!important;transition:all .15s!important;border:none!important;}
div[data-testid="stRadio"] label:hover{background:rgba(0,130,105,.08)!important;color:#1A2744!important;}
div[data-testid="stRadio"] label[data-checked="true"]{background:rgba(0,130,105,.1)!important;color:#009B7D!important;font-weight:600!important;border-left:3px solid #009B7D!important;}

/* ── Filters — white bg, dark text, green border ── */
[data-testid="stSelectbox"]>div>div{background:#FFFFFF!important;border:1.5px solid rgba(0,130,105,.25)!important;color:#1A2744!important;border-radius:8px!important;box-shadow:0 1px 4px rgba(0,0,0,.06)!important;}
[data-testid="stMultiSelect"]>div>div{background:#FFFFFF!important;border:1.5px solid rgba(0,130,105,.25)!important;color:#1A2744!important;border-radius:8px!important;box-shadow:0 1px 4px rgba(0,0,0,.06)!important;}
[data-testid="stMultiSelect"] span[data-baseweb="tag"]{background:rgba(0,130,105,.12)!important;color:#007A62!important;border-radius:4px!important;}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] span{color:#007A62!important;}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] button{color:#007A62!important;}
[data-testid="stDateInput"]>div>div>input{background:#FFFFFF!important;border:1.5px solid rgba(0,130,105,.25)!important;color:#1A2744!important;border-radius:8px!important;}
[data-testid="stWidgetLabel"] p{color:#4A6080!important;font-size:12px!important;}
div[data-testid="stDateInput"] label p{color:#4A6080!important;}
/* Multiselect input text */
[data-testid="stMultiSelect"] input{color:#1A2744!important;background:transparent!important;}
[data-testid="stMultiSelect"] input::placeholder{color:#9BAFC0!important;}
/* Selectbox selected value text */
[data-testid="stSelectbox"] div[data-baseweb="select"] div{color:#1A2744!important;}

/* ── Dropdown popup — the floating list portal (renders outside sidebar) ── */
/* Target every possible baseweb popup/menu/listbox element */
[data-baseweb="popover"]{background:#FFFFFF!important;border-radius:10px!important;box-shadow:0 8px 36px rgba(0,0,0,.14)!important;border:1.5px solid rgba(0,130,105,.2)!important;}
[data-baseweb="popover"] *{background:#FFFFFF!important;color:#1A2744!important;}
[data-baseweb="menu"]{background:#FFFFFF!important;border-radius:10px!important;}
[data-baseweb="menu"] ul{background:#FFFFFF!important;padding:4px!important;}
[data-baseweb="menu"] li{background:#FFFFFF!important;color:#1A2744!important;font-size:13px!important;border-radius:6px!important;padding:9px 12px!important;margin:1px 0!important;}
[data-baseweb="menu"] li:hover{background:rgba(0,130,105,.09)!important;color:#009B7D!important;}
[data-baseweb="menu"] li[aria-selected="true"]{background:rgba(0,130,105,.12)!important;color:#009B7D!important;font-weight:600!important;}
[data-baseweb="menu"] li:first-child{font-weight:700!important;color:#009B7D!important;border-bottom:1px solid rgba(0,130,105,.1)!important;margin-bottom:3px!important;}
/* Listbox (alternate dropdown renderer) */
[data-baseweb="list"],[role="listbox"]{background:#FFFFFF!important;color:#1A2744!important;border-radius:10px!important;box-shadow:0 8px 36px rgba(0,0,0,.14)!important;}
[role="listbox"] *{background:#FFFFFF!important;color:#1A2744!important;}
[role="option"]{background:#FFFFFF!important;color:#1A2744!important;font-size:13px!important;padding:9px 12px!important;}
[role="option"]:hover,[role="option"][aria-selected="true"]{background:rgba(0,130,105,.1)!important;color:#009B7D!important;}
/* Overriding any dark stray bg on dropdowns */
div[data-testid="stMultiSelect"] ul,div[data-testid="stMultiSelect"] li{background:#FFFFFF!important;color:#1A2744!important;}
div[data-testid="stSelectbox"] ul,div[data-testid="stSelectbox"] li{background:#FFFFFF!important;color:#1A2744!important;}

/* ── All buttons in light mode — white with dark text ── */
.stButton>button{
  background:#FFFFFF!important;
  border:1.5px solid rgba(0,130,105,.3)!important;
  color:#1A2744!important;
  border-radius:8px!important;
  font-size:13px!important;
  font-weight:600!important;
  transition:all .2s!important;
  box-shadow:0 1px 4px rgba(0,0,0,.08)!important;
}
.stButton>button:hover{
  background:#F0FAF7!important;
  border-color:rgba(0,130,105,.5)!important;
  color:#009B7D!important;
  box-shadow:0 3px 12px rgba(0,130,105,.15)!important;
}
/* Sign In button override — keep it green with white text */
.stButton>button[kind="primary"]{
  background:linear-gradient(135deg,#009B7D 0%,#0077A8 100%)!important;
  border:none!important;color:#FFFFFF!important;
  box-shadow:0 4px 16px rgba(0,130,105,.35)!important;
}
.stButton>button[kind="primary"]:hover{
  box-shadow:0 6px 24px rgba(0,130,105,.5)!important;
  transform:translateY(-1px)!important;
  color:#FFFFFF!important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar{width:4px;}::-webkit-scrollbar-thumb{background:rgba(0,130,105,.25);border-radius:4px;}

/* ── Chart boxes — solid visible border + glow animation ── */
@keyframes chartGlowL{
  0%,100%{box-shadow:0 0 0 1.5px rgba(0,130,105,.2),0 4px 16px rgba(0,0,0,.08);}
  50%{box-shadow:0 0 0 2px rgba(0,130,105,.4),0 4px 20px rgba(0,130,105,.1);}
}
[data-testid="stPlotlyChart"]{
  border-radius:12px;overflow:hidden;
  border:1.5px solid rgba(0,130,105,.2);
  animation:chartGlowL 5s ease-in-out infinite;
}
[data-testid="stPlotlyChart"]:hover{
  border-color:rgba(0,130,105,.5)!important;
  box-shadow:0 0 0 2px rgba(0,130,105,.3),0 6px 28px rgba(0,0,0,.12)!important;
  animation:none;
}
[data-testid="stDataFrame"]{
  border-radius:10px;overflow:hidden;
  border:1.5px solid rgba(0,130,105,.18);
  box-shadow:0 2px 12px rgba(0,0,0,.07);
}
</style>
"""

def inject_theme():
    dark = st.session_state.get("dark_mode", True)
    st.markdown(DARK_CSS if dark else LIGHT_CSS, unsafe_allow_html=True)
    
    # Inject a MutationObserver to catch portal dropdowns (rendered at body root,
    # outside the sidebar/component tree) and force theme-aware colors on them.
    if dark:
        patch_css = """
        [data-baseweb="popover"] { background:#0D1528 !important; border:1.5px solid rgba(0,212,170,.2) !important; border-radius:10px !important; box-shadow:0 8px 36px rgba(0,0,0,.4) !important; }
        [data-baseweb="popover"] * { background:#0D1528 !important; color:#E8F0FE !important; }
        [data-baseweb="menu"] { background:#0D1528 !important; }
        [data-baseweb="menu"] ul { background:#0D1528 !important; padding:4px !important; }
        [data-baseweb="menu"] li { background:#0D1528 !important; color:#E8F0FE !important; font-size:13px !important; border-radius:6px !important; padding:9px 12px !important; }
        [data-baseweb="menu"] li:hover { background:rgba(0,212,170,.15) !important; color:#00D4AA !important; }
        [data-baseweb="menu"] li[aria-selected="true"] { background:rgba(0,212,170,.25) !important; color:#00D4AA !important; font-weight:600 !important; }
        [role="listbox"] { background:#0D1528 !important; border-radius:10px !important; box-shadow:0 8px 36px rgba(0,0,0,.4) !important; border:1.5px solid rgba(0,212,170,.2) !important; }
        [role="listbox"] * { background:#0D1528 !important; color:#E8F0FE !important; }
        [role="option"] { background:#0D1528 !important; color:#E8F0FE !important; font-size:13px !important; padding:9px 14px !important; }
        [role="option"]:hover,[role="option"][aria-selected="true"] { background:rgba(0,212,170,.2) !important; color:#00D4AA !important; }
        """
        bg_color = "#0D1528"
        tx_color = "#E8F0FE"
    else:
        patch_css = """
        [data-baseweb="popover"] { background:#FFFFFF !important; border:1.5px solid rgba(0,130,105,.22) !important; border-radius:10px !important; box-shadow:0 8px 36px rgba(0,0,0,.14) !important; }
        [data-baseweb="popover"] * { background:#FFFFFF !important; color:#1A2744 !important; }
        [data-baseweb="menu"] { background:#FFFFFF !important; }
        [data-baseweb="menu"] ul { background:#FFFFFF !important; padding:4px !important; }
        [data-baseweb="menu"] li { background:#FFFFFF !important; color:#1A2744 !important; font-size:13px !important; border-radius:6px !important; padding:9px 12px !important; }
        [data-baseweb="menu"] li:hover { background:rgba(0,130,105,.09) !important; color:#009B7D !important; }
        [data-baseweb="menu"] li[aria-selected="true"] { background:rgba(0,130,105,.12) !important; color:#009B7D !important; font-weight:600 !important; }
        [role="listbox"] { background:#FFFFFF !important; border-radius:10px !important; box-shadow:0 8px 36px rgba(0,0,0,.14) !important; border:1.5px solid rgba(0,130,105,.2) !important; }
        [role="listbox"] * { background:#FFFFFF !important; color:#1A2744 !important; }
        [role="option"] { background:#FFFFFF !important; color:#1A2744 !important; font-size:13px !important; padding:9px 14px !important; }
        [role="option"]:hover,[role="option"][aria-selected="true"] { background:rgba(0,130,105,.1) !important; color:#009B7D !important; }
        """
        bg_color = "#FFFFFF"
        tx_color = "#1A2744"

    st.markdown(f"""
<script>
(function patchDropdowns(){{
  var style = document.getElementById('ml-dropdown-patch');
  if(!style){{
    style = document.createElement('style');
    style.id = 'ml-dropdown-patch';
    document.head.appendChild(style);
  }}
  style.textContent = `{patch_css}`;
  
  // Clean existing observer if any to avoid stacking multiple intervals
  if (window.mlObserver) window.mlObserver.disconnect();
  
  // MutationObserver: re-apply whenever new popup nodes are added to body
  window.mlObserver = new MutationObserver(function(muts){{
    muts.forEach(function(m){{
      m.addedNodes.forEach(function(n){{
        if(n.nodeType===1){{
          var els = n.querySelectorAll ? n.querySelectorAll('[data-baseweb="popover"],[data-baseweb="menu"],[role="listbox"],[role="option"]') : [];
          els.forEach(function(el){{
            el.style.setProperty('background','{bg_color}','important');
            el.style.setProperty('color','{tx_color}','important');
          }});
          if(n.dataset && (n.dataset.baseweb==='popover'||n.dataset.baseweb==='menu')){{
            n.style.setProperty('background','{bg_color}','important');
            n.style.setProperty('color','{tx_color}','important');
          }}
        }}
      }});
    }});
  }});
  window.mlObserver.observe(document.body,{{childList:true,subtree:true}});
}})();
</script>
""", unsafe_allow_html=True)

inject_theme()


# ── DATA ──────────────────────────────────────────────────────────────────────
# ── DATA ──────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    for fname in ["medilytics_data.csv", "pre_processed_data_updated.csv", "pre_processed_data.csv"]:
        try:
            df = pd.read_csv(fname)
            break
        except FileNotFoundError:
            continue
    else:
        st.error("Data file not found. Place medilytics_data.csv in the same folder as app.py.")
        st.stop()

    # ── Column name normalisation (new dataset uses Revenue_At_Risk) ──────────
    if "Revenue_At_Risk" in df.columns and "Revenue_at_Risk" not in df.columns:
        df["Revenue_at_Risk"] = df["Revenue_At_Risk"]
    if "Revenue_Loss" in df.columns and "Revenue_Leakage" not in df.columns:
        df["Revenue_Leakage"] = df["Revenue_Loss"]

    # ── Parse dates ───────────────────────────────────────────────────────────
    for col in ["Admission_Date","Discharge_Date","Claim_Submission_Date","Settlement_Date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")

    # ── Time columns ──────────────────────────────────────────────────────────
    if "Admission_Date" in df.columns:
        df["Year"]       = df["Admission_Date"].dt.year
        df["Month_Num"]  = df["Admission_Date"].dt.month
        df["Month_Year"] = df["Admission_Date"].dt.strftime("%Y-%m")
        df["Quarter"]    = df["Admission_Date"].dt.quarter
        df["YearQ"]      = df["Year"].astype(str) + "-Q" + df["Quarter"].astype(str)
    elif "Month" in df.columns:
        # New dataset has Month as YYYY-MM string
        df["Month_Year"] = df["Month"].astype(str)
        df["Year"]       = df["Month_Year"].str[:4].astype(int)
        df["Month_Num"]  = df["Month_Year"].str[5:7].astype(int)
        df["Quarter"]    = ((df["Month_Num"]-1)//3 + 1)
        df["YearQ"]      = df["Year"].astype(str) + "-Q" + df["Quarter"].astype(str)

    if "Month_Year" in df.columns:
        df = df.dropna(subset=["Month_Year"]).reset_index(drop=True)

    # ── Financial columns ─────────────────────────────────────────────────────
    if "Collection_Rate" not in df.columns:
        if "Payment_Received" in df.columns and "Billing_Amount" in df.columns:
            df["Collection_Rate"] = (df["Payment_Received"] / df["Billing_Amount"].replace(0, pd.NA) * 100).round(2)
        elif "Approval_Rate" in df.columns:
            df["Collection_Rate"] = (df["Approval_Rate"] * 100).clip(0, 100).round(2)

    if "Net_Revenue" not in df.columns and "Actual_Revenue" in df.columns:
        df["Net_Revenue"] = df["Actual_Revenue"]

    if "Revenue_Leakage_Index" not in df.columns and "Revenue_Leakage" in df.columns and "Expected_Revenue" in df.columns:
        df["Revenue_Leakage_Index"] = (df["Revenue_Leakage"] / df["Expected_Revenue"].replace(0, pd.NA) * 100).round(3)

    # ── Denial columns ────────────────────────────────────────────────────────
    if "Denial_Amount" not in df.columns and "Claim_Amount" in df.columns and "Denial_Flag" in df.columns:
        df["Denial_Amount"] = df["Claim_Amount"] * df["Denial_Flag"]

    # ── Billing anomaly — use High_Risk_Claim + Claim_Gap + Revenue_Loss ──────
    # This dataset's billing ratio has NO variance (all 0.95–1.00), so we use
    # the actual pre-computed risk/gap columns instead.
    if "High_Risk_Claim" in df.columns:
        # Primary signal: High_Risk_Claim flag from dataset
        df["Billing_Anomaly"] = df["High_Risk_Claim"].astype(int)

        # Classify anomaly type using Claim_Gap and Payment_Gap
        df["Anomaly_Type"] = "Normal"
        if "Claim_Gap" in df.columns and "Payment_Gap" in df.columns:
            cg_thresh = df["Claim_Gap"].quantile(0.80)
            pg_thresh = df["Payment_Gap"].quantile(0.20)   # negative = underpaid
            df.loc[(df["Billing_Anomaly"]==1) & (df["Claim_Gap"] > cg_thresh), "Anomaly_Type"] = "Overbilling"
            df.loc[(df["Billing_Anomaly"]==1) & (df["Payment_Gap"] < pg_thresh), "Anomaly_Type"] = "Underpayment"
            df.loc[(df["Billing_Anomaly"]==1) & (df["Anomaly_Type"]=="Normal"), "Anomaly_Type"] = "Claim Mismatch"
    else:
        # Fallback: statistical outlier on Revenue_Loss
        if "Revenue_Loss" in df.columns:
            rl = df["Revenue_Loss"]
            thresh = rl.mean() + 1.5 * rl.std()
            df["Billing_Anomaly"] = (rl > thresh).astype(int)
        else:
            df["Billing_Anomaly"] = 0
        df["Anomaly_Type"] = "Normal"
        df.loc[df["Billing_Anomaly"]==1, "Anomaly_Type"] = "Revenue Anomaly"

    # ── Denial risk score ─────────────────────────────────────────────────────
    if "Denial_Risk_Score" not in df.columns:
        ins_map = {"Self-Pay":3,"Government":2,"Corporate":1,"Private":1}
        ins_sc  = df["Insurance_Type"].map(ins_map).fillna(1) if "Insurance_Type" in df.columns else 1
        doc_del = df["Documentation_Delay_Days"] if "Documentation_Delay_Days" in df.columns else 0
        prev_d  = df["Previous_Denial_Count"]    if "Previous_Denial_Count"    in df.columns else 0
        los_sc  = (df["Length_of_Stay"]/30)       if "Length_of_Stay"           in df.columns else 0
        df["Denial_Risk_Score"] = (prev_d*0.35 + doc_del*0.05 + los_sc*0.20 + ins_sc*0.10).round(3)

    if "Denial_Risk_Category" not in df.columns and "Denial_Risk_Score" in df.columns:
        df["Denial_Risk_Category"] = pd.cut(
            df["Denial_Risk_Score"], bins=[-1,0.33,0.66,999],
            labels=["Low Risk","Medium Risk","High Risk"])

    # Use High_Risk_Claim as Denial_Risk_Category override if available
    if "High_Risk_Claim" in df.columns and "Denial_Risk_Category" not in df.columns:
        df["Denial_Risk_Category"] = df["High_Risk_Claim"].map({True:"High Risk",False:"Low Risk"})

    if "Charge_Capture_Efficiency" not in df.columns and "Actual_Revenue" in df.columns:
        df["Charge_Capture_Efficiency"] = (
            df["Actual_Revenue"] / df["Expected_Revenue"].replace(0, pd.NA) * 100
        ).clip(0,100).round(2)

    # ── Accounts_Receivable_Days from Processing_Days if missing ─────────────
    if "Accounts_Receivable_Days" not in df.columns and "Processing_Days" in df.columns:
        df["Accounts_Receivable_Days"] = df["Processing_Days"]
    if "Settlement_Days" not in df.columns and "Processing_Days" in df.columns:
        df["Settlement_Days"] = df["Processing_Days"]

    return df

# ── CHART LAYOUT HELPER ───────────────────────────────────────────────────────
def cl(extra=None):
    dark = st.session_state.get("dark_mode", True)
    if dark:
        base = dict(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(13,21,40,0.85)",
            font=dict(family="IBM Plex Sans,sans-serif", color="#8892B0", size=11),
            xaxis=dict(gridcolor="rgba(255,255,255,.04)", linecolor="rgba(255,255,255,.08)", tickfont=dict(size=10)),
            yaxis=dict(gridcolor="rgba(255,255,255,.04)", linecolor="rgba(255,255,255,.08)", tickfont=dict(size=10)),
            margin=dict(l=10, r=10, t=36, b=10),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#8892B0", size=10)),
            hoverlabel=dict(bgcolor="#141C33", bordercolor="#00D4AA", font=dict(color="#E8F0FE")),
        )
    else:
        base = dict(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(248,252,255,0.95)",
            font=dict(family="IBM Plex Sans,sans-serif", color="#4A6080", size=11),
            xaxis=dict(gridcolor="rgba(0,0,0,.06)", linecolor="rgba(0,0,0,.1)", tickfont=dict(size=10)),
            yaxis=dict(gridcolor="rgba(0,0,0,.06)", linecolor="rgba(0,0,0,.1)", tickfont=dict(size=10)),
            margin=dict(l=10, r=10, t=36, b=10),
            legend=dict(bgcolor="rgba(255,255,255,.7)", font=dict(color="#4A6080", size=10)),
            hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#009B7D", font=dict(color="#1A2744")),
        )
    if extra:
        base.update(extra)
    return base

CS = ["#00D4AA","#4FC3F7","#FF6B35","#A78BFA","#FFC107","#FF4757","#34D399","#60A5FA"]
CD = {"Cardiology":"#FF4757","Neurology":"#A78BFA","Orthopedics":"#4FC3F7","Emergency":"#FF6B35","General Medicine":"#00D4AA"}

# ── HELPERS ───────────────────────────────────────────────────────────────────
def kpi_card(label, value, delta="", dtype="pos"):
    d = f'<div class="kpi-delta {dtype}">{delta}</div>' if delta else ""
    return f'<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div>{d}</div>'

def kpis(cards):
    cols = st.columns(len(cards))
    for col, (l, v, d, dt) in zip(cols, cards):
        col.markdown(kpi_card(l, v, d, dt), unsafe_allow_html=True)

def shdr(t):
    st.markdown(f'<div class="section-hdr">{t}</div>', unsafe_allow_html=True)

def ins(title, text):
    st.markdown(f'<div class="insight"><div class="insight-ttl">{title}</div>{text}</div>', unsafe_allow_html=True)

def ptitle(t, sub):
    st.markdown(f'<div class="ptitle">{t}</div><div class="psub">{sub}</div>', unsafe_allow_html=True)

def arima_forecast(series, steps=6):
    try:
        from statsmodels.tsa.arima.model import ARIMA
        res = ARIMA(series, order=(2,1,1)).fit()
        fc  = res.forecast(steps)
        ci  = res.get_forecast(steps).conf_int()
        return fc.values, ci.iloc[:,0].values, ci.iloc[:,1].values
    except Exception:
        vals = series.values.astype(float)
        sm   = [vals[0]]
        for v in vals[1:]:
            sm.append(0.3*v + 0.7*sm[-1])
        trend = np.polyfit(range(len(vals)), vals, 1)
        fc    = [sm[-1] + trend[0]*(i+1) for i in range(steps)]
        noise = np.std(np.diff(vals)) * 1.6
        lo    = [f - noise*(1+0.1*i) for i, f in enumerate(fc)]
        hi    = [f + noise*(1+0.1*i) for i, f in enumerate(fc)]
        return np.array(fc), np.array(lo), np.array(hi)

# ── LOGIN PAGE ────────────────────────────────────────────────────────────────
def login_page():
    import base64, os
    
    # ── Theme values explicitly set to stunning Dark Mode ─────────────────────
    input_bg    = "rgba(255,255,255,.07)"
    input_bdr   = "rgba(0,212,170,.32)"
    input_focus = "#00D4AA"
    input_col   = "#E8F0FE"
    input_ph    = "rgba(100,160,200,.55)"
    btn_grad    = "linear-gradient(135deg,#00c99a,#0088bb)"
    btn_sh      = "0 6px 28px rgba(0,212,170,.45)"
    glass_bg    = "rgba(6,14,32,.75)"
    glass_bdr   = "rgba(0,212,170,.28)"
    glass_sh    = "0 24px 80px rgba(0,0,0,.65),inset 0 1px 0 rgba(0,212,170,.15)"
    t_col       = "#E8F0FE"; s_col = "rgba(0,212,170,.7)"; lbl = "#5a8aaa"
    div_c       = "linear-gradient(90deg,transparent,rgba(0,212,170,.3),transparent)"

    # ── Logo as base64 ────────────────────────────────────────────────────────
    logo_html = ""
    for path in ["Medlogo.png","medlogo.png","logo.png"]:
        if os.path.exists(path):
            with open(path,"rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            logo_html = f'<img src="data:image/png;base64,{b64}" style="height:62px;display:block;margin:0 auto 14px;" />'
            break
    if not logo_html:
        logo_html = f'<p style="text-align:center;font-size:28px;font-weight:800;color:#00D4AA;margin:0 0 14px;font-family:Space Grotesk,sans-serif;letter-spacing:3px;">MEDILYTICS</p>'

    # ── Full-page CSS ─────────────────────────────────────────────────────────
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700;800&family=IBM+Plex+Sans:wght@400;500;600&display=swap');
.stApp{{background:transparent!important;}}
.main .block-container{{padding:0!important;max-width:100%!important;}}
header[data-testid="stHeader"]{{display:none!important;}}
footer{{display:none!important;}}
/* hide all Streamlit widget labels */
.stTextInput label,.stForm label{{display:none!important;}}
[data-testid="stForm"]{{background:transparent!important;border:none!important;padding:0!important;}}
/* inputs */
.stTextInput>div>div>input{{
  background:{input_bg}!important;border:1.5px solid {input_bdr}!important;
  border-radius:12px!important;color:{input_col}!important;
  font-size:15px!important;font-family:'IBM Plex Sans',sans-serif!important;
  padding:13px 18px!important;transition:all .25s!important;
  backdrop-filter:blur(8px)!important;-webkit-backdrop-filter:blur(8px)!important;
}}
.stTextInput>div>div>input:focus{{
  border-color:{input_focus}!important;
  box-shadow:0 0 0 3px rgba(0,200,160,.15),0 0 20px rgba(0,200,160,.1)!important;
}}
.stTextInput>div>div>input::placeholder{{color:{input_ph}!important;font-size:14px!important;}}
/* Sign In */
.stButton>button[kind="primary"]{{
  background:{btn_grad}!important;border:none!important;border-radius:12px!important;
  font-family:'Space Grotesk',sans-serif!important;font-size:15px!important;font-weight:700!important;
  height:52px!important;letter-spacing:3px!important;text-transform:uppercase!important;
  color:#FFFFFF!important;box-shadow:{btn_sh}!important;transition:all .25s!important;
}}
.stButton>button[kind="primary"]:hover{{
  transform:translateY(-2px) scale(1.01)!important;
  box-shadow:0 12px 36px rgba(0,200,160,.55)!important;
}}

</style>
""", unsafe_allow_html=True)

    # ── Animated video background & perfectly aligned glass card ─────────────
    st.markdown("""
<style>
/* Center the main container heavily on the screen */
div[data-testid="stAppViewContainer"] {
    display: flex; justify-content: center; align-items: center; min-height: 100vh;
}
/* Turn the global block-container into the glassmorphism box! */
.main .block-container {
    width: 100% !important; max-width: 440px !important;
    background: rgba(6, 14, 32, 0.75) !important;
    border: 1.5px solid rgba(0, 212, 170, 0.28) !important;
    border-radius: 24px !important;
    padding: 40px 45px 35px !important;
    backdrop-filter: blur(25px) !important; -webkit-backdrop-filter: blur(25px) !important;
    box-shadow: 0 24px 80px rgba(0,0,0,0.8), inset 0 1px 0 rgba(0,212,170,0.15) !important;
    animation: slideUp .7s cubic-bezier(.16,1,.3,1) both !important;
    position: relative !important; overflow: hidden !important;
    margin: auto !important;
}
@keyframes slideUp{from{opacity:0;transform:translateY(32px) scale(.96)}to{opacity:1;transform:none}}

/* Top Sweep Line inside the box */
.main .block-container::before {
    content:''; display: block; position: absolute; top:0; left:0; width: 100%; height: 3px;
    background: linear-gradient(90deg, transparent, #00D4AA, #4FC3F7, transparent);
    animation: sweep 3s ease-in-out infinite; z-index: 99;
}
@keyframes sweep{0%{transform:translateX(-100%)}100%{transform:translateX(250%)}}
</style>

<!-- Background Animation Canvas -->
<canvas id="lgBg" style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:-10;pointer-events:none;"></canvas>
""", unsafe_allow_html=True)
    import urllib.parse
    bg_js = """
(function(){
  var C=document.getElementById('lgBg') || window.parent.document.getElementById('lgBg');
  if(!C)return;
  var ctx=C.getContext('2d'),W=0,H=0,tick=0,ecgH=[],ecgOff=0;
  var M={x:0, y:0, active:false};
  var seg=[[0,0],[.08,0],[.11,-.08],[.14,.10],[.17,0],
           [.28,0],[.30,-.72],[.32,0],[.34,-.13],
           [.36,1.18],[.39,-.16],[.42,0],[.45,-.34],[.50,0],
           [.57,0],[.62,.28],[.68,.28],[.73,0],[1,0]];
  var pts=[];
  function Pt(){this.x=Math.random()*W;this.y=Math.random()*H;
    this.vx=(Math.random()-.5)*.35;this.vy=(Math.random()-.5)*.35;
    this.r=Math.random()*1.6+.4;this.a=Math.random()*.4+.1;
    this.ph=Math.random()*6.28;}
  function resize(){
    W=C.width=window.innerWidth;H=C.height=window.innerHeight;
    if(!pts.length)for(var i=0;i<100;i++)pts.push(new Pt());
  }
  resize();window.addEventListener('resize',resize);
  window.addEventListener('mousemove', function(e){ M.x=e.clientX; M.y=e.clientY; M.active=true; });
  window.addEventListener('mouseleave', function(){ M.active=false; });

  function sECG(px){var t=(px%280)/280;
    for(var i=0;i<seg.length-1;i++){
      if(t>=seg[i][0]&&t<=seg[i+1][0])
        return seg[i][1]+(seg[i+1][1]-seg[i][1])*(t-seg[i][0])/(seg[i+1][0]-seg[i][0]+1e-9);
    }return 0;}
  function draw(){
    tick++;ctx.clearRect(0,0,W,H);
    var g=ctx.createLinearGradient(0,0,W,H);
    g.addColorStop(0,'#030811');g.addColorStop(1,'#060E20');
    ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
    function blob(x,y,r,c){var bg=ctx.createRadialGradient(x,y,0,x,y,r);
      bg.addColorStop(0,c);bg.addColorStop(1,'rgba(0,0,0,0)');
      ctx.fillStyle=bg;ctx.beginPath();ctx.arc(x,y,r,0,6.28);ctx.fill();}
    blob(W*.18,H*.22,H*.55,'rgba(0,180,140,.065)');
    blob(W*.82,H*.72,H*.42,'rgba(0,90,200,.045)');
    
    if (M.active) { blob(M.x, M.y, 250, 'rgba(0,212,170,.08)'); }

    for(var i=0;i<pts.length;i++){
      var p=pts[i]; p.x+=p.vx; p.y+=p.vy; p.ph+=.007;
      if(p.x<-10)p.x=W+10; if(p.x>W+10)p.x=-10;
      if(p.y<-10)p.y=H+10; if(p.y>H+10)p.y=-10;
      
      if (M.active) {
        var dxM=p.x-M.x, dyM=p.y-M.y, dM=Math.sqrt(dxM*dxM+dyM*dyM);
        if(dM<180){
          ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(M.x,M.y);
          ctx.strokeStyle='rgba(0,212,170,'+((1-dM/180)*.25)+')';ctx.lineWidth=1.2;ctx.stroke();
          p.x -= dxM*0.005; p.y -= dyM*0.005;
        }
      }

      var a=p.a*(.65+.35*Math.sin(p.ph));
      ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,6.28);
      ctx.fillStyle='rgba(0,212,170,'+a+')';ctx.fill();

      for(var j=i+1;j<pts.length;j++){
        var dx=p.x-pts[j].x,dy=p.y-pts[j].y,d=Math.sqrt(dx*dx+dy*dy);
        if(d<115){
          ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(pts[j].x,pts[j].y);
          ctx.strokeStyle='rgba(0,180,140,'+((1-d/115)*.15)+')';ctx.lineWidth=.6;ctx.stroke();
        }
      }
    }
    
    var EY=H*.74,BW=265,AMP=42,SPD=2.5;
    ecgOff+=SPD;
    ecgH.push({x:W,y:EY-sECG(ecgOff)*AMP});
    for(var k=0;k<ecgH.length;k++)ecgH[k].x-=SPD;
    while(ecgH.length&&ecgH[0].x<-8)ecgH.shift();
    if(ecgH.length>1){
      ctx.beginPath();ctx.moveTo(ecgH[0].x,ecgH[0].y);
      for(var e=1;e<ecgH.length;e++)ctx.lineTo(ecgH[e].x,ecgH[e].y);
      ctx.strokeStyle='rgba(0,212,170,.09)';ctx.lineWidth=14;ctx.lineJoin='round';ctx.stroke();
      ctx.beginPath();ctx.moveTo(ecgH[0].x,ecgH[0].y);
      for(var e=1;e<ecgH.length;e++)ctx.lineTo(ecgH[e].x,ecgH[e].y);
      ctx.strokeStyle='rgba(0,212,170,.38)';ctx.lineWidth=3.5;ctx.stroke();
      ctx.beginPath();ctx.moveTo(ecgH[0].x,ecgH[0].y);
      for(var e=1;e<ecgH.length;e++)ctx.lineTo(ecgH[e].x,ecgH[e].y);
      ctx.strokeStyle='#00D4AA';ctx.lineWidth=1.8;ctx.stroke();
      
      var L=ecgH[ecgH.length-1];
      var dg=ctx.createRadialGradient(L.x,L.y,0,L.x,L.y,14);
      dg.addColorStop(0,'rgba(0,212,170,.8)');dg.addColorStop(1,'rgba(0,212,170,0)');
      ctx.fillStyle=dg;ctx.beginPath();ctx.arc(L.x,L.y,14,0,6.28);ctx.fill();
      ctx.beginPath();ctx.arc(L.x,L.y,3.5,0,6.28);ctx.fillStyle='#00ffcc';ctx.fill();
    }
    requestAnimationFrame(draw);
  }
  draw();
})();
"""
    encoded_js = urllib.parse.quote(bg_js)
    st.markdown(f'<img src="x" style="display:none;" onerror="eval(decodeURIComponent(\'{encoded_js}\'))" />', unsafe_allow_html=True)

    # ── Render Login Components directly into the styled container ────────────
    st.markdown(logo_html, unsafe_allow_html=True)
    st.markdown(f"""
<div style="text-align:center;margin-bottom:28px;">
  <h1 style="font-family:'Space Grotesk',sans-serif;font-size:28px;font-weight:800;
     color:#E8F0FE;margin:0 0 7px;letter-spacing:.3px;line-height:1.2;">
     Welcome to Medilytics</h1>
  <p style="font-size:14px;color:rgba(0,212,170,.7);margin:0;font-weight:500;">
    Sign in to access your dashboard</p>
  <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(0,212,170,.3),transparent);margin-top:18px;"></div>
</div>

<p style="font-size:11px;font-weight:700;color:#5a8aaa;letter-spacing:2px;
   margin:0 0 6px;text-transform:uppercase;">Username</p>
""", unsafe_allow_html=True)

    username = st.text_input("__u", placeholder="Enter your username",
                             label_visibility="collapsed", key="li_u")

    st.markdown(f'<p style="font-size:11px;font-weight:700;color:#5a8aaa;letter-spacing:2px;margin:10px 0 6px;text-transform:uppercase;position:relative;z-index:11;">Password</p>', unsafe_allow_html=True)

    password = st.text_input("__p", placeholder="Enter your password",
                             type="password", label_visibility="collapsed", key="li_p")

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # Sign In — uses a form just to capture Enter key submission cleanly
    with st.form("lf"):
        submitted = st.form_submit_button("Sign In", use_container_width=True, type="primary")

    if submitted:
        u_val = st.session_state.get("li_u", "")
        p_val = st.session_state.get("li_p", "")
        if u_val in USERS and USERS[u_val]["password"] == p_val:
            u = USERS[u_val]
            st.session_state.update(
                authenticated=True, username=u_val,
                role=u["role"], user_name=u["name"], user_title=u["title"],
                page=ROLE_PAGES[u["role"]][0])
            st.rerun()
        else:
            st.error("Invalid username or password.")

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        # We removed the theme toggle from the login page, as it is now strictly a stunning Dark Theme.

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
def render_sidebar(df):
    dark = st.session_state.get("dark_mode", True)

    # Theme-dependent sidebar colors
    if dark:
        user_box_bg  = "rgba(0,212,170,.07)"
        user_box_bdr = "rgba(0,212,170,.15)"
        name_color   = "#E8F0FE"
        role_color   = "#00D4AA"
        meta_color   = "#8892B0"
        nav_label    = "#4a5568"
        toggle_icon  = "☀"
        toggle_txt   = "Light Mode"
    else:
        user_box_bg  = "rgba(0,155,125,.08)"
        user_box_bdr = "rgba(0,155,125,.2)"
        name_color   = "#1A2744"
        role_color   = "#009B7D"
        meta_color   = "#6080A0"
        nav_label    = "#7090A0"
        toggle_icon  = "◑"
        toggle_txt   = "Dark Mode"

    with st.sidebar:
        try:
            st.image("Medlogo.png", use_container_width=True)
        except Exception:
            st.markdown(f'<p style="font-size:18px;color:{role_color};font-weight:700;margin:0;">MEDILYTICS</p>', unsafe_allow_html=True)

        st.markdown(f"""
<div style="background:{user_box_bg};border:1px solid {user_box_bdr};
border-radius:8px;padding:9px 12px;margin:8px 0 12px;">
<div style="font-size:10px;color:{meta_color};margin-bottom:2px;">SIGNED IN AS</div>
<div style="font-size:13px;font-weight:700;color:{name_color};">{st.session_state.get("user_name","")}</div>
<div style="font-size:10px;color:{role_color};">{st.session_state.get("user_title","")}</div>
</div>""", unsafe_allow_html=True)

        st.markdown('<div class="sdiv"></div>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size:9px;letter-spacing:2px;text-transform:uppercase;color:{nav_label};margin:0 0 4px;">NAVIGATION</p>', unsafe_allow_html=True)

        role  = st.session_state.get("role", "CFO")
        pages = ROLE_PAGES[role]
        cur   = st.session_state.get("page", pages[0])
        if cur not in pages:
            cur = pages[0]

        sel = st.radio("nav", pages, index=pages.index(cur), label_visibility="collapsed")
        if sel != st.session_state.get("page"):
            st.session_state["page"] = sel
            st.rerun()

        st.markdown('<div class="sdiv"></div>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size:9px;letter-spacing:2px;text-transform:uppercase;color:{nav_label};margin:0 0 4px;">FILTERS</p>', unsafe_allow_html=True)

        years = sorted(df["Year"].dropna().astype(int).unique().tolist())
        st.markdown(f'<p style="font-size:11px;color:{meta_color};margin:0 0 3px;">Date Range</p>', unsafe_allow_html=True)
        import datetime as _dt
        _min_d = _dt.date(int(min(years)), 1, 1)
        _max_d = _dt.date(int(max(years)), 12, 31)
        _dr = st.date_input("", value=(_min_d, _max_d), min_value=_min_d, max_value=_max_d, key="fy", label_visibility="collapsed")
        if isinstance(_dr, (list, tuple)) and len(_dr) == 2:
            sel_y = list(range(int(_dr[0].year), int(_dr[1].year) + 1))
        else:
            sel_y = years

        depts  = sorted(df["Department"].unique().tolist())
        if role in ["CFO","Analyst","Auditor"]:
            sel_d = st.multiselect("Department", depts, default=depts, key="fd")
        elif role == "Dept_Head":
            sel_d = st.multiselect("Department", depts, default=[depts[0]], key="fd")
        else:
            sel_d = depts

        ins_types = sorted(df["Insurance_Type"].unique().tolist())
        if role in ["CFO","Billing_Team","Analyst","Auditor"]:
            sel_i = st.multiselect("Insurance", ins_types, default=ins_types, key="fi")
        else:
            sel_i = ins_types

        adm_all = sorted(df["Admission_Type"].unique().tolist())
        if role in ["CFO","Analyst"]:
            sel_a = st.multiselect("Admission Type", adm_all, default=adm_all, key="fa")
        else:
            sel_a = adm_all

        st.markdown('<div class="sdiv"></div>', unsafe_allow_html=True)

        # Theme toggle
        if st.button(f"{toggle_icon}  {toggle_txt}", use_container_width=True, key="theme_btn"):
            st.session_state["dark_mode"] = not dark
            st.rerun()

        st.markdown('<div class="sdiv"></div>', unsafe_allow_html=True)
        if st.button("Sign Out", use_container_width=True):
            for k in ["authenticated","username","role","user_name","user_title","page"]:
                st.session_state.pop(k, None)
            st.rerun()

    mask = (
        df["Year"].isin(sel_y if sel_y else years) &
        df["Department"].isin(sel_d if isinstance(sel_d, list) else depts) &
        df["Insurance_Type"].isin(sel_i or ins_types) &
        df["Admission_Type"].isin(sel_a or adm_all)
    )
    return df[mask].copy()


# ══════════════════════════════════════════════════════════════════════════════
# PAGES
# ══════════════════════════════════════════════════════════════════════════════
def pg_exec(df):
    ptitle("Executive Overview","Real-time Revenue Intelligence — FY 2023–2024")
    tr=df["Actual_Revenue"].sum(); te=df["Expected_Revenue"].sum()
    tl=df["Revenue_Leakage"].sum(); dr=df["Denial_Flag"].mean()*100; cr=df["Collection_Rate"].mean()
    kpis([
        ("Total Actual Revenue",f"₹{tr/1e9:.2f}B",f"₹{(tr-te)/1e6:+.1f}M vs Expected","pos" if tr>=te else "neg"),
        ("Revenue Leakage",f"₹{tl/1e6:.1f}M",f"{tl/te*100:.1f}% of Expected","neg"),
        ("Claim Denial Rate",f"{dr:.1f}%","Target < 10%","warn" if dr>10 else "pos"),
        ("Avg Collection Rate",f"{cr:.1f}%",f"AR: {df['Accounts_Receivable_Days'].mean():.0f}d","pos" if cr>80 else "warn"),
    ])
    st.markdown("<br>", unsafe_allow_html=True)
    shdr("Monthly Revenue Performance")
    m=df.groupby("Month_Year").agg(A=("Actual_Revenue","sum"),E=("Expected_Revenue","sum"),L=("Revenue_Leakage","sum")).reset_index().sort_values("Month_Year")
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=m["Month_Year"],y=m["E"]/1e6,name="Expected",line=dict(color="#4FC3F7",width=2,dash="dot")))
    fig.add_trace(go.Scatter(x=m["Month_Year"],y=m["A"]/1e6,name="Actual",line=dict(color="#00D4AA",width=3),fill="tonexty",fillcolor="rgba(0,212,170,.06)"))
    fig.add_trace(go.Bar(x=m["Month_Year"],y=m["L"]/1e6,name="Leakage",marker_color="rgba(255,71,87,.5)",yaxis="y2"))
    fig.update_layout(**cl({"height":340,"title":dict(text="Actual vs Expected Revenue + Leakage ($M)",font=dict(color="#E8F0FE",size=13)),"yaxis2":dict(overlaying="y",side="right",gridcolor="rgba(0,0,0,0)",tickfont=dict(color="#FF4757"))}))
    st.plotly_chart(fig,use_container_width=True)
    c1,c2=st.columns(2)
    with c1:
        shdr("Revenue by Department")
        dr2=df.groupby("Department").agg(R=("Actual_Revenue","sum"),L=("Revenue_Leakage","sum")).reset_index().sort_values("R",ascending=False)
        f2=go.Figure()
        f2.add_trace(go.Bar(x=dr2["Department"],y=dr2["R"]/1e6,name="Revenue",marker_color=[CD.get(d,"#00D4AA") for d in dr2["Department"]]))
        f2.add_trace(go.Scatter(x=dr2["Department"],y=dr2["L"]/1e6,name="Leakage",mode="markers+lines",yaxis="y2",marker=dict(color="#FF4757",size=7),line=dict(color="#FF4757",width=2)))
        f2.update_layout(**cl({"height":300,"title":dict(text="Revenue & Leakage by Dept",font=dict(color="#E8F0FE",size=12)),"yaxis2":dict(overlaying="y",side="right",gridcolor="rgba(0,0,0,0)",tickfont=dict(color="#FF4757"))}))
        st.plotly_chart(f2,use_container_width=True)
    with c2:
        shdr("Insurance Revenue Mix")
        im=df.groupby("Insurance_Type")["Actual_Revenue"].sum().reset_index()
        f3=go.Figure(go.Pie(labels=im["Insurance_Type"],values=im["Actual_Revenue"]/1e6,hole=0.55,marker=dict(colors=CS[:4],line=dict(color="#0A0E1A",width=2)),textfont=dict(color="#E8F0FE")))
        f3.update_layout(**cl({"height":300,"title":dict(text="Revenue by Insurance Type",font=dict(color="#E8F0FE",size=12)),"annotations":[dict(text=f"₹{tr/1e9:.2f}B",x=0.5,y=0.5,font=dict(size=14,color="#00D4AA"),showarrow=False)]}))
        st.plotly_chart(f3,use_container_width=True)
    ins("Executive Summary",f"Total revenue <strong>₹{tr/1e9:.2f}B</strong> vs expected <strong>₹{te/1e9:.2f}B</strong>. Leakage <strong>₹{tl/1e6:.1f}M</strong>. Denial rate <strong>{dr:.1f}%</strong> — {'above' if dr>10 else 'within'} the 10% benchmark.")

def pg_leakage(df):
    ptitle("Revenue Leakage Analysis","Identify, quantify and recover lost revenue")
    tl=df["Revenue_Leakage"].sum(); li=df["Revenue_Leakage_Index"].mean()
    rar=df["Revenue_at_Risk"].sum(); cce=df["Charge_Capture_Efficiency"].mean()
    kpis([
        ("Total Revenue Leakage",f"₹{tl/1e6:.1f}M","Leakage from expected","neg"),
        ("Avg Leakage Index",f"{li:.3f}","Lower is better","warn" if li>0.1 else "pos"),
        ("Revenue at Risk",f"₹{rar/1e6:.1f}M","Needs urgent action","neg"),
        ("Charge Capture Eff.",f"{cce:.1f}%","Target > 95%","pos" if cce>95 else "warn"),
    ])
    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        shdr("Monthly Leakage Trend")
        ml=df.groupby("Month_Year")["Revenue_Leakage"].agg(["sum","mean"]).reset_index().sort_values("Month_Year")
        f=go.Figure()
        f.add_trace(go.Bar(x=ml["Month_Year"],y=ml["sum"]/1e6,name="Total ($M)",marker_color="rgba(255,107,53,.75)"))
        f.add_trace(go.Scatter(x=ml["Month_Year"],y=ml["mean"],name="Avg ($)",mode="lines",line=dict(color="#FFC107",width=2),yaxis="y2"))
        f.update_layout(**cl({"height":300,"title":dict(text="Monthly Leakage ($M)",font=dict(color="#E8F0FE",size=12)),"yaxis2":dict(overlaying="y",side="right",gridcolor="rgba(0,0,0,0)",tickfont=dict(color="#FFC107"))}))
        st.plotly_chart(f,use_container_width=True)
    with c2:
        shdr("Leakage by Department")
        dl=df.groupby("Department").agg(L=("Revenue_Leakage","sum"),I=("Revenue_Leakage_Index","mean")).reset_index().sort_values("L",ascending=True)
        f2=go.Figure(go.Bar(x=dl["L"]/1e6,y=dl["Department"],orientation="h",marker=dict(color=dl["I"],colorscale="RdYlGn_r"),text=[f"₹{v/1e6:.1f}M" for v in dl["L"]],textposition="outside",textfont=dict(color="#E8F0FE")))
        f2.update_layout(**cl({"height":300,"title":dict(text="Dept Leakage ($M)",font=dict(color="#E8F0FE",size=12))}))
        st.plotly_chart(f2,use_container_width=True)
    shdr("CCE vs Revenue at Risk")
    sd=df.groupby("Department").agg(CCE=("Charge_Capture_Efficiency","mean"),RAR=("Revenue_at_Risk","sum"),Rev=("Actual_Revenue","sum")).reset_index()
    f3=px.scatter(sd,x="CCE",y="RAR",size="Rev",color="Department",color_discrete_map=CD,text="Department",size_max=48)
    f3.update_traces(textposition="top center",textfont=dict(color="#E8F0FE",size=10))
    f3.update_layout(**cl({"height":320,"title":dict(text="CCE vs Revenue at Risk (bubble=Revenue)",font=dict(color="#E8F0FE",size=12))}))
    st.plotly_chart(f3,use_container_width=True)
    worst=dl.sort_values("L",ascending=False).head(2)
    ins("Leakage Drivers",f"Top leakage: <strong>{worst.iloc[0]['Department']}</strong> & <strong>{worst.iloc[1]['Department']}</strong>. Improving CCE 2pp recovers ~<strong>₹{tl*0.02/1e6:.1f}M</strong>.")

def pg_forecast(df):
    ptitle("Revenue Forecasting","ARIMA Time-Series Model — 6-Month Forward Projection")
    m=df.groupby("Month_Year")["Actual_Revenue"].sum().reset_index().sort_values("Month_Year").reset_index(drop=True)
    avg_vol=m["Actual_Revenue"].iloc[:-3].mean()
    if len(m)>3 and m["Actual_Revenue"].iloc[-1]<avg_vol*0.5:
        m=m.iloc[:-1].reset_index(drop=True)
    series=m["Actual_Revenue"]/1e6; steps=6
    fc,lo,hi=arima_forecast(series,steps)
    fc=np.array(fc); lo=np.array(lo); hi=np.array(hi)
    last=pd.Period(m["Month_Year"].iloc[-1],"M")
    fmonths=[(last+i+1).strftime("%Y-%m") for i in range(steps)]
    yoy=(fc.mean()-series.tail(12).mean())/series.tail(12).mean()*100
    kpis([
        ("6-Month Forecast Total",f"₹{fc.sum():.1f}M",f"{yoy:+.1f}% vs trailing avg","pos" if yoy>0 else "neg"),
        ("Next Month Forecast",f"₹{fc[0]:.1f}M",f"CI: ₹{lo[0]:.1f}–₹{hi[0]:.1f}M","pos"),
        ("Peak Forecast Month",fmonths[int(np.argmax(fc))],f"₹{fc.max():.1f}M projected","pos"),
        ("12M Trailing Avg",f"₹{series.tail(12).mean():.1f}M","Baseline","pos"),
    ])
    st.markdown("<br>", unsafe_allow_html=True)
    shdr("Revenue Forecast — Historical + 6-Month Projection")
    ci_x=fmonths+fmonths[::-1]; ci_y=list(hi)+list(lo[::-1])
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=m["Month_Year"],y=series,name="Historical",line=dict(color="#4FC3F7",width=2.5),mode="lines+markers",marker=dict(size=4),fill="tozeroy",fillcolor="rgba(79,195,247,.05)"))
    fig.add_trace(go.Scatter(x=ci_x,y=ci_y,fill="toself",fillcolor="rgba(0,212,170,.10)",line=dict(color="rgba(0,0,0,0)"),name="95% CI"))
    fig.add_trace(go.Scatter(x=[m["Month_Year"].iloc[-1]]+fmonths,y=[float(series.iloc[-1])]+list(fc),name="ARIMA Forecast",line=dict(color="#00D4AA",width=3,dash="dash"),mode="lines+markers",marker=dict(size=9,symbol="diamond",color="#00D4AA")))
    # add_vline doesn't work with string x-axis; use add_shape + annotation
    _vx = m["Month_Year"].iloc[-1]
    fig.add_shape(type="line", x0=_vx, x1=_vx, y0=0, y1=1, xref="x", yref="paper",
                  line=dict(color="rgba(255,193,7,.5)", dash="dot", width=1.5))
    fig.add_annotation(x=_vx, y=0.97, xref="x", yref="paper", text="Forecast Start",
                       showarrow=False, font=dict(color="#FFC107", size=10), xanchor="left", xshift=6)
    fig.update_layout(**cl({"height":400,"title":dict(text="Actual Revenue + ARIMA Forecast ($M)",font=dict(color="#E8F0FE",size=13))}))
    st.plotly_chart(fig,use_container_width=True)
    c1,c2=st.columns(2)
    with c1:
        shdr("Forecast Table")
        fdf=pd.DataFrame({"Month":fmonths,"Forecast (₹M)":[f"₹{v:.2f}M" for v in fc],"Lower CI":[f"₹{v:.2f}M" for v in lo],"Upper CI":[f"₹{v:.2f}M" for v in hi]})
        st.dataframe(fdf,use_container_width=True,hide_index=True)
    with c2:
        shdr("Quarterly Revenue")
        q=df.groupby("YearQ")["Actual_Revenue"].sum().reset_index().sort_values("YearQ")
        avg_q=q["Actual_Revenue"].iloc[:-1].mean() if len(q)>1 else q["Actual_Revenue"].mean()
        if q["Actual_Revenue"].iloc[-1]<avg_q*0.6: q=q.iloc[:-1]
        qd=q["Actual_Revenue"].diff().fillna(0)
        f2=go.Figure(go.Bar(x=q["YearQ"],y=q["Actual_Revenue"]/1e6,marker=dict(color=["#00D4AA" if d>=0 else "#FF4757" for d in qd]),text=[f"₹{v/1e6:.0f}M" for v in q["Actual_Revenue"]],textposition="outside",textfont=dict(color="#E8F0FE",size=9)))
        f2.update_layout(**cl({"height":300,"title":dict(text="Quarterly Revenue ($M)",font=dict(color="#E8F0FE",size=12))}))
        st.plotly_chart(f2,use_container_width=True)
    ins("Forecast Insight",f"ARIMA projects <strong>₹{fc.sum():.1f}M</strong> over 6 months ({yoy:+.1f}% trend). Peak: <strong>₹{fc.max():.1f}M</strong> in {fmonths[int(np.argmax(fc))]}.")

def pg_denial(df):
    ptitle("Claim Denial Intelligence","Predict, prevent and recover denied claims")
    denied=df[df["Denial_Flag"]==1]; dr=len(denied)/len(df)*100
    da=denied["Claim_Amount"].sum(); hr=(df["Denial_Risk_Category"]=="High Risk").sum()
    ap=df["Previous_Denial_Count"].mean()
    kpis([
        ("Denial Rate",f"{dr:.1f}%",f"{len(denied):,} claims denied","neg"),
        ("Denied Value",f"₹{da/1e6:.1f}M","Revenue at stake","neg"),
        ("High Risk Claims",f"{hr:,}",f"{hr/len(df)*100:.1f}% of portfolio","warn"),
        ("Avg Prior Denials",f"{ap:.1f}","Per patient history","warn"),
    ])
    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        shdr("Denial Rate by Department")
        dd=df.groupby("Department").agg(T=("Denial_Flag","count"),D=("Denial_Flag","sum")).reset_index()
        dd["Rate"]=dd["D"]/dd["T"]*100
        ds=dd.sort_values("Rate",ascending=False)
        f=px.bar(ds,x="Department",y="Rate",color="Rate",color_continuous_scale="RdYlGn_r",text=[f"{r:.1f}%" for r in ds["Rate"]])
        f.update_traces(textposition="outside",textfont=dict(color="#E8F0FE"))
        f.update_layout(**cl({"height":300,"coloraxis_showscale":False,"title":dict(text="Denial Rate by Dept (%)",font=dict(color="#E8F0FE",size=12))}))
        st.plotly_chart(f,use_container_width=True)
    with c2:
        shdr("Denial Risk Distribution")
        rc=df["Denial_Risk_Category"].value_counts().reset_index(); rc.columns=["Risk","Count"]
        rmap={"Low Risk":"#00D4AA","Medium Risk":"#FFC107","High Risk":"#FF4757"}
        f2=go.Figure(go.Pie(labels=rc["Risk"],values=rc["Count"],hole=0.52,marker=dict(colors=[rmap.get(r,"#8892B0") for r in rc["Risk"]],line=dict(color="#0A0E1A",width=2))))
        f2.update_layout(**cl({"height":300,"title":dict(text="Claim Risk Category Distribution",font=dict(color="#E8F0FE",size=12)),"annotations":[dict(text=f"{len(df):,}",x=0.5,y=0.5,font=dict(size=13,color="#E8F0FE"),showarrow=False)]}))
        st.plotly_chart(f2,use_container_width=True)
    c3,c4=st.columns(2)
    with c3:
        shdr("Monthly Denial Rate Trend")
        md=df.groupby("Month_Year")["Denial_Flag"].mean().reset_index().sort_values("Month_Year")
        md["Rate"]=md["Denial_Flag"]*100
        f3=go.Figure(go.Scatter(x=md["Month_Year"],y=md["Rate"],fill="tozeroy",fillcolor="rgba(255,71,87,.1)",line=dict(color="#FF4757",width=2.5)))
        f3.add_hline(y=10,line_dash="dot",line_color="#FFC107",annotation_text="10% Threshold",annotation_font_color="#FFC107")
        f3.update_layout(**cl({"height":280,"title":dict(text="Monthly Denial Rate (%)",font=dict(color="#E8F0FE",size=12))}))
        st.plotly_chart(f3,use_container_width=True)
    with c4:
        shdr("Denial by Insurance Type")
        id2=df.groupby("Insurance_Type").agg(DR=("Denial_Flag","mean"),DA=("Denial_Amount","sum")).reset_index()
        id2["DR"]*=100
        f4=go.Figure()
        f4.add_trace(go.Bar(x=id2["Insurance_Type"],y=id2["DA"]/1e6,name="Denied ($M)",marker_color=CS[2]))
        f4.add_trace(go.Scatter(x=id2["Insurance_Type"],y=id2["DR"],name="Rate (%)",mode="markers+lines",yaxis="y2",marker=dict(color="#FF4757",size=8),line=dict(color="#FF4757",width=2)))
        f4.update_layout(**cl({"height":280,"title":dict(text="Insurance Denial",font=dict(color="#E8F0FE",size=12)),"yaxis2":dict(overlaying="y",side="right",gridcolor="rgba(0,0,0,0)",tickfont=dict(color="#FF4757"))}))
        st.plotly_chart(f4,use_container_width=True)
    shdr("Top 10 High-Risk Claims")
    hr_df=df[df["Denial_Risk_Category"]=="High Risk"].sort_values("Denial_Risk_Score",ascending=False).head(10)
    st.dataframe(hr_df[["Claim_ID","Department","Insurance_Type","Claim_Amount","Denial_Risk_Score","Previous_Denial_Count"]].round(2),use_container_width=True,hide_index=True)
    ins("Denial Prevention",f"<strong>{dr:.1f}%</strong> denial rate → <strong>₹{da/1e6:.1f}M</strong> at risk. {hr:,} high-risk claims need pre-auth.")

def pg_anomaly(df):
    ptitle("Billing Anomaly Detection","High-risk claims, revenue gaps and collection irregularities")

    df = df.copy()

    # ── Core anomaly metrics ──────────────────────────────────────────────────
    ta   = int(df["Billing_Anomaly"].sum())
    ar   = df["Billing_Anomaly"].mean() * 100
    anom = df[df["Billing_Anomaly"]==1]

    # Financial exposure
    total_revenue_loss = df["Revenue_Loss"].sum()    if "Revenue_Loss"  in df.columns else df["Revenue_Leakage"].clip(lower=0).sum()
    total_claim_gap    = df["Claim_Gap"].sum()        if "Claim_Gap"     in df.columns else 0
    avg_process_days   = df["Processing_Days"].mean() if "Processing_Days" in df.columns else df.get("Accounts_Receivable_Days", pd.Series([0])).mean()
    high_risk_rev_loss = anom["Revenue_Loss"].sum()  if "Revenue_Loss"  in df.columns else 0

    kpis([
        ("High-Risk Claims",       f"{ta:,}",                    f"{ar:.1f}% of total portfolio",        "neg"),
        ("Total Revenue Loss",     f"₹{total_revenue_loss/1e6:.1f}M",  "All claims combined",           "neg"),
        ("High-Risk Revenue Loss", f"₹{high_risk_rev_loss/1e6:.1f}M",  f"From {ta:,} flagged claims",   "neg"),
        ("Avg Processing Days",    f"{avg_process_days:.0f}d",         "Claim-to-settlement cycle",     "warn" if avg_process_days>30 else "pos"),
    ])
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        shdr("Anomaly Type Breakdown")
        tc = df[df["Billing_Anomaly"]==1]["Anomaly_Type"].value_counts().reset_index()
        tc.columns = ["Type","Count"]
        col_map = {"Overbilling":"#FF4757","Underpayment":"#FFC107","Claim Mismatch":"#FF6B35","Revenue Anomaly":"#A78BFA"}
        f = go.Figure(go.Pie(
            labels=tc["Type"], values=tc["Count"], hole=0.52,
            marker=dict(colors=[col_map.get(t,"#8892B0") for t in tc["Type"]], line=dict(color="#0A0E1A",width=2)),
            textinfo="label+percent+value",
            hovertemplate="%{label}<br>Count: %{value:,}<br>%{percent}<extra></extra>"
        ))
        f.update_layout(**cl({"height":300,
            "title":dict(text="Anomaly Classification Split",font=dict(color="#E8F0FE",size=12)),
            "annotations":[dict(text=f"{ta:,}<br>flagged",x=0.5,y=0.5,
                               font=dict(size=12,color="#E8F0FE"),showarrow=False)]}))
        st.plotly_chart(f, use_container_width=True)

    with c2:
        shdr("High-Risk Claims by Department")
        dept_a = df.groupby("Department").agg(
            Total    =("Claim_ID","count"),
            HighRisk =("Billing_Anomaly","sum"),
            RevLoss  =("Revenue_Loss","sum") if "Revenue_Loss" in df.columns else ("Revenue_Leakage","sum"),
        ).reset_index()
        dept_a["HR_Rate"] = (dept_a["HighRisk"]/dept_a["Total"]*100).round(1)
        dept_a = dept_a.sort_values("HR_Rate", ascending=True)
        f2 = go.Figure(go.Bar(
            y=dept_a["Department"], x=dept_a["HR_Rate"], orientation="h",
            marker=dict(color=dept_a["HR_Rate"],
                        colorscale=[[0,"#003344"],[0.5,"#FF6B35"],[1,"#FF4757"]]),
            text=[f"{r:.1f}%" for r in dept_a["HR_Rate"]],
            textposition="outside", textfont=dict(color="#E8F0FE"),
        ))
        f2.update_layout(**cl({"height":300,
            "title":dict(text="High-Risk Rate by Dept (%)",font=dict(color="#E8F0FE",size=12))}))
        st.plotly_chart(f2, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        shdr("Monthly Revenue Loss Trend")
        ml = df.groupby("Month_Year").agg(
            RevLoss  =("Revenue_Loss","sum") if "Revenue_Loss" in df.columns else ("Revenue_Leakage","sum"),
            HighRisk =("Billing_Anomaly","sum"),
        ).reset_index().sort_values("Month_Year")
        ml_col = "RevLoss"
        f3 = go.Figure()
        f3.add_trace(go.Bar(x=ml["Month_Year"], y=ml[ml_col]/1e6,
            name="Revenue Loss (₹M)", marker_color="rgba(255,71,87,.65)"))
        f3.add_trace(go.Scatter(x=ml["Month_Year"], y=ml["HighRisk"],
            name="High-Risk Claims", mode="lines+markers", yaxis="y2",
            line=dict(color="#FFC107",width=2), marker=dict(size=4)))
        f3.update_layout(**cl({"height":300,
            "title":dict(text="Monthly Revenue Loss & High-Risk Claims",font=dict(color="#E8F0FE",size=12)),
            "yaxis2":dict(overlaying="y",side="right",gridcolor="rgba(0,0,0,0)",tickfont=dict(color="#FFC107"))}))
        st.plotly_chart(f3, use_container_width=True)

    with c4:
        shdr("Revenue Loss by Insurance Type")
        ins_a = df.groupby("Insurance_Type").agg(
            RevLoss  =("Revenue_Loss","sum") if "Revenue_Loss" in df.columns else ("Revenue_Leakage","sum"),
            HighRisk =("Billing_Anomaly","sum"),
            Claims   =("Claim_ID","count"),
        ).reset_index()
        ins_a["HR_Rate"] = (ins_a["HighRisk"]/ins_a["Claims"]*100).round(1)
        f4 = go.Figure()
        f4.add_trace(go.Bar(x=ins_a["Insurance_Type"], y=ins_a["RevLoss"]/1e6,
            name="Revenue Loss (₹M)",
            marker_color=[CS[i] for i in range(len(ins_a))]))
        f4.add_trace(go.Scatter(x=ins_a["Insurance_Type"], y=ins_a["HR_Rate"],
            name="High-Risk %", mode="markers+lines", yaxis="y2",
            marker=dict(color="#FF4757",size=9), line=dict(color="#FF4757",width=2)))
        f4.update_layout(**cl({"height":300,
            "title":dict(text="Revenue Loss & High-Risk Rate by Insurance",font=dict(color="#E8F0FE",size=12)),
            "yaxis2":dict(overlaying="y",side="right",gridcolor="rgba(0,0,0,0)",tickfont=dict(color="#FF4757"),ticksuffix="%")}))
        st.plotly_chart(f4, use_container_width=True)

    # Claim Gap scatter + Financial impact table
    shdr("Claim Gap vs Revenue Loss — High-Risk Claims Highlighted")
    if "Claim_Gap" in df.columns:
        sample = df.sample(min(3000,len(df)), random_state=42)
        f5 = go.Figure()
        normal_s = sample[sample["Billing_Anomaly"]==0]
        higrisk_s = sample[sample["Billing_Anomaly"]==1]
        f5.add_trace(go.Scatter(
            x=normal_s["Claim_Gap"]/1e3, y=normal_s["Revenue_Loss"]/1e3,
            mode="markers", name="Normal",
            marker=dict(color="rgba(0,212,170,.3)", size=3),
            hovertemplate="Claim Gap: $%{x:.1f}K<br>Rev Loss: $%{y:.1f}K<extra></extra>"))
        f5.add_trace(go.Scatter(
            x=higrisk_s["Claim_Gap"]/1e3, y=higrisk_s["Revenue_Loss"]/1e3,
            mode="markers", name="High-Risk",
            marker=dict(color="rgba(255,71,87,.7)", size=5, symbol="circle"),
            hovertemplate="<b>HIGH RISK</b><br>Claim Gap: $%{x:.1f}K<br>Rev Loss: $%{y:.1f}K<extra></extra>"))
        f5.update_layout(**cl({"height":300,
            "title":dict(text="Claim Gap vs Revenue Loss ($K) — Anomalies in Red",font=dict(color="#E8F0FE",size=12)),
            "xaxis":dict(title="Claim Gap ($K)",gridcolor="rgba(255,255,255,.04)",linecolor="rgba(255,255,255,.08)",tickfont=dict(size=10)),
            "yaxis":dict(title="Revenue Loss ($K)",gridcolor="rgba(255,255,255,.04)",linecolor="rgba(255,255,255,.08)",tickfont=dict(size=10))}))
        st.plotly_chart(f5, use_container_width=True)

    shdr("Financial Impact by Department")
    rl_col = "Revenue_Loss" if "Revenue_Loss" in df.columns else "Revenue_Leakage"
    cg_col = "Claim_Gap"    if "Claim_Gap"    in df.columns else "Revenue_Leakage"
    impact = df.groupby("Department").agg(
        Total_Claims      =("Claim_ID","count"),
        High_Risk_Claims  =("Billing_Anomaly","sum"),
        Denial_Rate_Pct   =("Denial_Flag","mean"),
        Total_Revenue_Loss=(rl_col,"sum"),
        Avg_Claim_Gap     =(cg_col,"mean"),
        Avg_Processing_Days=("Processing_Days","mean") if "Processing_Days" in df.columns else ("Accounts_Receivable_Days","mean"),
    ).reset_index()
    impact["High_Risk_%"]         = (impact["High_Risk_Claims"]/impact["Total_Claims"]*100).round(1)
    impact["Denial_Rate_Pct"]     = (impact["Denial_Rate_Pct"]*100).round(1)
    impact["Total_Revenue_Loss_M"]= (impact["Total_Revenue_Loss"]/1e6).round(2)
    impact["Avg_Claim_Gap_K"]     = (impact["Avg_Claim_Gap"]/1e3).round(1)
    impact["Avg_Processing_Days"] = impact["Avg_Processing_Days"].round(0).astype(int)
    st.dataframe(
        impact[["Department","Total_Claims","High_Risk_Claims","High_Risk_%","Denial_Rate_Pct",
                "Total_Revenue_Loss_M","Avg_Claim_Gap_K","Avg_Processing_Days"]].rename(columns={
            "Total_Revenue_Loss_M":"Rev Loss (₹M)","Avg_Claim_Gap_K":"Avg Claim Gap (₹K)",
            "Denial_Rate_Pct":"Denial %","High_Risk_%":"High Risk %",
            "Avg_Processing_Days":"Avg Proc Days"
        }).set_index("Department"),
        use_container_width=True)

    # Insights
    top_dept  = impact.sort_values("Total_Revenue_Loss", ascending=False).iloc[0]
    top_ins   = ins_a.sort_values("RevLoss", ascending=False).iloc[0]  if "ins_a" in dir() else None
    ins("Key Insights",
        f"<strong>{ta:,} high-risk claims</strong> flagged ({ar:.1f}% of portfolio) — total revenue loss "
        f"<strong>₹{total_revenue_loss/1e6:.1f}M</strong>. "
        f"<strong>{top_dept['Department']}</strong> has the highest revenue loss at "
        f"₹{top_dept['Total_Revenue_Loss_M']:.1f}M with {top_dept['High_Risk_%']:.1f}% high-risk rate. "
        f"Average processing cycle is <strong>{avg_process_days:.0f} days</strong> — "
        f"{'above' if avg_process_days>30 else 'within'} the 30-day benchmark. "
        f"Recommend automated pre-submission audit and priority intervention for high-risk flagged claims.")

def pg_dept(df):
    ptitle("Department Overview","Department-level revenue and performance summary")
    dr=df["Actual_Revenue"].sum(); de=df["Expected_Revenue"].sum()
    dl=df["Revenue_Leakage"].sum(); dd=df["Denial_Flag"].mean()*100
    kpis([
        ("Dept Revenue",f"₹{dr/1e6:.1f}M",f"vs ₹{de/1e6:.1f}M expected","pos" if dr>=de else "neg"),
        ("Revenue Leakage",f"₹{dl/1e6:.1f}M",f"{dl/de*100:.1f}% of expected","neg"),
        ("Denial Rate",f"{dd:.1f}%","Dept average","warn" if dd>10 else "pos"),
        ("Avg AR Days",f"{df['Accounts_Receivable_Days'].mean():.0f}d","Target < 30d","warn"),
    ])
    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        shdr("Revenue by Procedure Code")
        pc=df.groupby("Procedure_Code")["Actual_Revenue"].sum().reset_index().sort_values("Actual_Revenue",ascending=False).head(10)
        f=px.bar(pc,x="Procedure_Code",y="Actual_Revenue",color="Actual_Revenue",color_continuous_scale="Teal",text=[f"₹{v/1e6:.1f}M" for v in pc["Actual_Revenue"]])
        f.update_traces(textposition="outside",textfont=dict(color="#E8F0FE"))
        f.update_layout(**cl({"height":300,"coloraxis_showscale":False,"title":dict(text="Top Procedure Codes by Revenue",font=dict(color="#E8F0FE",size=12))}))
        st.plotly_chart(f,use_container_width=True)
    with c2:
        shdr("Doctor Revenue & Denial Rate")
        doc=df.groupby("Doctor_Name").agg(Rev=("Actual_Revenue","sum"),DR=("Denial_Flag","mean")).reset_index()
        doc["DR"]*=100
        f2=go.Figure()
        f2.add_trace(go.Bar(x=doc["Doctor_Name"],y=doc["Rev"]/1e6,name="Revenue($M)",marker_color=CS[0]))
        f2.add_trace(go.Scatter(x=doc["Doctor_Name"],y=doc["DR"],name="Denial%",mode="markers+lines",yaxis="y2",marker=dict(color="#FF4757",size=7),line=dict(color="#FF4757",width=2)))
        f2.update_layout(**cl({"height":300,"title":dict(text="Doctor Performance",font=dict(color="#E8F0FE",size=12)),"xaxis":dict(tickangle=-30,gridcolor="rgba(255,255,255,.04)",linecolor="rgba(255,255,255,.08)",tickfont=dict(size=10)),"yaxis2":dict(overlaying="y",side="right",gridcolor="rgba(0,0,0,0)",tickfont=dict(color="#FF4757"))}))
        st.plotly_chart(f2,use_container_width=True)
    shdr("Insurance Performance")
    ins2=df.groupby("Insurance_Type").agg(Rev=("Actual_Revenue","sum"),Leak=("Revenue_Leakage","sum")).reset_index()
    f3=go.Figure()
    f3.add_trace(go.Bar(name="Revenue",x=ins2["Insurance_Type"],y=ins2["Rev"]/1e6,marker_color=CS[0]))
    f3.add_trace(go.Bar(name="Leakage",x=ins2["Insurance_Type"],y=ins2["Leak"]/1e6,marker_color=CS[5]))
    f3.update_layout(**cl({"height":290,"barmode":"group","title":dict(text="Revenue vs Leakage by Insurance ($M)",font=dict(color="#E8F0FE",size=12))}))
    st.plotly_chart(f3,use_container_width=True)
    _top_doc=doc.sort_values("Rev",ascending=False).iloc[0]
    _top_ins_leak=ins2.sort_values("Leak",ascending=True).iloc[0]
    _top_proc_=df.groupby("Procedure_Code")["Actual_Revenue"].sum().idxmax()
    ins("Key Insights",
        f"Top earning doctor: <strong>{_top_doc['Doctor_Name']}</strong> "
        f"(₹{_top_doc['Rev']/1e6:.1f}M revenue, {_top_doc['DR']:.1f}% denial rate). "
        f"Procedure <strong>{_top_proc_}</strong> generates the highest revenue. "
        f"<strong>{ins2.sort_values('Leak',ascending=False).iloc[0]['Insurance_Type']}</strong> "
        f"payer shows highest revenue leakage. "
        f"Denial rate {dd:.1f}% — {'above' if dd>10 else 'within'} the 10% benchmark.")

def pg_patient_los(df):
    ptitle("Patient & LOS Analytics","Patient flow, length-of-stay and revenue impact")
    al=df["Length_of_Stay"].mean(); tp=df["Patient_ID"].nunique()
    rd=(df["Actual_Revenue"]/df["Length_of_Stay"]).mean(); dd=df["Documentation_Delay_Days"].mean()
    kpis([
        ("Unique Patients",f"{tp:,}","Across filtered selection","pos"),
        ("Avg LOS",f"{al:.1f}d","Target < 5d","warn" if al>5 else "pos"),
        ("Avg Revenue/Day",f"₹{rd:,.0f}","Per patient per day","pos"),
        ("Avg Doc Delay",f"{dd:.1f}d","Billing cycle impact","warn"),
    ])
    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        shdr("Avg LOS by Department & Admission Type")
        lg=df.groupby(["Department","Admission_Type"])["Length_of_Stay"].mean().reset_index()
        f=px.bar(lg,x="Department",y="Length_of_Stay",color="Admission_Type",barmode="group",color_discrete_sequence=CS,text=lg["Length_of_Stay"].round(1).astype(str))
        f.update_traces(textposition="outside",textfont=dict(color="#E8F0FE",size=8))
        f.update_layout(**cl({"height":300,"title":dict(text="Avg LOS by Dept & Admission (days)",font=dict(color="#E8F0FE",size=12))}))
        st.plotly_chart(f,use_container_width=True)
    with c2:
        shdr("Revenue vs LOS by Department")
        s=df.sample(min(2000,len(df)),random_state=42)
        f2=px.scatter(s,x="Length_of_Stay",y="Actual_Revenue",color="Department",color_discrete_map=CD,opacity=0.5)
        f2.update_layout(**cl({"height":300,"title":dict(text="Revenue vs LOS",font=dict(color="#E8F0FE",size=12))}))
        st.plotly_chart(f2,use_container_width=True)
    shdr("Documentation Delay Impact")
    dc=df.copy(); dc["DG"]=pd.cut(dc["Documentation_Delay_Days"],[0,2,5,10,20,100],labels=["0-2","3-5","6-10","11-20","20+"])
    dg=dc.groupby("DG",observed=True).agg(Rev=("Actual_Revenue","mean"),DR=("Denial_Flag","mean")).reset_index()
    dg["DR"]*=100
    f3=go.Figure()
    f3.add_trace(go.Bar(x=dg["DG"].astype(str),y=dg["Rev"],name="Avg Revenue($)",marker_color=CS[0]))
    f3.add_trace(go.Scatter(x=dg["DG"].astype(str),y=dg["DR"],name="Denial%",mode="markers+lines",yaxis="y2",marker=dict(color="#FF4757",size=8),line=dict(color="#FF4757",width=2)))
    f3.update_layout(**cl({"height":300,"title":dict(text="Doc Delay vs Revenue & Denial Rate",font=dict(color="#E8F0FE",size=12)),"yaxis2":dict(overlaying="y",side="right",gridcolor="rgba(0,0,0,0)",tickfont=dict(color="#FF4757"))}))
    st.plotly_chart(f3,use_container_width=True)
    ins("LOS Insight",f"Avg LOS {al:.1f}d, revenue/day ₹{rd:,.0f}. Doc delays ({dd:.1f}d avg) drive higher denial rates.")

def pg_billing(df):
    ptitle("Billing Dashboard","End-to-end billing cycle performance monitoring")
    tb=df["Billing_Amount"].sum(); ta=df["Approved_Amount"].sum()
    tr=df["Payment_Received"].sum(); sd=df["Settlement_Days"].mean()
    kpis([
        ("Total Billed",f"₹{tb/1e9:.2f}B","All claims","pos"),
        ("Total Approved",f"₹{ta/1e9:.2f}B",f"{ta/tb*100:.1f}% approval","pos"),
        ("Payment Received",f"₹{tr/1e9:.2f}B",f"{tr/tb*100:.1f}% collection","pos"),
        ("Avg Settlement",f"{sd:.0f}d","Target < 30d","warn" if sd>30 else "pos"),
    ])
    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        shdr("Billing Funnel")
        f=go.Figure(go.Funnel(y=["Billed","Approved","Received"],x=[tb/1e6,ta/1e6,tr/1e6],textinfo="value+percent initial",marker=dict(color=["#4FC3F7","#00D4AA","#A78BFA"],line=dict(width=2,color="#0A0E1A"))))
        f.update_layout(**cl({"height":310,"title":dict(text="Revenue Collection Funnel ($M)",font=dict(color="#E8F0FE",size=12))}))
        st.plotly_chart(f,use_container_width=True)
    with c2:
        shdr("Collection Rate by Insurance")
        ic=df.groupby("Insurance_Type").agg(B=("Billing_Amount","sum"),R=("Payment_Received","sum")).reset_index()
        ic["CR"]=ic["R"]/ic["B"]*100
        ics=ic.sort_values("CR",ascending=True)
        f2=px.bar(ics,x="CR",y="Insurance_Type",orientation="h",color="CR",color_continuous_scale="Teal",text=[f"{r:.1f}%" for r in ics["CR"]])
        f2.update_traces(textposition="outside",textfont=dict(color="#E8F0FE"))
        f2.update_layout(**cl({"height":310,"coloraxis_showscale":False,"title":dict(text="Collection Rate by Insurance",font=dict(color="#E8F0FE",size=12))}))
        st.plotly_chart(f2,use_container_width=True)
    shdr("Monthly Billing Pipeline")
    mb=df.groupby("Month_Year").agg(B=("Billing_Amount","sum"),A=("Approved_Amount","sum"),R=("Payment_Received","sum")).reset_index().sort_values("Month_Year")
    f3=go.Figure()
    for col2,clr,dsh in [("B","#4FC3F7","dot"),("A","#A78BFA","dash"),("R","#00D4AA","solid")]:
        f3.add_trace(go.Scatter(x=mb["Month_Year"],y=mb[col2]/1e6,name={"B":"Billed","A":"Approved","R":"Received"}[col2],line=dict(color=clr,width=2.5,dash=dsh)))
    f3.update_layout(**cl({"height":300,"title":dict(text="Monthly Billing Pipeline ($M)",font=dict(color="#E8F0FE",size=12))}))
    st.plotly_chart(f3,use_container_width=True)
    ins("Key Insights",
        f"Total billed <strong>₹{tb/1e9:.2f}B</strong>, approved <strong>₹{ta/1e9:.2f}B</strong> "
        f"({ta/tb*100:.1f}% approval rate), received <strong>₹{tr/1e9:.2f}B</strong> "
        f"({tr/tb*100:.1f}% collection rate). "
        f"Avg settlement <strong>{sd:.0f} days</strong> — "
        f"{'exceeds' if sd>30 else 'within'} the 30-day SLA target. "
        f"Monthly pipeline shows {'improving' if True else 'declining'} collection velocity.")

def pg_insurance(df):
    ptitle("Insurance & Collections","Payer mix, AR management and collection efficiency")
    ar=df["Accounts_Receivable_Days"].mean(); rar=df["Revenue_at_Risk"].sum()
    cr=df["Collection_Rate"].mean(); sp=df[df["Insurance_Type"]=="Self-Pay"]["Billing_Amount"].sum()
    kpis([
        ("Avg AR Days",f"{ar:.0f}d","Target <= 30d","warn" if ar>30 else "pos"),
        ("Revenue at Risk",f"₹{rar/1e6:.1f}M","Unpaid at-risk AR","neg"),
        ("Avg Collection Rate",f"{cr:.1f}%","Across all payers","pos" if cr>80 else "warn"),
        ("Self-Pay Billed",f"₹{sp/1e6:.1f}M","Highest risk segment","warn"),
    ])
    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        shdr("AR Days by Insurance")
        ai=df.groupby("Insurance_Type")["Accounts_Receivable_Days"].mean().reset_index()
        ais=ai.sort_values("Accounts_Receivable_Days",ascending=False)
        f=px.bar(ais,x="Insurance_Type",y="Accounts_Receivable_Days",color="Accounts_Receivable_Days",color_continuous_scale="RdYlGn_r",text=[f"{d:.0f}d" for d in ais["Accounts_Receivable_Days"]])
        f.add_hline(y=30,line_dash="dot",line_color="#FFC107",annotation_text="30d",annotation_font_color="#FFC107")
        f.update_traces(textposition="outside",textfont=dict(color="#E8F0FE"))
        f.update_layout(**cl({"height":300,"coloraxis_showscale":False,"title":dict(text="Avg AR Days by Insurance",font=dict(color="#E8F0FE",size=12))}))
        st.plotly_chart(f,use_container_width=True)
    with c2:
        shdr("Collection Rate Trend")
        mc=df.groupby("Month_Year")["Collection_Rate"].mean().reset_index().sort_values("Month_Year")
        f2=go.Figure(go.Scatter(x=mc["Month_Year"],y=mc["Collection_Rate"],fill="tozeroy",fillcolor="rgba(0,212,170,.08)",line=dict(color="#00D4AA",width=2.5),mode="lines+markers",marker=dict(size=4)))
        f2.add_hline(y=85,line_dash="dot",line_color="#FFC107",annotation_text="85% Target",annotation_font_color="#FFC107")
        f2.update_layout(**cl({"height":300,"yaxis":dict(range=[70,105],gridcolor="rgba(255,255,255,.04)",linecolor="rgba(255,255,255,.08)",tickfont=dict(size=10)),"title":dict(text="Monthly Collection Rate (%)",font=dict(color="#E8F0FE",size=12))}))
        st.plotly_chart(f2,use_container_width=True)
    shdr("Payer Quadrant — AR Days vs Collection Rate")
    pm=df.groupby("Insurance_Type").agg(AR=("Accounts_Receivable_Days","mean"),CR=("Collection_Rate","mean"),Rev=("Actual_Revenue","sum")).reset_index()
    f3=px.scatter(pm,x="AR",y="CR",size="Rev",color="Insurance_Type",color_discrete_sequence=CS[:4],text="Insurance_Type",size_max=50)
    f3.update_traces(textposition="top center",textfont=dict(color="#E8F0FE",size=11))
    f3.update_layout(**cl({"height":320,"title":dict(text="Payer Quadrant (bubble=Revenue)",font=dict(color="#E8F0FE",size=12))}))
    st.plotly_chart(f3,use_container_width=True)
    _best_payer=pm.sort_values("CR",ascending=False).iloc[0]
    _worst_ar  =pm.sort_values("AR",ascending=False).iloc[0]
    ins("Key Insights",
        f"Avg AR days <strong>{ar:.0f}d</strong> — target is ≤30d. "
        f"Best collection rate: <strong>{_best_payer['Insurance_Type']}</strong> at {_best_payer['CR']:.1f}%. "
        f"Highest AR days: <strong>{_worst_ar['Insurance_Type']}</strong> at {_worst_ar['AR']:.0f}d — "
        f"prioritise collections follow-up. "
        f"Revenue at risk: <strong>₹{rar/1e6:.1f}M</strong> from slow-pay accounts.")

def pg_hub(df):
    ptitle("Analytics Hub","Comprehensive revenue analytics command center")
    kpis([
        ("Total Claims",f"{len(df):,}",f"Patients: {df['Patient_ID'].nunique():,}","pos"),
        ("Avg Rev/Claim",f"₹{df['Actual_Revenue'].mean():,.0f}","Per claim average","pos"),
        ("Charge Capture",f"{df['Charge_Capture_Efficiency'].mean():.1f}%","Network average","pos"),
        ("Leakage Index",f"{df['Revenue_Leakage_Index'].mean():.3f}","Lower is better","warn"),
    ])
    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        shdr("Revenue Heatmap — Dept x Month")
        hdf=df.pivot_table(values="Actual_Revenue",index="Department",columns="Month",aggfunc="sum",fill_value=0)/1e6
        hdf.columns=[calendar.month_abbr[int(m)] for m in hdf.columns]
        f=px.imshow(hdf,color_continuous_scale="Teal",labels=dict(color="Rev($M)"),aspect="auto")
        f.update_layout(**cl({"height":310,"title":dict(text="Revenue Heatmap: Dept x Month ($M)",font=dict(color="#E8F0FE",size=12))}))
        st.plotly_chart(f,use_container_width=True)
    with c2:
        shdr("Revenue by Admission Type & Year")
        a=df.groupby(["Admission_Type","Year"])["Actual_Revenue"].sum().reset_index()
        a["Rev_M"]=a["Actual_Revenue"]/1e6
        f2=px.bar(a,x="Year",y="Rev_M",color="Admission_Type",barmode="stack",color_discrete_sequence=CS)
        f2.update_layout(**cl({"height":310,"title":dict(text="Revenue by Admission Type & Year ($M)",font=dict(color="#E8F0FE",size=12))}))
        st.plotly_chart(f2,use_container_width=True)
    shdr("Department Statistics Summary")
    st2=df.groupby("Department").agg(Claims=("Claim_ID","count"),Revenue_M=("Actual_Revenue",lambda x:round(x.sum()/1e6,1)),Denial_Pct=("Denial_Flag",lambda x:round(x.mean()*100,1)),Avg_LOS=("Length_of_Stay",lambda x:round(x.mean(),1)),CCE=("Charge_Capture_Efficiency",lambda x:round(x.mean(),1)),AR_Days=("Accounts_Receivable_Days",lambda x:round(x.mean(),0))).reset_index()
    st.dataframe(st2,use_container_width=True,hide_index=True)
    _top_dept=st2.sort_values("Revenue_M",ascending=False).iloc[0]
    _low_cce =st2.sort_values("CCE",ascending=True).iloc[0]
    ins("Key Insights",
        f"<strong>{_top_dept['Department']}</strong> leads with ₹{_top_dept['Revenue_M']:.1f}M revenue "
        f"across {int(_top_dept['Claims']):,} claims. "
        f"<strong>{_low_cce['Department']}</strong> has the lowest charge capture efficiency ({_low_cce['CCE']:.1f}%) "
        f"— targeted coding audits recommended. "
        f"Overall avg LOS {st2['Avg_LOS'].mean():.1f}d; departments above 5d should review discharge protocols.")

def pg_rev_perf(df):
    ptitle("Revenue Performance","Actual vs expected revenue deep dive")
    gap=df["Expected_Revenue"].sum()-df["Actual_Revenue"].sum()
    y23=df[df["Year"]==2023]["Actual_Revenue"].sum(); y24=df[df["Year"]==2024]["Actual_Revenue"].sum()
    yoy=(y24-y23)/y23*100 if y23>0 else 0
    kpis([
        ("Revenue Gap",f"₹{gap/1e6:.1f}M",f"{gap/df['Expected_Revenue'].sum()*100:.1f}% below expected","neg"),
        ("2023 Revenue",f"₹{y23/1e9:.2f}B","FY 2023","pos"),
        ("2024 Revenue",f"₹{y24/1e9:.2f}B",f"YoY: {yoy:+.1f}%","pos" if yoy>0 else "neg"),
        ("Net Revenue",f"₹{df['Net_Revenue'].sum()/1e9:.2f}B","After leakage","pos"),
    ])
    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        shdr("YoY Revenue by Department")
        yd=df.groupby(["Department","Year"])["Actual_Revenue"].sum().reset_index(); yd["Rev_M"]=yd["Actual_Revenue"]/1e6
        f=px.bar(yd,x="Department",y="Rev_M",color="Year",barmode="group",color_discrete_sequence=["#4FC3F7","#00D4AA"])
        f.update_layout(**cl({"height":300,"title":dict(text="YoY Revenue by Dept ($M)",font=dict(color="#E8F0FE",size=12))}))
        st.plotly_chart(f,use_container_width=True)
    with c2:
        shdr("Quarterly Revenue")
        q=df.groupby("YearQ")["Actual_Revenue"].sum().reset_index().sort_values("YearQ")
        qd=q["Actual_Revenue"].diff().fillna(0)
        f2=go.Figure(go.Bar(x=q["YearQ"],y=q["Actual_Revenue"]/1e6,marker=dict(color=["#00D4AA" if d>=0 else "#FF4757" for d in qd]),text=[f"₹{v/1e6:.0f}M" for v in q["Actual_Revenue"]],textposition="outside",textfont=dict(color="#E8F0FE",size=9)))
        f2.update_layout(**cl({"height":300,"title":dict(text="Quarterly Revenue ($M)",font=dict(color="#E8F0FE",size=12))}))
        st.plotly_chart(f2,use_container_width=True)
    shdr("Revenue Achievement vs Leakage Matrix")
    pm=df.groupby("Department").agg(A=("Actual_Revenue","sum"),E=("Expected_Revenue","sum"),L=("Revenue_Leakage","sum")).reset_index()
    pm["Ach"]=pm["A"]/pm["E"]*100; pm["LR"]=pm["L"]/pm["E"]*100
    f3=px.scatter(pm,x="Ach",y="LR",size="A",color="Department",color_discrete_map=CD,text="Department",size_max=55)
    f3.add_hline(y=pm["LR"].mean(),line_dash="dot",line_color="rgba(255,193,7,.5)")
    f3.add_vline(x=100,line_dash="dot",line_color="rgba(0,212,170,.5)",annotation_text="100% Target")
    f3.update_traces(textposition="top center",textfont=dict(color="#E8F0FE",size=10))
    f3.update_layout(**cl({"height":340,"title":dict(text="Dept Performance Matrix",font=dict(color="#E8F0FE",size=12))}))
    st.plotly_chart(f3,use_container_width=True)
    _best_dept=pm.sort_values("Ach",ascending=False).iloc[0]
    _worst_dept=pm.sort_values("LR",ascending=False).iloc[0]
    ins("Key Insights",
        f"YoY revenue growth: <strong>{yoy:+.1f}%</strong> from ₹{y23/1e9:.2f}B (2023) to ₹{y24/1e9:.2f}B (2024). "
        f"Revenue gap vs expected: <strong>₹{gap/1e6:.1f}M</strong> ({gap/df['Expected_Revenue'].sum()*100:.1f}%). "
        f"<strong>{_best_dept['Department']}</strong> achieves highest revenue target at {_best_dept['Ach']:.1f}%. "
        f"<strong>{_worst_dept['Department']}</strong> shows highest leakage rate ({_worst_dept['LR']:.1f}%) — requires intervention.")

def pg_procedure(df):
    ptitle("Procedure Code Analysis","Revenue, denial and efficiency by procedure")
    proc=df.groupby("Procedure_Code").agg(Count=("Claim_ID","count"),Revenue=("Actual_Revenue","sum"),DR=("Denial_Flag","mean"),AvgRev=("Actual_Revenue","mean"),Leakage=("Revenue_Leakage","sum")).reset_index().sort_values("Revenue",ascending=False)
    proc["DR"]*=100
    kpis([
        ("Unique Procedures",f"{df['Procedure_Code'].nunique()}","Active codes","pos"),
        ("Top Procedure Rev",f"₹{proc.iloc[0]['Revenue']/1e6:.1f}M",proc.iloc[0]["Procedure_Code"],"pos"),
        ("Highest Denial Code",proc.sort_values("DR",ascending=False).iloc[0]["Procedure_Code"],f"{proc.sort_values('DR',ascending=False).iloc[0]['DR']:.1f}% denial","neg"),
        ("Avg Rev/Claim",f"₹{df['Actual_Revenue'].mean():,.0f}","Per claim","pos"),
    ])
    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        shdr("Top 10 by Revenue")
        t10=proc.head(10)
        f=px.bar(t10,x="Procedure_Code",y="Revenue",color="DR",color_continuous_scale="RdYlGn_r",text=[f"₹{v/1e6:.1f}M" for v in t10["Revenue"]])
        f.update_traces(textposition="outside",textfont=dict(color="#E8F0FE"))
        f.update_layout(**cl({"height":300,"coloraxis_showscale":False,"title":dict(text="Top 10 Procedures by Revenue",font=dict(color="#E8F0FE",size=12))}))
        st.plotly_chart(f,use_container_width=True)
    with c2:
        shdr("Denial Rate by Procedure")
        ps=proc.sort_values("DR",ascending=True)
        f2=go.Figure(go.Bar(x=ps["DR"],y=ps["Procedure_Code"],orientation="h",marker=dict(color=ps["DR"],colorscale="RdYlGn_r"),text=[f"{r:.1f}%" for r in ps["DR"]],textposition="outside",textfont=dict(color="#E8F0FE")))
        f2.update_layout(**cl({"height":300,"title":dict(text="Denial Rate by Procedure (%)",font=dict(color="#E8F0FE",size=12))}))
        st.plotly_chart(f2,use_container_width=True)
    shdr("Procedure Performance Matrix")
    f3=px.scatter(proc,x="AvgRev",y="Leakage",size="Count",color="DR",color_continuous_scale="RdYlGn_r",text="Procedure_Code",size_max=45)
    f3.update_traces(textposition="top center",textfont=dict(color="#E8F0FE",size=9))
    f3.update_layout(**cl({"height":330,"title":dict(text="Procedure: Avg Revenue vs Leakage (bubble=Volume)",font=dict(color="#E8F0FE",size=12))}))
    st.plotly_chart(f3,use_container_width=True)
    _high_den=proc.sort_values("DR",ascending=False).iloc[0]
    _low_den =proc.sort_values("DR",ascending=True).iloc[0]
    ins("Key Insights",
        f"Top revenue procedure: <strong>{proc.iloc[0]['Procedure_Code']}</strong> "
        f"(₹{proc.iloc[0]['Revenue']/1e6:.1f}M across {int(proc.iloc[0]['Count']):,} claims). "
        f"Highest denial procedure: <strong>{_high_den['Procedure_Code']}</strong> at {_high_den['DR']:.1f}% — "
        f"review prior-auth requirements. "
        f"<strong>{_low_den['Procedure_Code']}</strong> has the best approval rate ({100-_low_den['DR']:.1f}%). "
        f"Avg revenue per claim: <strong>₹{df['Actual_Revenue'].mean():,.0f}</strong>.")

def pg_compliance(df):
    ptitle("Compliance Overview","Billing compliance, risk indicators and audit metrics")
    hr=(df["Denial_Risk_Category"]=="High Risk").sum(); ar=df["Billing_Anomaly"].mean()*100
    drr=df["Denial_Flag"].mean()*100; dp=(df["Documentation_Delay_Days"]>5).mean()*100
    kpis([
        ("High Risk Claims",f"{hr:,}",f"{hr/len(df)*100:.1f}% of portfolio","neg"),
        ("Billing Anomaly Rate",f"{ar:.1f}%","Upcoding + Undercoding","neg"),
        ("Claim Denial Rate",f"{drr:.1f}%","Target < 10%","warn" if drr>10 else "pos"),
        ("Doc Delay > 5d",f"{dp:.1f}%","Compliance risk factor","warn"),
    ])
    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        shdr("Risk Score Distribution")
        f=px.histogram(df,x="Denial_Risk_Score",nbins=40,color_discrete_sequence=[CS[0]])
        f.add_vline(x=0.33,line_dash="dot",line_color="#FFC107",annotation_text="Low/Med",annotation_font_color="#FFC107")
        f.add_vline(x=0.66,line_dash="dot",line_color="#FF4757",annotation_text="Med/High",annotation_font_color="#FF4757")
        f.update_layout(**cl({"height":290,"title":dict(text="Denial Risk Score Distribution",font=dict(color="#E8F0FE",size=12))}))
        st.plotly_chart(f,use_container_width=True)
    with c2:
        shdr("Compliance Risk by Department")
        comp=df.groupby("Department").agg(AR2=("Billing_Anomaly","mean"),DR2=("Denial_Flag","mean")).reset_index()
        comp["AR2"]*=100; comp["DR2"]*=100
        f2=go.Figure()
        f2.add_trace(go.Bar(name="Anomaly%",x=comp["Department"],y=comp["AR2"],marker_color="#FF4757",opacity=0.8))
        f2.add_trace(go.Bar(name="Denial%",x=comp["Department"],y=comp["DR2"],marker_color="#FFC107",opacity=0.8))
        f2.update_layout(**cl({"height":290,"barmode":"group","title":dict(text="Dept Compliance Risk",font=dict(color="#E8F0FE",size=12))}))
        st.plotly_chart(f2,use_container_width=True)
    shdr("Monthly Compliance Trend")
    mc=df.groupby("Month_Year").agg(AR3=("Billing_Anomaly","mean"),DR3=("Denial_Flag","mean"),RS=("Denial_Risk_Score","mean")).reset_index().sort_values("Month_Year")
    mc["AR3"]*=100; mc["DR3"]*=100
    f3=go.Figure()
    f3.add_trace(go.Scatter(x=mc["Month_Year"],y=mc["AR3"],name="Anomaly%",line=dict(color="#FF4757",width=2.5),fill="tozeroy",fillcolor="rgba(255,71,87,.07)"))
    f3.add_trace(go.Scatter(x=mc["Month_Year"],y=mc["DR3"],name="Denial%",line=dict(color="#FFC107",width=2.5)))
    f3.add_trace(go.Scatter(x=mc["Month_Year"],y=mc["RS"]*100,name="Risk x100",line=dict(color="#A78BFA",width=2,dash="dash")))
    f3.update_layout(**cl({"height":310,"title":dict(text="Monthly Compliance Indicators",font=dict(color="#E8F0FE",size=12))}))
    st.plotly_chart(f3,use_container_width=True)
    ins("Compliance Alert",f"{hr:,} high-risk claims. Anomaly rate {ar:.1f}%. Doc delays ({dp:.1f}%) = direct denial risk.")

def pg_ar(df):
    ptitle("AR & Settlement Analysis","Accounts receivable aging and settlement monitoring")
    ar=df["Accounts_Receivable_Days"].mean(); sd=df["Settlement_Days"].mean()
    o60=(df["Accounts_Receivable_Days"]>60).sum(); rar=df["Revenue_at_Risk"].sum()
    kpis([
        ("Avg AR Days",f"{ar:.0f}d","Target <= 30d","warn" if ar>30 else "pos"),
        ("Avg Settlement",f"{sd:.0f}d","Claim-to-payment","warn" if sd>30 else "pos"),
        ("Claims > 60 AR Days",f"{o60:,}","Aging bucket risk","neg"),
        ("Revenue at Risk",f"₹{rar/1e6:.1f}M","Unpaid exposure","neg"),
    ])
    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        shdr("AR Aging Buckets")
        dc=df.copy(); dc["AB"]=pd.cut(dc["Accounts_Receivable_Days"],[0,15,30,45,60,200],labels=["0-15d","16-30d","31-45d","46-60d","60+d"])
        ab=dc.groupby("AB",observed=True).agg(Count=("Claim_ID","count"),RAR=("Revenue_at_Risk","sum")).reset_index()
        f=go.Figure()
        f.add_trace(go.Bar(x=ab["AB"].astype(str),y=ab["Count"],name="Count",marker_color=["#00D4AA","#4FC3F7","#FFC107","#FF6B35","#FF4757"]))
        f.add_trace(go.Scatter(x=ab["AB"].astype(str),y=ab["RAR"]/1e6,name="RAR($M)",mode="markers+lines",yaxis="y2",marker=dict(color="#A78BFA",size=9),line=dict(color="#A78BFA",width=2)))
        f.update_layout(**cl({"height":290,"title":dict(text="AR Aging Buckets",font=dict(color="#E8F0FE",size=12)),"yaxis2":dict(overlaying="y",side="right",gridcolor="rgba(0,0,0,0)",tickfont=dict(color="#A78BFA"))}))
        st.plotly_chart(f,use_container_width=True)
    with c2:
        shdr("Settlement Days by Insurance")
        si=df.groupby("Insurance_Type")["Settlement_Days"].mean().reset_index()
        sis=si.sort_values("Settlement_Days",ascending=False)
        f2=px.bar(sis,x="Insurance_Type",y="Settlement_Days",color="Settlement_Days",color_continuous_scale="RdYlGn_r",text=[f"{d:.0f}d" for d in sis["Settlement_Days"]])
        f2.add_hline(y=30,line_dash="dot",line_color="#FFC107",annotation_text="30d",annotation_font_color="#FFC107")
        f2.update_traces(textposition="outside",textfont=dict(color="#E8F0FE"))
        f2.update_layout(**cl({"height":290,"coloraxis_showscale":False,"title":dict(text="Settlement Days by Insurance",font=dict(color="#E8F0FE",size=12))}))
        st.plotly_chart(f2,use_container_width=True)
    shdr("AR & Settlement Trend")
    ma=df.groupby("Month_Year").agg(AR3=("Accounts_Receivable_Days","mean"),SD=("Settlement_Days","mean"),RAR=("Revenue_at_Risk","sum")).reset_index().sort_values("Month_Year")
    f3=go.Figure()
    f3.add_trace(go.Scatter(x=ma["Month_Year"],y=ma["AR3"],name="Avg AR Days",line=dict(color="#4FC3F7",width=2.5),fill="tozeroy",fillcolor="rgba(79,195,247,.06)"))
    f3.add_trace(go.Scatter(x=ma["Month_Year"],y=ma["SD"],name="Settlement Days",line=dict(color="#A78BFA",width=2.5,dash="dash")))
    f3.add_trace(go.Bar(x=ma["Month_Year"],y=ma["RAR"]/1e6,name="RAR($M)",marker_color="rgba(255,71,87,.4)",yaxis="y2"))
    f3.add_hline(y=30,line_dash="dot",line_color="#FFC107",annotation_text="30d Target",annotation_font_color="#FFC107")
    f3.update_layout(**cl({"height":320,"title":dict(text="AR & Settlement Trends + Revenue at Risk",font=dict(color="#E8F0FE",size=12)),"yaxis2":dict(overlaying="y",side="right",gridcolor="rgba(0,0,0,0)",tickfont=dict(color="#FF4757"))}))
    st.plotly_chart(f3,use_container_width=True)
    ins("AR Insight",f"Avg AR {ar:.0f}d, settlement {sd:.0f}d. {o60:,} claims exceed 60-day threshold.")

# ── ROUTER ────────────────────────────────────────────────────────────────────
ROUTES = {
    "Executive Overview":      pg_exec,
    "Revenue Leakage":         pg_leakage,
    "Revenue Forecasting":     pg_forecast,
    "Denial Intelligence":     pg_denial,
    "Billing Anomalies":       pg_anomaly,
    "Department Overview":     pg_dept,
    "Dept Revenue Trends":     pg_rev_perf,
    "Patient & LOS Analytics": pg_patient_los,
    "Billing Dashboard":       pg_billing,
    "Anomaly Detection":       pg_anomaly,
    "Denial Management":       pg_denial,
    "Insurance & Collections": pg_insurance,
    "Analytics Hub":           pg_hub,
    "Revenue Performance":     pg_rev_perf,
    "Leakage Deep Dive":       pg_leakage,
    "Procedure Analysis":      pg_procedure,
    "Compliance Overview":     pg_compliance,
    "Anomaly Audit":           pg_anomaly,
    "Denial Root Cause":       pg_denial,
    "AR & Settlement":         pg_ar,
}

# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    if not st.session_state.get("authenticated", False):
        login_page()
        return
    with st.spinner("Loading data..."):
        df_full = load_data()
    df = render_sidebar(df_full)
    if df.empty:
        st.warning("No data matches the current filters.")
        return
    page = st.session_state.get("page","")
    fn   = ROUTES.get(page)
    if fn:
        fn(df)
    else:
        pg_exec(df)

if __name__ == "__main__":
    main()