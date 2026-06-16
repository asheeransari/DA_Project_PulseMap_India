# 🗺️ PulseMap India — District Health Risk Intelligence

An end-to-end data analytics system that scores 707 Indian districts on preventable disease risk using NFHS-5 data — built with Python, SQL, Power BI, and a fully deployed Streamlit dashboard.

🔗 **Live Demo:** https://da-project-pulsemap-india-web-app.streamlit.app/ &nbsp;|&nbsp; 📊 **Power BI Dashboard:** [View PDF](https://drive.google.com/file/d/128gnVAyjF2bXeCpyk4uxJ1SVeTMxAPA8/view?usp=sharing) &nbsp;|&nbsp; 📄 **Analysis Report:** [View PDF](./reports/PulseMap_India_Analysis_Report.pdf)

---

## Project Info

This is an end-to-end Data Analysis project that builds a district-level Health Risk Intelligence system for India. The project covers the full analytics workflow — from raw government data cleaning to a deployed, production-ready web dashboard.

It demonstrates how a data analyst can transform a 109-column government survey into a structured composite Risk Score, segment districts using machine learning clustering, and deliver findings through both a Power BI dashboard and an interactive Streamlit web application — covering clinical health outcomes, cancer screening gaps, gender health disparities, and social determinants of health.

---

## Problem Statement

India's healthcare burden is distributed unevenly across districts, yet most public health planning happens at the state level — masking critical district-level variation. This project aims to answer key business questions:

- Which Indian districts carry the highest preventable disease risk?
- What social and environmental factors most strongly predict health outcomes?
- Is there a measurable gender health gap in blood sugar and blood pressure?
- How severe is the cancer screening gap, and which geographies need urgent intervention?
- Can districts be meaningfully segmented into risk tiers for targeted healthcare resource allocation?

---

## Key Insights

- **Critical Risk Concentration:** 77 districts (10.9%) fall in Critical Risk tier — concentrated in Bihar, Odisha, Chhattisgarh, Jharkhand, and Northeast India. Bijapur, Chhattisgarh scores 100/100, the highest risk district in India
- **Anaemia Crisis:** National average women anaemia stands at 55.9% — Ladakh records 92.76%, the highest in India, with all top 10 states exceeding 63%
- **Cancer Screening Gap:** Cervical cancer screening coverage is just 1.57% nationally — one of the lowest rates in the world for a fully preventable cancer
- **Gender Health Gap:** Men consistently show higher blood pressure and blood sugar than women across all states — Uttarakhand has the highest BP gap at 9.72 percentage points
- **Education as Intervention:** Female literacy shows the strongest negative correlation with risk score (-0.59) — every 10% increase in literacy corresponds to ~2-3 point reduction in risk

---

## Dashboard Pages

| Page | Description |
|------|-------------|
| 🏠 Home | Project overview, key insights, and navigation cards |
| 📊 Overview | Risk tier distribution, top critical districts, and score histogram |
| 🗺️ Risk Map | State-level risk ranking, tier breakdown, and summary table |
| 🏥 Health Indicators | Anaemia, BP, blood sugar, gender gap, and literacy correlation |
| 🔬 Cancer Screening | Coverage gap analysis across states — cervical, breast, and oral |
| 🔍 District Lookup | Deep dive into any district — risk gauge, indicators, and comparison |

---

## Power BI Dashboard

This project includes a parallel Power BI dashboard built on the same risk-scored dataset — covering the same core analysis through KPI cards, state-level risk maps, and drill-down tables across 5 pages.

Having both versions demonstrates the ability to work across code-based (Python/Streamlit) and drag-and-drop (Power BI) analytics environments — a practical skill expected in most Data Analyst roles.

🔗 [View Power BI Dashboard (PDF)](https://drive.google.com/file/d/REPLACE_WITH_YOUR_LINK/view?usp=drive_link)

---

## Analysis Report

A complete 23-page professional analysis report is included, covering methodology, all EDA findings, SQL query results, risk score derivation, and business recommendations for health insurers, NGOs, hospital chains, and government policy bodies.

📄 [View Full Analysis Report (PDF)](./reports/PulseMap_India_Analysis_Report.pdf)

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Data processing, cleaning, and risk score modeling |
| Pandas | Data cleaning, transformation, and aggregation |
| Scikit-learn | Min-Max normalization and K-Means clustering |
| SQLite + SQLAlchemy | Normalized database, business queries with CTEs and window functions |
| Matplotlib / Seaborn | Exploratory data analysis visualizations |
| Plotly | Interactive Streamlit visualizations |
| Streamlit | Multi-page web application framework |
| Power BI | Business intelligence dashboard |
| Git / GitHub | Version control and project hosting |
| CSS | Custom dark theme UI styling |

---

## Requirements

- Python 3.10+
- Git
- VS Code or any code editor

---

## Libraries Used

- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- sqlalchemy
- thefuzz
- plotly
- streamlit
- statsmodels

---

## Project Structure

```
pulsemap-india/
├── .streamlit/
│   └── config.toml             # Dark theme configuration
├── assets/
│   └── style.css                # Custom CSS styling
├── app.py                        # Main landing page
├── data_loader.py                 # Shared data loading & helper functions
├── pages/
│   ├── 1_Overview.py             # Risk tier distribution & critical districts
│   ├── 2_Risk_Map.py             # State-level risk comparison
│   ├── 3_Health_Indicators.py    # Anaemia, BP, blood sugar, gender gap
│   ├── 4_Cancer_Screening.py     # Screening coverage gap analysis
│   └── 5_District_Lookup.py      # District-level deep dive
├── notebooks/
│   ├── 01_data_cleaning.ipynb    # NFHS-5 data cleaning
│   ├── 02_eda.ipynb              # Exploratory data analysis
│   ├── 03_risk_scoring.ipynb     # Risk score & K-Means clustering
│   └── 04_database.ipynb         # SQLite database & SQL queries
├── sql/
│   ├── schema.sql                # Database schema
│   └── queries.sql               # Business queries (CTEs, window functions)
├── src/
│   ├── logger/                   # Custom logging module
│   └── exception/                # Custom exception handling
├── reports/
│   ├── *.png                     # 10 EDA visualization charts
│   └── PulseMap_India_Analysis_Report.pdf
├── setup.py                      # Python package configuration
├── requirements.txt              # Project dependencies
└── README.md
```

---

## Steps Used in This Project

1. Data Collection (NFHS-5, Government of India)
2. Data Cleaning and Validation
3. SQL Database Design and Business Query Writing
4. Exploratory Data Analysis (EDA)
5. Correlation and Statistical Analysis
6. Risk Score Feature Engineering
7. K-Means Clustering for Risk Tier Segmentation
8. Data Visualization
9. Power BI Dashboard Development
10. Streamlit Multi-page App Setup
11. Custom CSS Dark Theme Styling
12. Deployment on Streamlit Community Cloud
13. Analysis Report Writing and Documentation

---

## Limitations

- NFHS-5 data reflects 2019-21 conditions; NFHS-6 has not been published as of 2026
- Men's BMI and anaemia data was not available at district level in public NFHS-5 publications
- District-level healthcare infrastructure data (hospitals, beds, doctors) was not available in clean public format; health insurance coverage was used as a proxy
- The Risk Score is an exploratory composite index, not a clinically validated epidemiological model

Full details in Section 9 of the [Analysis Report](./reports/PulseMap_India_Analysis_Report.pdf).

---

## Author

**Asheer Ahmad Ansari** <br>
B.Tech Graduate (AI & Data Science) | Aspiring Data Analyst <br>
🔗 [LinkedIn](https://www.linkedin.com/in/asheer-an) &nbsp;|&nbsp; 🔗 [GitHub](https://github.com/asheeransari)