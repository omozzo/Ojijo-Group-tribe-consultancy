import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ────────────────────────────────────────────────
# Page Config
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="TRIBE Hotel | Employment & Labour BI Dashboard",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ────────────────────────────────────────────────
# Custom CSS – Black / Gold / White Theme
# ────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

    /* Main background */
    .stApp {
        background-color: #0a0a0a;
        color: #f8f8f8;
        font-family: 'Inter', sans-serif;
    }

    /* Hide default Streamlit elements */
    #MainMenu, footer, header {visibility: hidden;}

    /* Headers */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #d4af37 !important;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-left: 4px solid #d4af37;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
    }
    [data-testid="stMetricLabel"] {
        color: #a0a0a0 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    [data-testid="stMetricValue"] {
        color: #f8f8f8 !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricDelta"] {
        color: #f0d875 !important;
    }

    /* Dataframes */
    .stDataFrame {
        background-color: #1a1a1a;
        border-radius: 12px;
        border: 1px solid #2a2a2a;
    }

    /* Section dividers */
    hr {
        border-color: #2a2a2a !important;
        margin: 2rem 0;
    }

    /* Roadmap cards */
    .roadmap-card {
        background-color: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 10px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: flex-start;
        gap: 1rem;
    }
    .step-num {
        background: #d4af37;
        color: #0a0a0a;
        font-weight: 700;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.85rem;
        flex-shrink: 0;
    }
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# Header
# ────────────────────────────────────────────────
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center; 
            border-bottom:2px solid #d4af37; padding-bottom:1rem; margin-bottom:2rem;">
    <div>
        <span style="font-family:'Playfair Display',serif; font-size:2rem; font-weight:700; color:#d4af37;">
            TRIBE
        </span>
        <span style="font-size:0.95rem; color:#f8f8f8; letter-spacing:1px; margin-left:8px;">
            HOTEL COLLECTION
        </span>
    </div>
    <div style="background:#d4af37; color:#0a0a0a; font-size:0.7rem; font-weight:700; 
                padding:0.4rem 1rem; border-radius:20px; letter-spacing:1px; text-transform:uppercase;">
        Board Confidential · Employment & Labour Review
    </div>
</div>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# KPI Row
# ────────────────────────────────────────────────
st.subheader("Key Headcount Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Current Total Roster",
        value="659",
        delta="All facilities + Corporate",
        delta_color="off"
    )

with col2:
    st.metric(
        label="Industry Benchmark",
        value="393",
        delta="-40% vs current",
        delta_color="inverse"
    )

with col3:
    st.metric(
        label="Management Proposal",
        value="489",
        delta="Target lean model",
        delta_color="off"
    )

with col4:
    st.metric(
        label="Potential Reduction",
        value="170",
        delta="vs current roster",
        delta_color="inverse"
    )

st.markdown("---")

# ────────────────────────────────────────────────
# Charts Section
# ────────────────────────────────────────────────
st.subheader("Manpower Rationalization")

col_chart1, col_chart2 = st.columns(2)

# Data
facilities = ["Tribe", "Trademark", "Restaurants"]
current = [215, 288, 156]
industry = [129, 108, 156]
proposal = [156, 192, 141]

with col_chart1:
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        name="Current Staff",
        x=facilities,
        y=current,
        marker_color="rgba(248,248,248,0.85)",
        marker_line_width=0
    ))
    fig1.add_trace(go.Bar(
        name="Industry Std",
        x=facilities,
        y=industry,
        marker_color="rgba(160,160,160,0.7)",
        marker_line_width=0
    ))
    fig1.add_trace(go.Bar(
        name="Mgmt Proposal",
        x=facilities,
        y=proposal,
        marker_color="rgba(212,175,55,0.9)",
        marker_line_width=0
    ))
    fig1.update_layout(
        barmode="group",
        title=dict(text="Staff by Facility – Current vs Industry vs Proposal", font=dict(color="#d4af37", size=14)),
        paper_bgcolor="#1a1a1a",
        plot_bgcolor="#1a1a1a",
        font=dict(color="#f8f8f8"),
        legend=dict(font=dict(color="#f8f8f8")),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#a0a0a0")),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#a0a0a0"), title="Headcount"),
        margin=dict(t=50, b=40, l=40, r=20),
        height=380
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_chart2:
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        name="Industry Std (staff per room)",
        x=["Tribe (129 rooms)", "Trademark (215 rooms)"],
        y=[1.0, 0.5],
        marker_color="rgba(160,160,160,0.7)"
    ))
    fig2.add_trace(go.Bar(
        name="Current Ratio",
        x=["Tribe (129 rooms)", "Trademark (215 rooms)"],
        y=[1.7, 1.3],
        marker_color="rgba(212,175,55,0.9)"
    ))
    fig2.update_layout(
        barmode="group",
        title=dict(text="Staff-to-Room Ratios", font=dict(color="#d4af37", size=14)),
        paper_bgcolor="#1a1a1a",
        plot_bgcolor="#1a1a1a",
        font=dict(color="#f8f8f8"),
        legend=dict(font=dict(color="#f8f8f8")),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#a0a0a0")),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#a0a0a0"), title="Staff per Room"),
        margin=dict(t=50, b=40, l=40, r=20),
        height=380
    )
    st.plotly_chart(fig2, use_container_width=True)

# ────────────────────────────────────────────────
# Staff Numbers Table
# ────────────────────────────────────────────────
st.subheader("Detailed Headcount Comparison")

staff_df = pd.DataFrame({
    "Facility": ["Tribe", "Trademark", "Restaurants", "Total Roster"],
    "Current Staff": [215, 288, 156, 659],
    "Industry Std": [129, 108, 156, 393],
    "Mgmt Proposal": [156, 192, 141, 489],
    "Gap to Proposal": [-59, -96, -15, -170]
})

st.dataframe(
    staff_df.style
        .format({"Current Staff": "{:,}", "Industry Std": "{:,}", "Mgmt Proposal": "{:,}", "Gap to Proposal": "{:+,}"})
        .applymap(lambda x: "color: #d4af37; font-weight:600" if isinstance(x, (int, float)) and x in [156, 192, 141, 489] else "")
        .applymap(lambda x: "color: #f87171" if isinstance(x, (int, float)) and x < 0 else ""),
    use_container_width=True,
    hide_index=True
)

# ────────────────────────────────────────────────
# Ratios Table
# ────────────────────────────────────────────────
st.subheader("Staff-to-Room Ratios")

ratio_df = pd.DataFrame({
    "Facility": ["Tribe", "Trademark"],
    "No. of Rooms": [129, 215],
    "Industry Std Ratio": ["1 : 1", "1 : 0.5"],
    "Current Ratio": ["1 : 1.7", "1 : 1.3"]
})

st.dataframe(ratio_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ────────────────────────────────────────────────
# Wage Schedules
# ────────────────────────────────────────────────
st.subheader("Current Wage Schedules (CBA)")

wage_df = pd.DataFrame({
    "Grade": [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "01/01/2025": [18853.84, 19268.14, 20362.34, 25447.29, 32003.70, 34566.00, 42544.04, 43026.81, 44747.75],
    "01/01/2026": [19985.07, 20424.23, 21584.08, 26974.13, 33923.92, 36639.96, 45096.69, 45608.42, 47432.62],
    "01/01/2027": [20984.32, 21445.44, 22663.28, 28322.84, 35620.12, 38471.95, 47351.52, 47888.84, 49804.25],
    "01/01/2028": [22033.54, 22517.71, 23796.44, 29738.98, 37401.12, 40395.55, 49719.10, 50283.28, 52294.46]
})

st.dataframe(
    wage_df.style.format({
        "01/01/2025": "{:,.2f}",
        "01/01/2026": "{:,.2f}",
        "01/01/2027": "{:,.2f}",
        "01/01/2028": "{:,.2f}"
    }),
    use_container_width=True,
    hide_index=True
)

# ────────────────────────────────────────────────
# Housing Allowance
# ────────────────────────────────────────────────
st.subheader("Monthly House Allowance")

housing_df = pd.DataFrame({
    "Grade Band": ["Grade 1–3", "Grade 4–5", "Grade 6–9"],
    "01/01/2025": [13384.24, 13674.32, 13999.35],
    "01/01/2026": [14454.98, 14768.27, 15119.30],
    "01/01/2027": [15466.83, 15802.04, 16177.65],
    "01/01/2028": [16549.50, 16908.19, 17310.08]
})

st.dataframe(
    housing_df.style.format({
        "01/01/2025": "{:,.2f}",
        "01/01/2026": "{:,.2f}",
        "01/01/2027": "{:,.2f}",
        "01/01/2028": "{:,.2f}"
    }),
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ────────────────────────────────────────────────
# Implementation Roadmap
# ────────────────────────────────────────────────
st.subheader("Proposed Implementation Roadmap")

roadmap_items = [
    "Give the union <strong>90 days’ notice</strong> of proposed amendments",
    "Negotiate on behalf of the Association with <strong>KUDHEIHA</strong>",
    "Register the agreed negotiations once concluded",
    "Process any redundancy in line with Separation & Placement Agreement",
    "Draft new/updated internal policies reflecting agreed changes",
    "Draft new service-provider agreements (outsourcing + service charge)",
    "Conduct full HR Audit",
    "Participate in Union / Management negotiations as required"
]

# Display in two columns
col_r1, col_r2 = st.columns(2)

for i, item in enumerate(roadmap_items):
    target_col = col_r1 if i < 4 else col_r2
    with target_col:
        st.markdown(f"""
        <div class="roadmap-card">
            <div class="step-num">{i+1}</div>
            <div style="color:#f8f8f8; font-size:0.92rem;">{item}</div>
        </div>
        """, unsafe_allow_html=True)

# ────────────────────────────────────────────────
# Footer
# ────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:2rem 0 1rem; color:#a0a0a0; font-size:0.8rem; 
            border-top:1px solid #2a2a2a; margin-top:3rem;">
    TRIBE HOTEL | BOARD CONFIDENTIAL · Employment and Labour Relations Review · 
    <span style="color:#d4af37;">Prepared for Board Presentation</span>
</div>
""", unsafe_allow_html=True)
