import streamlit as st
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from app.data_loader import load_data, apply_styles, render_sidebar, COLOR_MAP, footer

st.set_page_config(
    page_title="PulseMap India",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_styles()
render_sidebar()
df = load_data()

# ── Hero Banner ────────────────────────────────
st.markdown("""
<div class='hero-banner'>
    <div class='hero-title'>🗺️ PulseMap India</div>
    <div class='hero-subtitle'>
        District-level preventable disease risk intelligence across 707 Indian districts
        · Built with Python, Pandas, Plotly & Streamlit
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ──────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Districts Analyzed", f"{len(df):,}")
with col2:
    critical = len(df[df['risk_tier'] == 'Critical Risk'])
    st.metric("Critical Risk Districts", critical)
with col3:
    st.metric("Avg Risk Score", f"{df['risk_score'].mean():.1f} / 100")
with col4:
    st.metric("States & UTs", df['state'].nunique())

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ── About ──────────────────────────────────────
st.markdown("<div class='section-header'>🎯 About This Project</div>",
            unsafe_allow_html=True)
st.markdown("""
<div style='font-size:0.95rem; color:#94a3b8; line-height:1.8; max-width:900px;'>
    This dashboard analyzes <strong style='color:#e8eaf0;'>707 Indian districts</strong> 
    across 36 States & UTs using NFHS-5 (2019–21) data to build a composite 
    <strong style='color:#e8eaf0;'>Health Risk Score</strong> based on 19 indicators — 
    covering clinical health outcomes, cancer screening coverage, gender health gaps, 
    and social determinants of health. Districts are classified into 4 risk tiers 
    using K-Means clustering to enable actionable, data-backed intervention planning.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ── Key Insights ───────────────────────────────
st.markdown("<div class='section-header'>💡 Key Insights</div>",
            unsafe_allow_html=True)

insights = [
    ("📈", "Critical Districts",
    "77 districts (10.9%) fall in the Critical Risk tier - "
    "with the highest concentration in Bihar, Odisha, Chhattisgarh, Jharkhand and Northeast India."),
    ("🩸", "Anaemia Crisis",
     "Average women anaemia across India stands at 55.9% - "
     "Ladakh (90%+) and West Bengal (70%+) are worst affected."),
    ("🔬", "Cancer Screening Gap",
     "Cervical screening average is just 1.57% nationally - "
     "one of the lowest rates in the world for a preventable cancer."),
    ("⚖️", "Gender Health Gap",
     "Men show consistently higher BP and blood sugar than women - "
     "Uttarakhand has the highest BP gap at 9.72 percentage points."),
]

c1, c2, c3, c4 = st.columns(4)
for col, (icon, title, text) in zip([c1, c2, c3, c4], insights):
    with col:
        st.markdown(f"""
        <div class='insight-card'>
            <div class='insight-card-icon'>{icon}</div>
            <div class='insight-card-title'>{title}</div>
            <div class='insight-card-text'>{text}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ── Dashboard Pages ────────────────────────────
st.markdown("<div class='section-header'>📋 Dashboard Pages</div>",
            unsafe_allow_html=True)

pages = [
    ("📊", "Overview",
     "Risk tiers, critical districts & score distribution"),

    ("🗺️", "Risk Map",
     "State rankings and risk tier analysis"),

    ("🏥", "Health Indicators",
     "Anaemia, BP, diabetes and gender gaps"),

    ("🔬", "Cancer Screening",
     "Screening coverage across states"),

    ("🔍", "District Lookup",
     "District profile, metrics and comparison"),
]

cols = st.columns(5)
for col, (icon, title, desc) in zip(cols, pages):
    with col:
        st.markdown(f"""
        <div class='page-card'>
            <div class='page-card-icon'>{icon}</div>
            <div class='page-card-title'>{title}</div>
            <div class='page-card-desc'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div class='insight-box'>
    👈 <strong>Use the sidebar</strong> to navigate between pages.
</div>
""", unsafe_allow_html=True)

footer()