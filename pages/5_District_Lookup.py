import streamlit as st
import plotly.graph_objects as go
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from app.data_loader import (load_data, apply_styles, render_sidebar,
                         COLOR_MAP, plotly_layout, insight_box, footer)

st.set_page_config(page_title="District Lookup · PulseMap", page_icon="🔍", layout="wide")
apply_styles()
render_sidebar()
df = load_data()

st.markdown("<div class='page-title'>🔍 District Lookup</div>", unsafe_allow_html=True)
st.markdown("<div class='page-subtitle'>Deep dive into any district's health profile</div>",
            unsafe_allow_html=True)
st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# Selection
col1, col2 = st.columns(2)
with col1:
    selected_state = st.selectbox("Select State", sorted(df['state'].unique()))
with col2:
    districts = sorted(df[df['state'] == selected_state]['district'].unique())
    selected_district = st.selectbox("Select District", districts)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

row     = df[(df['state'] == selected_state) & (df['district'] == selected_district)].iloc[0]
national = df.mean(numeric_only=True)
state_avg = df[df['state'] == selected_state].mean(numeric_only=True)

badge_class = {
    'Low Risk': 'badge-low', 'Moderate Risk': 'badge-moderate',
    'High Risk': 'badge-high', 'Critical Risk': 'badge-critical'
}[row['risk_tier']]

# District header
st.markdown(f"""
<div style='display:flex; align-items:center; gap:1.2rem; margin-bottom:1.5rem;'>
    <div>
        <div style='font-family:Space Grotesk; font-size:1.8rem;
                    font-weight:700; color:#e8eaf0;'>{selected_district}</div>
        <div style='color:#7b8599; font-size:1rem; margin-top:2px;'>{selected_state}</div>
    </div>
    <span class='{badge_class}'>{row['risk_tier']}</span>
</div>
""", unsafe_allow_html=True)

gauge_color = COLOR_MAP[row['risk_tier']]
fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=row['risk_score'],
    number={'font': {'color': '#e8eaf0', 'family': 'Space Grotesk', 'size': 42}},
    title={'text': "Health Risk Score",
            'font': {'color': '#7b8599', 'size': 13}},
    gauge={
        'axis': {'range': [0, 100], 'tickcolor': '#3d4559',
                    'tickfont': {'color': '#7b8599'}},
        'bar': {'color': gauge_color, 'thickness': 0.25},
        'bgcolor': '#1e2738',
        'bordercolor': '#1e2738',
        'steps': [
            {'range': [0, 30],  'color': 'rgba(39,174,96,0.15)'},
            {'range': [30, 45], 'color': 'rgba(241,196,15,0.15)'},
            {'range': [45, 60], 'color': 'rgba(230,126,34,0.15)'},
            {'range': [60, 100],'color': 'rgba(192,57,43,0.15)'}
        ],
    }
))
fig_gauge.update_layout(
    height=200, paper_bgcolor='#161b27', plot_bgcolor='#161b27',
    margin=dict(l=20, r=20, t=50, b=10),
    font=dict(color='#7b8599')
)
st.plotly_chart(fig_gauge, use_container_width=True)

def indicator_row(label, val, nat, higher_is_bad=True):
    diff = val - nat
    if higher_is_bad:
        arrow, color = ("↑", "#e74c3c") if diff > 0 else ("↓", "#27ae60")
    else:
        arrow, color = ("↑", "#27ae60") if diff > 0 else ("↓", "#e74c3c")
    return f"""
    <div style='display:flex; justify-content:space-between;
                padding:0.35rem 0; border-bottom:1px solid #1e2738;
                font-size:0.88rem;'>
        <span style='color:#a0aabe;'>{label}</span>
        <span style='color:#e8eaf0; font-weight:600;'>
            {val:.1f}%
            <span style='color:{color}; font-size:0.76rem; margin-left:4px;'>
                {arrow}{abs(diff):.1f}
            </span>
        </span>
    </div>"""

# indicators
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("<div class='section-header'>🏥 Health Indicators</div>",
                unsafe_allow_html=True)
    rows_html = ""
    for label, col_key in [
        ("Anaemia (Women)", "anaemia_w"),
        ("Blood Sugar (Women)", "blood_sugar_w"),
        ("Blood Sugar (Men)", "blood_sugar_m"),
        ("BP Elevated (Women)", "bp_elevated_w"),
        ("BP Elevated (Men)", "bp_elevated_m"),
        ("Tobacco (Women)", "tobacco_w"),
        ("Tobacco (Men)", "tobacco_m"),
        ("Alcohol (Women)", "alcohol_w"),
        ("Alcohol (Men)", "alcohol_m"),
    ]:
        rows_html += indicator_row(label, row[col_key], national[col_key], higher_is_bad=True)
    st.markdown(rows_html, unsafe_allow_html=True)

with col2:
    st.markdown("<div class='section-header'>🌱 Social Determinants</div>",
                unsafe_allow_html=True)
    sdoh_html = ""
    for label, col_key in [
        ("Female Literacy", "literacy_w"),
        ("Health Insurance", "health_insurance"),
        ("Clean Water", "clean_water"),
        ("Sanitation", "sanitation"),
        ("Clean Fuel", "clean_fuel"),
    ]:
        sdoh_html += indicator_row(label, row[col_key], national[col_key], higher_is_bad=False)
    st.markdown(sdoh_html, unsafe_allow_html=True)

with col3:
    st.markdown("<div class='section-header'>🔬 Cancer Screening</div>",
                unsafe_allow_html=True)
    cancer_html = ""
    for label, col_key in [
        ("Cervical", "cervical_screening_w"),
        ("Breast", "breast_exam_w"),
        ("Oral", "oral_exam_w"),
    ]:
        val = row[col_key]
        nat = national[col_key]
        diff = val - nat
        arrow = "↑" if diff > 0 else "↓"
        color = "#27ae60" if diff > 0 else "#e74c3c"
        cancer_html += f"""
        <div style='display:flex; justify-content:space-between;
                    padding:0.35rem 0; border-bottom:1px solid #1e2738;
                    font-size:0.88rem;'>
            <span style='color:#a0aabe;'>{label}</span>
            <span style='color:#e8eaf0; font-weight:600;'>
                {val:.2f}%
                <span style='color:{color}; font-size:0.76rem; margin-left:4px;'>
                    {arrow}{abs(diff):.2f}
                </span>
            </span>
        </div>"""
    st.markdown(cancer_html, unsafe_allow_html=True)

insight_box(
    "Arrows show deviation from <strong>national average</strong>. "
    "↑ red = worse than national, ↓ green = better than national (for risk indicators). "
    "Reverse for protective indicators like literacy and clean fuel."
)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown("<div class='section-header'>📊 District vs State vs National Comparison</div>",
            unsafe_allow_html=True)

compare_cols   = ['anaemia_w', 'blood_sugar_w', 'bp_elevated_w',
                  'literacy_w', 'clean_fuel', 'risk_score']
compare_labels = ['Anaemia (W)', 'Blood Sugar (W)', 'BP Elevated (W)',
                  'Literacy (W)', 'Clean Fuel', 'Risk Score']

fig_c = go.Figure()
fig_c.add_trace(go.Bar(
    name='National Avg', x=compare_labels,
    y=[round(national[c], 1) for c in compare_cols],
    marker_color='#3498db', opacity=0.8
))
fig_c.add_trace(go.Bar(
    name=f'{selected_state} Avg', x=compare_labels,
    y=[round(state_avg[c], 1) for c in compare_cols],
    marker_color='#e67e22', opacity=0.8
))
fig_c.add_trace(go.Bar(
    name=selected_district, x=compare_labels,
    y=[round(row[c], 1) for c in compare_cols],
    marker_color='#c0392b', opacity=0.9
))
fig_c = plotly_layout(fig_c, height=400)
fig_c.update_layout(barmode='group', legend=dict(orientation='h', y=1.05),
                    showlegend=True, title_text="")
st.plotly_chart(fig_c, use_container_width=True)

footer()