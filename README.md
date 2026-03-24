#  MEDILYTICS — Healthcare Revenue Intelligence Dashboard

##  Key Features

-  Interactive healthcare operations dashboard using Streamlit  
-  6-month revenue forecasting using ARIMA model  
-  Anomaly detection for identifying revenue leakage  
-  Secure login system with role-based access  
-  KPI tracking for claims, billing, and performance  

---

##  Dashboard Preview

> *(Add your screenshots in an `images/` folder)*

![Dashboard](images/dashboard.png)
<img width="379" height="561" alt="image" src="https://github.com/user-attachments/assets/4cf7bc98-04a6-4c83-abe0-317ea74711ca" />

![Login](images/login.png)

---

##  Introduction

MEDILYTICS is a healthcare operations and revenue analytics dashboard developed as part of the **Infosys Springboard Virtual Internship 6.0 (Batch 13)**.  

The project focuses on analyzing healthcare financial data, monitoring operational performance, and generating predictive insights using data analytics and machine learning techniques.

---

##  Internship

Developed as part of **Infosys Springboard Virtual Internship 6.0 (Batch 13)** under guided mentorship.

---

##  Objectives

- Design an interactive dashboard for healthcare operations monitoring  
- Analyze revenue and claims-related data for insights  
- Forecast future revenue trends using time-series modeling  
- Identify anomalies and inefficiencies in financial data  
- Support data-driven decision-making in healthcare  

---

##  Methodology

###  Data Preprocessing
- Handling missing values  
- Feature engineering for time-series  
- Monthly aggregation of revenue data  

###  Forecasting Model
- ARIMA (AutoRegressive Integrated Moving Average)  
- Captures trends & seasonality  
- Generates 6-month revenue forecast  

###  Anomaly Detection
- Detect abnormal revenue patterns  
- Identify potential leakage  

###  Visualization
- Time-series plots  
- KPI dashboards  
- Comparative analysis  

---

##  System Architecture

- **Data Layer** → Raw & processed datasets  
- **Model Layer** → Forecasting & anomaly detection  
- **Application Layer** → Streamlit dashboard  
- **Presentation Layer** → Interactive charts & KPIs  

---

##  Project Structure

```
Medilytics-Healthcare-Revenue-Intelligence-Dashboard/
│
├── data/ # Dataset files
├── app.py # Main dashboard
├── Login.py # Authentication
├── billing_anomaly.py
├── forecast_dashboard.py
├── Executive_Dashboard.py
├── style.css
└── README.md
```

---

##  Installation & Setup

```bash
git clone https://github.com/Munavvara-17/Medilytics-Healthcare-Revenue-Intelligence-Dashboard.git
cd Medilytics-Healthcare-Revenue-Intelligence-Dashboard
pip install -r requirements.txt
streamlit run app.py
