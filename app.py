
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Tribe Hotel | Board BI Dashboard",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ────────────────────────────────────────────────
# Custom CSS – Black / Gold / White Theme
# ────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

    .stApp {
        background-color: #0a0a0a;
        color: #f8f8f8;
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3, h4 {
        font-family: 'Playfair Display', serif !important;
        color: #d4af37 !important;
    }

    [data-testid="stMetric"] {
        background-color: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-left: 4px solid #d4af37;
        border-radius: 10px;
        padding: 12px 16px;
    }
    [data-testid="stMetricLabel"] {
        color: #a0a0a0 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    [data-testid="stMetricValue"] {
        color: #f8f8f8 !important;
        font-weight: 700 !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1a1a;
        border-radius: 8px 8px 0 0;
        color: #a0a0a0;
        border: 1px solid #2a2a2a;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f1a00 !important;
        color: #d4af37 !important;
        border-bottom: 2px solid #d4af37;
    }

    div[data-testid="stDataFrame"] {
        background-color: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 10px;
    }

    .stSidebar {
        background-color: #121212;
    }
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# Header
# ────────────────────────────────────────────────
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center; 
            border-bottom:2px solid #d4af37; padding-bottom:12px; margin-bottom:20px;">
    <div>
        <span style="font-family:'Playfair Display',serif; font-size:1.9rem; font-weight:700; color:#d4af37;">TRIBE</span>
        <span style="font-size:0.95rem; color:#f8f8f8; margin-left:8px; letter-spacing:1px;">HOTEL COLLECTION</span>
    </div>
    <div style="background:#d4af37; color:#0a0a0a; font-size:0.7rem; font-weight:700; 
                padding:6px 14px; border-radius:20px; letter-spacing:0.8px;">
        BOARD CONFIDENTIAL · EMPLOYMENT & LABOUR REVIEW
    </div>
</div>
""", unsafe_allow_html=True)

st.caption("Decision-support dashboard based on the Tribe Hotel Board Presentation. Financial and workforce inputs are editable assumptions.")

# ────────────────────────────────────────────────
# Sidebar Inputs
# ────────────────────────────────────────────────
st.sidebar.header("Board Inputs")

employees = st.sidebar.number_input("Total employees", min_value=0, value=659, step=1)
monthly_payroll = st.sidebar.number_input("Monthly payroll (KES)", min_value=0.0, value=25_000_000.0, step=100_000.0)
monthly_revenue = st.sidebar.number_input("Monthly revenue (KES)", min_value=0.0, value=80_000_000.0, step=100_000.0)
monthly_service_charge = st.sidebar.number_input("Monthly service charge pool (KES)", min_value=0.0, value=5_000_000.0, step=100_000.0)
outsourced_monthly_cost = st.sidebar.number_input("Current monthly cost of functions proposed for outsourcing (KES)", min_value=0.0, value=3_000_000.0, step=100_000.0)
outsourced_provider_cost = st.sidebar.number_input("Estimated outsourced provider monthly cost (KES)", min_value=0.0, value=2_400_000.0, step=100_000.0)

st.sidebar.subheader("Salary / CBA")
entry_current = st.sidebar.number_input("Entry-level current increment %", min_value=0.0, value=5.0, step=0.5)
general_current = st.sidebar.number_input("General-wage current increment %", min_value=0.0, value=7.0, step=0.5)
entry_proposed = st.sidebar.number_input("Entry-level proposed increment %", min_value=0.0, value=2.5, step=0.5)
general_proposed = st.sidebar.number_input("General-wage proposed increment %", min_value=0.0, value=3.5, step=0.5)

st.sidebar.subheader("Service Charge")
org_share = st.sidebar.number_input("Organization share %", min_value=0.0, max_value=100.0, value=20.0, step=1.0)
mgmt_share = st.sidebar.number_input("Management share %", min_value=0.0, max_value=100.0, value=5.0, step=1.0)
employee_share = 100.0 - org_share - mgmt_share

# ────────────────────────────────────────────────
# Calculations
# ────────────────────────────────────────────────
payroll_ratio = (monthly_payroll / monthly_revenue * 100) if monthly_revenue else 0
outsourcing_saving = max(0, outsourced_monthly_cost - outsourced_provider_cost)
annual_outsourcing_saving = outsourcing_saving * 12
entry_delta = entry_current - entry_proposed
general_delta = general_current - general_proposed
employee_service_charge = monthly_service_charge * employee_share / 100
org_service_charge = monthly_service_charge * org_share / 100
mgmt_service_charge = monthly_service_charge * mgmt_share / 100

# ────────────────────────────────────────────────
# Tabs
# ────────────────────────────────────────────────
tabs = st.tabs([
    "Executive Dashboard", "Manpower", "CBA & Salary", "Service Charge",
    "Outsourcing", "Legal Risk", "Roadmap", "Data Export"
])

# ==================== TAB 0: Executive ====================
with tabs[0]:
    st.subheader("Executive Board Dashboard")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Employees", f"{employees:,}")
    c2.metric("Labour Cost / Revenue", f"{payroll_ratio:.1f}%")
    c3.metric("Annual Outsourcing Saving", f"KES {annual_outsourcing_saving:,.0f}")
    c4.metric("Employee Service Charge", f"KES {employee_service_charge:,.0f}")

    st.markdown("### Strategic Decision Signals")
    signals = pd.DataFrame({
        "Area": ["CBA / Salary", "Service Charge", "Outsourcing", "Manpower"],
        "Current / Baseline": [
            f"{entry_current:.1f}% entry · {general_current:.1f}% general",
            f"{org_share:.0f}% org / {mgmt_share:.0f}% mgmt / {employee_share:.0f}% employees",
            f"KES {outsourced_monthly_cost:,.0f} monthly",
            f"{employees:,} employees (report baseline 659)"
        ],
        "Proposed / Target": [
            f"{entry_proposed:.1f}% entry · {general_proposed:.1f}% general",
            "20% organization / 5% management / 75% employees",
            f"KES {outsourced_provider_cost:,.0f} monthly",
            "Evidence-based rationalization · non-compulsory routes first"
        ]
    })
    st.dataframe(signals, use_container_width=True, hide_index=True)

    st.info("Source position: proposed changes should proceed through appropriate legal, contractual and consultative processes rather than unilateral variation.")

# ==================== TAB 1: Manpower (ENHANCED) ====================
with tabs[1]:
    st.subheader("Manpower Rationalization")

    # Real data from the report
    staff_df = pd.DataFrame({
        "Facility": ["Tribe", "Trademark", "Restaurants", "Total Roster"],
        "Current Staff": [215, 288, 156, 659],
        "Industry Std": [129, 108, 156, 393],
        "Mgmt Proposal": [156, 192, 141, 489],
        "Gap to Proposal": [-59, -96, -15, -170]
    })

    st.markdown("#### Headcount by Facility (from Board Report)")
    st.dataframe(staff_df, use_container_width=True, hide_index=True)

    # Chart
    fig_staff = go.Figure()
    fig_staff.add_trace(go.Bar(name="Current", x=["Tribe", "Trademark", "Restaurants"], y=[215, 288, 156],
                               marker_color="rgba(248,248,248,0.85)"))
    fig_staff.add_trace(go.Bar(name="Industry Std", x=["Tribe", "Trademark", "Restaurants"], y=[129, 108, 156],
                               marker_color="rgba(160,160,160,0.7)"))
    fig_staff.add_trace(go.Bar(name="Mgmt Proposal", x=["Tribe", "Trademark", "Restaurants"], y=[156, 192, 141],
                               marker_color="rgba(212,175,55,0.9)"))
    fig_staff.update_layout(
        barmode="group",
        title="Staff by Facility – Current vs Industry vs Proposal",
        paper_bgcolor="#1a1a1a",
        plot_bgcolor="#1a1a1a",
        font=dict(color="#f8f8f8"),
        height=380
    )
    st.plotly_chart(fig_staff, use_container_width=True)

    # Ratios
    st.markdown("#### Staff-to-Room Ratios")
    ratio_df = pd.DataFrame({
        "Facility": ["Tribe", "Trademark"],
        "No. of Rooms": [129, 215],
        "Industry Std Ratio": ["1 : 1", "1 : 0.5"],
        "Current Ratio": ["1 : 1.7", "1 : 1.3"]
    })
    st.dataframe(ratio_df, use_container_width=True, hide_index=True)

    st.warning("The source report prioritizes natural attrition, voluntary separation schemes, early retirement or mutually agreed exits before any compulsory redundancy.")

# ==================== TAB 2: CBA & Salary ====================
with tabs[2]:
    st.subheader("CBA & Salary Analytics")

    col1, col2 = st.columns(2)
    salary_df = pd.DataFrame({
        "Category": ["Entry level", "General wages"],
        "Current %": [entry_current, general_current],
        "Proposed %": [entry_proposed, general_proposed]
    })
    with col1:
        fig = px.bar(salary_df, x="Category", y=["Current %", "Proposed %"], barmode="group",
                     title="Current vs Proposed Salary Review Percentages",
                     color_discrete_sequence=["#a0a0a0", "#d4af37"])
        fig.update_layout(paper_bgcolor="#1a1a1a", plot_bgcolor="#1a1a1a", font=dict(color="#f8f8f8"))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.metric("Entry-level reduction", f"{entry_delta:.1f} percentage points")
        st.metric("General-wage reduction", f"{general_delta:.1f} percentage points")
        st.dataframe(salary_df, use_container_width=True, hide_index=True)

    st.markdown("#### Current Wage Schedules (from CBA)")
    wage_df = pd.DataFrame({
        "Grade": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "01/01/2025": [18853.84, 19268.14, 20362.34, 25447.29, 32003.70, 34566.00, 42544.04, 43026.81, 44747.75],
        "01/01/2026": [19985.07, 20424.23, 21584.08, 26974.13, 33923.92, 36639.96, 45096.69, 45608.42, 47432.62],
        "01/01/2027": [20984.32, 21445.44, 22663.28, 28322.84, 35620.12, 38471.95, 47351.52, 47888.84, 49804.25],
        "01/01/2028": [22033.54, 22517.71, 23796.44, 29738.98, 37401.12, 40395.55, 49719.10, 50283.28, 52294.46]
    })
    st.dataframe(wage_df.style.format("{:,.2f}", subset=["01/01/2025", "01/01/2026", "01/01/2027", "01/01/2028"]),
                 use_container_width=True, hide_index=True)

    st.markdown("#### Monthly House Allowance")
    housing_df = pd.DataFrame({
        "Grade Band": ["Grade 1–3", "Grade 4–5", "Grade 6–9"],
        "01/01/2025": [13384.24, 13674.32, 13999.35],
        "01/01/2026": [14454.98, 14768.27, 15119.30],
        "01/01/2027": [15466.83, 15802.04, 16177.65],
        "01/01/2028": [16549.50, 16908.19, 17310.08]
    })
    st.dataframe(housing_df.style.format("{:,.2f}", subset=["01/01/2025", "01/01/2026", "01/01/2027", "01/01/2028"]),
                 use_container_width=True, hide_index=True)

    st.info("Any deferral of 2027/2028 increments is a variation of an existing wage term and must follow a consultative process under Section 10(5) of the Employment Act.")

# ==================== TAB 3: Service Charge ====================
with tabs[3]:
    st.subheader("Service Charge Analytics")
    shares = pd.DataFrame({
        "Recipient": ["Organization", "Management", "Employees"],
        "Share %": [org_share, mgmt_share, employee_share],
        "Monthly KES": [org_service_charge, mgmt_service_charge, employee_service_charge]
    })
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(shares, names="Recipient", values="Share %", title="Service Charge Distribution",
                     color_discrete_sequence=["#d4af37", "#a0a0a0", "#f8f8f8"])
        fig.update_layout(paper_bgcolor="#1a1a1a", font=dict(color="#f8f8f8"))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.dataframe(shares, use_container_width=True, hide_index=True)
        st.metric("Total pool", f"KES {monthly_service_charge:,.0f}")

    st.caption("Source report proposal: 20% retained by the organization, 5% to management, remainder to employees.")

# ==================== TAB 4: Outsourcing ====================
with tabs[4]:
    st.subheader("Outsourcing Business Case")
    funcs = st.multiselect(
        "Functions identified in the report",
        ["Laundry", "Cleaning of common areas", "Security"],
        default=["Laundry"]
    )
    col1, col2, col3 = st.columns(3)
    col1.metric("Current monthly cost", f"KES {outsourced_monthly_cost:,.0f}")
    col2.metric("Estimated provider cost", f"KES {outsourced_provider_cost:,.0f}")
    col3.metric("Monthly saving", f"KES {outsourcing_saving:,.0f}")
    st.metric("Projected annual saving", f"KES {annual_outsourcing_saving:,.0f}")

    risk = pd.DataFrame({
        "Risk": [
            "Re-characterization as continuing employment",
            "Unfair labour practice / unlawful transfer",
            "Discriminatory outsourcing",
            "Union / CBA challenge"
        ],
        "Mitigation": [
            "Engage a genuinely independent contractor with own management, systems and capital",
            "Obtain express employee acceptance and settle accrued obligations before transfer",
            "Apply the outsourcing decision consistently across comparable roles and document the rationale",
            "Prior consultation with the union and negotiate any necessary CBA amendment"
        ]
    })
    st.dataframe(risk, use_container_width=True, hide_index=True)

# ==================== TAB 5: Legal Risk ====================
with tabs[5]:
    st.subheader("Legal & Industrial Relations Risk Matrix")
    risk_df = pd.DataFrame({
        "Issue": [
            "Unilateral change to CBA / employment terms",
            "Outsourcing without employee acceptance",
            "Discriminatory outsourcing",
            "Service charge changed without consultation",
            "Misclassification of management employees",
            "Fixed-term contracts used to circumvent CBA"
        ],
        "Probability": ["High", "High", "Medium", "Medium", "Medium", "Medium"],
        "Impact": ["High", "High", "High", "High", "High", "High"],
        "Priority Score": [9, 9, 6, 6, 6, 6],
        "Primary Mitigation": [
            "Consult, negotiate, document and register agreed changes",
            "Settle obligations and obtain express acceptance",
            "Apply consistent criteria and document rationale",
            "Consult and amend contractual/CBA framework",
            "Functional job analysis; consult and document",
            "Use fixed-term model lawfully and avoid systematic circumvention"
        ]
    })
    st.dataframe(risk_df, use_container_width=True, hide_index=True)

# ==================== TAB 6: Roadmap ====================
with tabs[6]:
    st.subheader("Implementation Roadmap")
    roadmap = pd.DataFrame({
        "Step": [1, 2, 3, 4, 5, 6, 7, 8],
        "Action": [
            "Give the union 90 days’ notice of the proposed amendments",
            "Negotiate on behalf of the Association with KUDHEIHA",
            "Register the agreed negotiations once concluded",
            "Process any redundancy in line with the Separation and Placement Agreement",
            "Draft new/updated internal policies to reflect the agreed changes",
            "Draft new service-provider agreements (outsourcing + service charge)",
            "Conduct a full HR Audit",
            "Participate in discussions and negotiations involving the Union, employees and management"
        ],
        "Status": ["Not started"] * 8
    })
    edited = st.data_editor(
        roadmap,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Status": st.column_config.SelectboxColumn(
                options=["Not started", "In progress", "Complete", "At risk"]
            )
        }
    )
    completed = (edited["Status"] == "Complete").sum()
    progress = completed / len(edited) * 100
    st.progress(progress / 100, text=f"Roadmap completion: {progress:.0f}%")

# ==================== TAB 7: Data Export ====================
with tabs[7]:
    st.subheader("Board Data Export")
    export = pd.DataFrame({
        "Metric": [
            "Employees", "Monthly Payroll", "Monthly Revenue", "Labour Cost / Revenue %",
            "Monthly Service Charge Pool", "Organization Service Charge", "Management Service Charge",
            "Employee Service Charge", "Current Outsourcing Cost", "Provider Cost",
            "Annual Outsourcing Saving", "Entry Current %", "Entry Proposed %",
            "General Current %", "General Proposed %"
        ],
        "Value": [
            employees, monthly_payroll, monthly_revenue, payroll_ratio,
            monthly_service_charge, org_service_charge, mgmt_service_charge,
            employee_service_charge, outsourced_monthly_cost, outsourced_provider_cost,
            annual_outsourcing_saving, entry_current, entry_proposed,
            general_current, general_proposed
        ]
    })
    st.dataframe(export, use_container_width=True, hide_index=True)
    csv = export.to_csv(index=False).encode("utf-8")
    st.download_button("Download Board KPI CSV", csv, "tribe_hotel_board_kpis.csv", "text/csv")

st.divider()
st.caption("Prepared as a decision-support prototype from the Tribe Hotel Board Presentation. Legal conclusions should be verified against current law and official records before external use.")