import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from data_loader import (load_data, apply_styles, render_sidebar,
                         COLOR_MAP, TIER_ORDER, plotly_layout,
                         insight_box, footer)

st.set_page_config(page_title="Health Indicators · PulseMap", page_icon="🏥", layout="wide")
apply_styles()
render_sidebar()
df = load_data()

st.markdown("<div class='page-title'>🏥 Health Indicators</div>", unsafe_allow_html=True)
st.markdown("<div class='page-subtitle'>Anaemia, blood sugar, blood pressure and gender health gap</div>",
            unsafe_allow_html=True)
st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# National KPIs
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Avg Anaemia (Women)", f"{df['anaemia_w'].mean():.1f}%")
with c2: st.metric("Avg Blood Sugar (Women)", f"{df['blood_sugar_w'].mean():.1f}%")
with c3: st.metric("Avg BP Elevated (Men)", f"{df['bp_elevated_m'].mean():.1f}%")
with c4: st.metric("Avg Female Literacy", f"{df['literacy_w'].mean():.1f}%")

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ── Anaemia ────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='section-header'>🩸 Top 10 States — Women Anaemia</div>",
                unsafe_allow_html=True)
    anaemia = (df.groupby('state')['anaemia_w'].mean()
               .reset_index().sort_values('anaemia_w', ascending=False).head(10))
    fig = px.bar(anaemia, x='anaemia_w', y='state', orientation='h',
                 color='anaemia_w',
                 color_continuous_scale=['#f1c40f', '#c0392b'],
                 text='anaemia_w',
                 labels={'anaemia_w': 'Anaemia (%)', 'state': ''})
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside',
                      textfont=dict(color='#7b8599', size=10))
    fig = plotly_layout(fig, height=400)
    fig.update_layout(yaxis={'categoryorder': 'total ascending'},
                      coloraxis_showscale=False,
                      showlegend=False, title_text="")
    st.plotly_chart(fig, use_container_width=True)
    insight_box(
        "<strong>Ladakh</strong> tops with 90%+ anaemia — extreme isolation and "
        "limited healthcare access are primary drivers. All top 10 states show 63%+ average."
    )

with col2:
    st.markdown("<div class='section-header'>💊 Gender Health Gap — Blood Pressure</div>",
                unsafe_allow_html=True)
    bp = (df.groupby('state')
          .agg(Women=('bp_elevated_w', 'mean'), Men=('bp_elevated_m', 'mean'))
          .reset_index().sort_values('Men', ascending=False).head(10))
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(name='Women', y=bp['state'], x=bp['Women'],
                          orientation='h', marker_color='#e74c3c', opacity=0.85))
    fig2.add_trace(go.Bar(name='Men', y=bp['state'], x=bp['Men'],
                          orientation='h', marker_color='#3498db', opacity=0.85))
    fig2 = plotly_layout(fig2, height=400)
    fig2.update_layout(barmode='group',
                       yaxis={'categoryorder': 'total ascending'},
                       legend=dict(orientation='v', y=1.05),
                       showlegend=True, title_text="")
    st.plotly_chart(fig2, use_container_width=True)
    insight_box(
        "<strong>Men consistently show higher BP</strong> across all states — "
        "Uttarakhand has the highest gap at 9.72 percentage points. "
        "Cardiovascular risk in men is a national pattern, not regional."
    )

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ── Literacy vs Risk Score ─────────────────────
st.markdown("<div class='section-header'>📚 Female Literacy vs Risk Score — District Level</div>",
            unsafe_allow_html=True)
fig3 = px.scatter(
    df, x='literacy_w', y='risk_score', color='risk_tier',
    color_discrete_map=COLOR_MAP,
    hover_data={'district': True, 'state': True,
                'risk_score': ':.1f', 'literacy_w': ':.1f'},
    labels={'literacy_w': 'Female Literacy Rate (%)',
            'risk_score': 'Risk Score (0–100)', 'risk_tier': 'Risk Tier'},
    trendline='ols', opacity=0.75,
    category_orders={'risk_tier': TIER_ORDER}
)
fig3.update_traces(marker=dict(size=6))
fig3 = plotly_layout(fig3, height=420)
fig3.update_layout(legend=dict(orientation='v', y=1.05),showlegend=True, title_text="")
st.plotly_chart(fig3, use_container_width=True)
insight_box(
    "Clear negative trend — as female literacy increases, risk score decreases. "
    "Every <strong>10% increase in literacy</strong> corresponds to ~2.3 point reduction "
    "in composite risk score. Education is the highest-ROI health intervention."
)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ── Gender Blood Sugar ─────────────────────────
st.markdown("<div class='section-header'>🩺 Gender Blood Sugar Gap — Top 15 States</div>",
            unsafe_allow_html=True)
bs = (df.groupby('state')
      .agg(Women=('blood_sugar_w', 'mean'), Men=('blood_sugar_m', 'mean'))
      .reset_index().sort_values('Men', ascending=False).head(15))
fig4 = go.Figure()
fig4.add_trace(go.Bar(name='Women', x=bs['state'], y=bs['Women'],
                      marker_color='#e74c3c', opacity=0.85))
fig4.add_trace(go.Bar(name='Men', x=bs['state'], y=bs['Men'],
                      marker_color='#3498db', opacity=0.85))
fig4 = plotly_layout(fig4, height=360)
fig4.update_layout(barmode='group', xaxis_tickangle=-30,
                   legend=dict(orientation='v', y=1.05),
                   showlegend=True, title_text="")
st.plotly_chart(fig4, use_container_width=True)
insight_box(
    "<strong>Sikkim</strong> shows the highest blood sugar gap (4.21 points) — "
    "men significantly more diabetic than women. "
    "Punjab and Chandigarh show negative gap — women higher than men, "
    "possibly linked to dietary patterns and lower physical activity."
)

footer()