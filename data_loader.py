import os
import pathlib
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    base = pathlib.Path(__file__).parent
    path = base/ 'notebooks' / 'data' / 'pulsemap_final.xlsx'
    return pd.read_excel(path)

# ── Color map ──────────────────────────────────
COLOR_MAP = {
    'Low Risk':      '#27ae60',
    'Moderate Risk': '#f1c40f',
    'High Risk':     '#e67e22',
    'Critical Risk': '#c0392b'
}
TIER_ORDER = ['Low Risk', 'Moderate Risk', 'High Risk', 'Critical Risk']

# ── CSS loader ─────────────────────────────────
def apply_styles():
    css_path = pathlib.Path(__file__).parent / 'assets' / 'style.css'
    st.markdown(
        f"<style>{css_path.read_text()}</style>",
        unsafe_allow_html=True
    )

# ── Sidebar (branding + data info only) ────────
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center; padding:0.5rem 0;'>
            <div style='font-size:1.5rem;font-weight:700;'>
                🗺️ PulseMap
            </div>
            <div style='font-size:0.8rem;color:#7b8599;'>
                India Health Risk Intelligence
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Navigation
        st.page_link("app.py", label="🏠 Home")
        st.page_link("pages/1_Overview.py", label="📊 Overview")
        st.page_link("pages/2_Risk_Map.py", label="🗺️ Risk Map")
        st.page_link("pages/3_Health_Indicators.py", label="🏥 Health Indicators")
        st.page_link("pages/4_Cancer_Screening.py", label="🔬 Cancer Screening")
        st.page_link("pages/5_District_Lookup.py", label="🔍 District Lookup")

        st.divider()

        st.markdown("""
        <div style='font-size:0.78rem;'>
            <strong>Data Source</strong><br>
            NFHS-5 (2019–21)<br>
            707 Districts · 36 States & UTs
        </div>
        """, unsafe_allow_html=True)

# ── Plotly dark theme ──────────────────────────
def plotly_layout(fig, height=420):
    fig.update_layout(
        height=height,
        paper_bgcolor='#161b27',
        plot_bgcolor='#161b27',
        font=dict(family='Inter', color='#7b8599', size=11),
        margin=dict(l=10, r=10, t=45, b=10),
        title=dict(font=dict(family='Space Grotesk', size=14, color='#a0aabe'), x=0),
        legend=dict(bgcolor='#161b27', bordercolor='#1e2738',
                    borderwidth=1, font=dict(color='#a0aabe')),
        xaxis=dict(gridcolor='#1e2738', zerolinecolor='#1e2738',
                   tickfont=dict(color='#7b8599')),
        yaxis=dict(gridcolor='#1e2738', zerolinecolor='#1e2738',
                   tickfont=dict(color='#7b8599')),
    )
    return fig

# ── Insight box helper ─────────────────────────
def insight_box(text: str):
    st.markdown(
        f"<div class='insight-box'>💡 {text}</div>",
        unsafe_allow_html=True
    )

# ── Footer helper ──────────────────────────────
def footer():
    st.markdown("""
    <div class='footer-text'>
        Built by <strong>Asheer Ahmad</strong> · 
        <a href='https://github.com/asheeransari'>GitHub</a> · 
        <a href='https://linkedin.com/in/asheer-an'>LinkedIn</a><br>
        Data: NFHS-5 (2019–21) · Government of India · 
        Python · Pandas · Plotly · Streamlit
    </div>
    """, unsafe_allow_html=True)