# Medilytics — Revenue Intelligence Dashboard

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. File Layout (keep all in the same folder)
```
your_folder/
├── app.py
├── requirements.txt
├── medlogo.png                    ← Your Medilytics logo
└── pre_processed_data_updated.csv ← Enriched dataset (provided)
```

> **Note:** The favicon/taskbar icon is set via `page_icon="Medlogo.py"` in the code
> (as requested). Streamlit will use `medlogo.png` from the working directory.

### 3. Run
```bash
streamlit run app.py
```

---

## 🔐 Login Credentials

| Role            | Username         | Password       |
|-----------------|------------------|----------------|
| CFO             | cfo_sharma       | CFO@Med2024    |
| Department Head | dept_priya       | Dept@Head99    |
| Billing Team    | billing_ravi     | Billing#123    |
| Revenue Analyst | analyst_meera    | Analyst$2024   |
| Operations Head | ops_arjun        | Ops&Health1    |

---

## 📋 Role → Pages Mapping

### 👔 CFO (cfo_sharma)
| Page | KPIs | Charts |
|------|------|--------|
| Executive Overview | Total Revenue, Leakage, Denial Rate, Expected Rev | Monthly trend, Dept pie, Quarterly bar, Dept matrix |
| Revenue Forecasting | Last Month Rev, Avg Forecast, Projected Growth, Peak Month | ARIMA forecast with CI, Forecast table, Insurance mix |
| Revenue Leakage Analysis | Total Leakage, Leakage Index, High-Risk Claims, Denial-driven Leakage | Dept bar, Insurance scatter, Monthly trend, Heatmap |
| Claim Denial Prediction | Denial Rate, Avg Risk Score, High-Risk Claims, Avg Settlement Days | Heatmap, Risk distribution, Feature importance, Monthly denials |
| Billing Anomalies | Anomalous %, Overcoded, Undercoded, Avg Doc Delay | Scatter plot, Dept anomaly bar, Variance histogram, Procedure anomaly |

### 🩺 Department Head (dept_priya)
| Page | KPIs | Charts |
|------|------|--------|
| Department Performance | Top Dept, Best CCE, Lowest Denial, Avg LOS | Revenue vs Expected, Bubble chart, LOS by type, AR days |
| Doctor-wise Revenue | Top Doctor, Total Doctors, Avg Rev/Doctor, Best CCE | Top 10 bar, Rev/claim scatter, Leaderboard table |
| Admission Analytics | Total Admissions, Elective%, Emergency%, Avg LOS | Monthly area, Revenue share pie, LOS box, Heatmap |
| Charge Capture Efficiency | Hospital CCE, Best/Worst Dept, Claims<95% | CCE trend, Procedure bar, Scatter, Violin |

### 💳 Billing Team (billing_ravi)
| Page | KPIs | Charts |
|------|------|--------|
| Claims Dashboard | Total Claims, Approved, Denied, Avg Settlement | Insurance grouped bar, Payment scatter, Treemap, Weekly trend |
| Denial Management | Total Denials, Denial Rate, Recovery Potential, Repeat% | Monthly dual-axis, Denial reasons pie, Heatmap, Settlement box |
| Settlement Tracker | Avg Settlement, Fast/Slow Payer%, Total Paid | Violin, Monthly bar, Payer scorecard, Target vs Actual |
| AR Aging Analysis | Avg AR Days, AR>60d, Claims>90d, Revenue at Risk | Aging bar, Value by bucket, Dept bar, Monthly trend |

### 📊 Revenue Analyst (analyst_meera)
| Page | KPIs | Charts |
|------|------|--------|
| Revenue Deep Dive | Total Revenue, YoY Growth, Avg Claim Value, Collection Efficiency | Waterfall, Procedure bar, YoY comparison, Box plot |
| Payer Mix Analysis | Best Reimbursement, Avg Reimb Rate, Private Share, Govt Denial | Dual-axis bar, Area chart, Payer scorecard |
| Procedure Revenue | Top Procedure, Unique Procedures, Highest Rev, Avg Rev | Horizontal bar, Bubble chart, Line trend, Scatter |
| Trend Analysis | Peak Month, Volatility, Anomalous Months, Claim Growth | MA trend with anomalies, Seasonality index, CCE trend, Denial trend |

### ⚙️ Operations Head (ops_arjun)
| Page | KPIs | Charts |
|------|------|--------|
| Operational Overview | Active Beds, Avg LOS, Avg Doc Delay, Total Episodes | Dual-axis, Admission pie, Workload bar, Doc delay histogram |
| Bed Utilisation | Unique Beds, Total Bed-Days, Utilisation Rate, Avg LOS | LOS histogram, Monthly bed-days, Insurance/admission heatmap, High LOS bar |
| Length of Stay Impact | LOS-Revenue Correlation, Rev/Day, Highest Rev LOS, Short Stays | Scatter, Avg rev by LOS category, AR scatter, Quarterly trend |
| Workflow Bottlenecks | Doc Delay, AR Days, Settlement Days, Total Cycle | Funnel, Bottleneck bar, Dept delays grouped, AR risk scatter |

---

## 🧮 ARIMA Revenue Forecasting
- Uses pure NumPy-based AR(2) + MA(1) model (no statsmodels dependency required at runtime)
- Trains on 24 months of monthly revenue data
- Projects 6 months forward with ±12% confidence bands
- If statsmodels is installed, can be upgraded to full ARIMA(2,1,2) for higher accuracy

## 📦 Dataset
- Input: `pre_processed_data.csv` (60,000 claims, 29 columns)
- Enriched: `pre_processed_data_updated.csv` (+7 derived columns):
  - `Month`, `Quarter`, `Year`, `Month_Num`
  - `Collection_Rate` — Payment Received / Billing Amount × 100
  - `Denial_Risk_Score` — weighted composite of denial predictors
  - `Billing_Anomaly_Flag` — flags billing > 1.5× or < 0.5× expected revenue
