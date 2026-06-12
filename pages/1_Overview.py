import streamlit as st
import plotly.express as px
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from app.data_loader import (
    load_data, apply_styles, render_sidebar,
    COLOR_MAP, TIER_ORDER, plotly_layout,
    insight_box, footer
)

st.set_page_config(
    page_title="Overview · PulseMap",
    page_icon="📊",
    layout="wide"
)

apply_styles()
render_sidebar()
df = load_data()

st.markdown("<div class='page-title'>📊 Overview</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='page-subtitle'>Risk tier distribution and highest risk districts</div>",
    unsafe_allow_html=True
)
st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ── Filters ─────────────────────────────────────
st.markdown(
    "<div class='section-header'>🔍 Explore by Filter</div>",
    unsafe_allow_html=True
)

f1, f2 = st.columns(2)

with f1:
    state_filter = st.multiselect(
        "Filter by State",
        options=sorted(df['state'].unique()),
        placeholder="All States"
    )

with f2:
    tier_filter = st.multiselect(
        "Filter by Risk Tier",
        options=TIER_ORDER,
        placeholder="All Risk Tiers"
    )

filtered_df = df.copy()

if state_filter:
    filtered_df = filtered_df[
        filtered_df['state'].isin(state_filter)
    ]

if tier_filter:
    filtered_df = filtered_df[
        filtered_df['risk_tier'].isin(tier_filter)
    ]

st.caption(
    f"Showing {len(filtered_df):,} districts across "
    f"{filtered_df['state'].nunique()} states/UTs"
)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# KPI row
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total Districts", f"{len(filtered_df):,}")

with c2:
    st.metric(
        "Critical Risk",
        len(
            filtered_df[
                filtered_df['risk_tier'] == 'Critical Risk'
            ]
        )
    )

with c3:
    st.metric(
        "Avg Risk Score",
        f"{filtered_df['risk_score'].mean():.1f}"
    )

with c4:
    st.metric(
        "States Covered",
        filtered_df['state'].nunique()
    )

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(
        "<div class='section-header'>🍩 Risk Tier Distribution</div>",
        unsafe_allow_html=True
    )

    tier_counts = (
        filtered_df['risk_tier']
        .value_counts()
        .reindex(TIER_ORDER, fill_value=0)
        .reset_index()
    )

    tier_counts.columns = ['Risk Tier', 'Districts']

    fig = px.pie(
        tier_counts,
        values='Districts',
        names='Risk Tier',
        hole=0.6,
        color='Risk Tier',
        color_discrete_map=COLOR_MAP
    )

    fig.update_traces(
        textposition='outside',
        textinfo='label+percent',
        textfont=dict(color='#a0aabe', size=11),
        marker=dict(line=dict(color='#0f1117', width=2))
    )

    fig = plotly_layout(fig, height=380)
    fig.update_layout(showlegend=False,title_text="")

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown(
        "<div class='section-header'>🔴 Top Critical Risk Districts</div>",
        unsafe_allow_html=True
    )

    top10 = (
        filtered_df[
            filtered_df['risk_tier'] == 'Critical Risk'
        ]
        .nlargest(10, 'risk_score')
        [['district', 'state', 'risk_score', 'risk_tier']]
        .reset_index(drop=True)
    )

    top10.index += 1
    top10.columns = ['District', 'State', 'Risk Score', 'Risk Tier']

    st.dataframe(
        top10,
        use_container_width=True,
        height=380
    )

col1, col2 = st.columns([1, 1])
with col1:
    insight_box(
    "66.5% of districts (470 of 707) fall in <strong>High or Critical Risk</strong> "
    "- highlighting the need for targeted health interventions nationwide."
    )

with col2:
    insight_box(
    "<strong>Bijapur, Chhattisgarh</strong> scores 100/100 — India's highest-risk district. "
    "Odisha and Chhattisgarh dominate the top 10."
    )


st.markdown("<hr class='divider'>", unsafe_allow_html=True)

st.markdown(
    "<div class='section-header'>📈 Risk Score Distribution</div>",
    unsafe_allow_html=True
)

fig2 = px.histogram(
    filtered_df,
    x='risk_score',
    color='risk_tier',
    color_discrete_map=COLOR_MAP,
    nbins=40,
    labels={
        'risk_score': 'Risk Score (0–100)',
        'count': 'Districts'
    },
    category_orders={
        'risk_tier': TIER_ORDER
    }

)


fig2 = plotly_layout(fig2, height=300)
fig2.update_layout(bargap=0.05,showlegend=True, title_text="")

st.plotly_chart(fig2, use_container_width=True)

insight_box(
    "Risk scores follow a roughly normal distribution with mean 39.6. "
    "The long right tail (60–100) represents 77 Critical Risk districts "
    "requiring immediate intervention."
)

footer()
