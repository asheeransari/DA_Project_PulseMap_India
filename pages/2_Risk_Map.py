import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from data_loader import (load_data, apply_styles, render_sidebar,
                         COLOR_MAP, TIER_ORDER, plotly_layout,
                         insight_box, footer)

st.set_page_config(page_title="Risk Map · PulseMap", page_icon="🗺️", layout="wide")
apply_styles()
render_sidebar()
df = load_data()

st.markdown("<div class='page-title'>🗺️ Risk Map</div>", unsafe_allow_html=True)
st.markdown("<div class='page-subtitle'>State-level risk comparison across India</div>",
            unsafe_allow_html=True)
st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# State summary
state_df = (
    df.groupby('state')
    .agg(
        avg_risk_score=('risk_score', 'mean'),
        total_districts=('district', 'count'),
        critical=('risk_tier', lambda x: (x == 'Critical Risk').sum()),
        high=('risk_tier', lambda x: (x == 'High Risk').sum()),
        moderate=('risk_tier', lambda x: (x == 'Moderate Risk').sum()),
        low=('risk_tier', lambda x: (x == 'Low Risk').sum()),
    )
    .round(2).reset_index()
    .sort_values('avg_risk_score', ascending=False)
)

col1, col2 = st.columns([1.3, 0.7])

with col1:
    st.markdown("<div class='section-header'>📊 States by Average Risk Score</div>",
                unsafe_allow_html=True)
    fig = px.bar(
        state_df.head(20),
        x='avg_risk_score', y='state', orientation='h',
        color='avg_risk_score',
        color_continuous_scale=[[0,'#27ae60'],[0.3,'#f1c40f'],
                                 [0.6,'#e67e22'],[1,'#c0392b']],
        text='avg_risk_score',
        labels={'avg_risk_score': 'Avg Risk Score', 'state': ''}
    )
    fig.update_traces(
        texttemplate='%{text:.1f}', textposition='outside',
        textfont=dict(color='#7b8599', size=10)
    )
    fig = plotly_layout(fig, height=580)
    fig.update_layout(yaxis={'categoryorder': 'total ascending'},
                      coloraxis_showscale=False,
                      title_text="")
    st.plotly_chart(fig,use_container_width = True)

with col2:
    st.markdown("<div class='section-header'>📋 State Summary</div>",
                unsafe_allow_html=True)
    display = state_df.rename(columns={
        'state': 'State', 'avg_risk_score': 'Avg Score',
        'total_districts': 'Districts', 'critical': '🔴',
        'high': '🟠', 'moderate': '🟡', 'low': '🟢'
    })
    st.dataframe(display, use_container_width=True, height=580)

insight_box(
    "<strong>Tripura</strong> has 100% of its districts in Critical Risk — "
    "every single district needs immediate intervention. "
    "Odisha (15 critical districts) and Jharkhand (10) follow closely."
)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown("<div class='section-header'>🏗️ Risk Tier Breakdown — Top 15 States</div>",
            unsafe_allow_html=True)

top15 = state_df.head(15)['state'].tolist()
tier_counts = (
    df[df['state'].isin(top15)]
    .groupby(['state', 'risk_tier']).size()
    .reset_index(name='count')
)

fig2 = px.bar(tier_counts, x='state', y='count', color='risk_tier',
              color_discrete_map=COLOR_MAP,
              category_orders={'risk_tier': TIER_ORDER},
              labels={'count': 'Districts', 'state': '', 'risk_tier': 'Risk Tier'})
fig2 = plotly_layout(fig2, height=380)
fig2.update_layout(barmode='stack', xaxis_tickangle=-30,showlegend=True, title_text="")
st.plotly_chart(fig2, use_container_width=True)

insight_box(
    "Stacked view reveals that even states like <strong>Assam and West Bengal</strong> "
    "with many districts have no Low Risk districts — "
    "the entire state needs systemic health intervention."
)

footer()