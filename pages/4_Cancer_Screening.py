import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from data_loader import (load_data, apply_styles, render_sidebar,
                         COLOR_MAP, plotly_layout, insight_box, footer)

st.set_page_config(page_title="Cancer Screening · PulseMap", page_icon="🔬", layout="wide")
apply_styles()
render_sidebar()
df = load_data()

st.markdown("<div class='page-title'>🔬 Cancer Screening</div>", unsafe_allow_html=True)
st.markdown("<div class='page-subtitle'>Preventive cancer screening coverage across Indian districts</div>",
            unsafe_allow_html=True)
st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# KPI cards
c1, c2, c3 = st.columns(3)
with c1: st.metric("Avg Cervical Screening", f"{df['cervical_screening_w'].mean():.2f}%")
with c2: st.metric("Avg Breast Examination", f"{df['breast_exam_w'].mean():.2f}%")
with c3: st.metric("Avg Oral Examination",   f"{df['oral_exam_w'].mean():.2f}%")

st.markdown("""
<div class='warning-banner'>
    ⚠️ <strong>Critical Gap:</strong> National average cervical cancer screening stands at 
    just <strong>1.57%</strong> — one of the lowest rates in the world for a fully preventable cancer. 
    Breast (0.65%) and oral (0.70%) screening are even lower. 
    These cancers are detectable early and treatable — the gap is entirely a healthcare access problem.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 0.8])

with col1:
    st.markdown("<div class='section-header'>📉 Bottom 10 States — Cancer Screening Coverage</div>",
                unsafe_allow_html=True)
    screening = (
        df.groupby('state')
        .agg(Cervical=('cervical_screening_w', 'mean'),
             Breast=('breast_exam_w', 'mean'),
             Oral=('oral_exam_w', 'mean'))
        .reset_index().sort_values('Cervical').head(10)
    )
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Cervical', y=screening['state'],
                         x=screening['Cervical'], orientation='h',
                         marker_color='#c0392b', opacity=0.9))
    fig.add_trace(go.Bar(name='Breast', y=screening['state'],
                         x=screening['Breast'], orientation='h',
                         marker_color='#e67e22', opacity=0.9))
    fig.add_trace(go.Bar(name='Oral', y=screening['state'],
                         x=screening['Oral'], orientation='h',
                         marker_color='#9b59b6', opacity=0.9))
    fig = plotly_layout(fig, height=440)
    fig.update_layout(barmode='group',
                      yaxis={'categoryorder': 'total ascending'},
                      legend=dict(orientation='v', y=1.05),
                      showlegend=True, title_text="")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("<div class='section-header'>📋 State-wise Coverage</div>",
                unsafe_allow_html=True)
    table = (
        df.groupby('state')
        .agg(Cervical=('cervical_screening_w', 'mean'),
             Breast=('breast_exam_w', 'mean'),
             Oral=('oral_exam_w', 'mean'))
        .round(2).reset_index().sort_values('Cervical')
        .rename(columns={'state': 'State', 'Cervical': 'Cervical (%)',
                         'Breast': 'Breast (%)', 'Oral': 'Oral (%)'})
    )
    st.dataframe(table, use_container_width=True, height=440)

insight_box(
        "4–5 of the bottom 10 states are from <strong>East and Northeast India</strong> — "
        "geographic isolation, limited specialist healthcare, and low awareness "
        "are primary drivers. Cervical screening is consistently lowest across all states."
    )

st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown("<div class='section-header'>📊 Cervical Screening vs Risk Score</div>",
            unsafe_allow_html=True)

fig2 = px.scatter(
    df, x='cervical_screening_w', y='risk_score', color='risk_tier',
    color_discrete_map=COLOR_MAP,
    hover_data={'district': True, 'state': True},
    labels={'cervical_screening_w': 'Cervical Screening Coverage (%)',
            'risk_score': 'Risk Score (0–100)', 'risk_tier': 'Risk Tier'},
    trendline='ols', opacity=0.7
)
fig2.update_traces(marker=dict(size=5))
fig2 = plotly_layout(fig2, height=380)
fig2.update_layout(legend=dict(orientation='v', y=1.05),
                    showlegend=True, title_text="")
st.plotly_chart(fig2, use_container_width=True)
insight_box(
    "Negative correlation confirmed — districts with higher screening coverage "
    "have lower overall risk scores. Screening is both a health outcome indicator "
    "and a proxy for healthcare system quality."
)

footer()