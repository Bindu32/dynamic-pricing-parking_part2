import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from scipy import stats
import warnings
warnings.filterwarnings("ignore")

# ---------------------------------------
# Page configuration
# ---------------------------------------

st.set_page_config(
    page_title="Smart City Parking Pricing",
    layout="wide"
)

st.title("🚗 Smart City Dynamic Parking Pricing System")

st.markdown("""
This dashboard demonstrates **dynamic pricing optimization for urban parking systems**.

Prices adjust based on:

• Parking occupancy  
• Traffic conditions  
• Queue length  
• Competitor pricing  

The goal is to **optimize parking revenue and manage demand efficiently**.
""")

# ---------------------------------------
# Sidebar
# ---------------------------------------

st.sidebar.header("Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload parking dataset (CSV)",
    type=["csv"]
)

simulate = st.sidebar.checkbox(
    "Enable Real-Time Demand Simulation"
)

# ---------------------------------------
# Load dataset
# ---------------------------------------

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    # Generate synthetic dataset if no file uploaded
    np.random.seed(42)
    n = 300
    df = pd.DataFrame({
        "SystemCodeNumber": [f"LOT_{i:03d}" for i in range(n)],
        "Capacity": np.random.randint(20, 100, n),
        "Occupancy": np.random.randint(5, 90, n),
        "QueueLength": np.random.randint(0, 10, n),
        "TrafficConditionNearby": np.random.choice(["low", "medium", "high"], n),
        "LastUpdated": pd.date_range("2024-01-01", periods=n, freq="h")
    })
    df["Occupancy"] = df[["Occupancy", "Capacity"]].min(axis=1)

# ---------------------------------------
# Generate coordinates if not present
# ---------------------------------------

if "latitude" not in df.columns:
    np.random.seed(42)
    city_lat = 17.3850
    city_lon = 78.4867
    df["latitude"] = city_lat + np.random.normal(0, 0.01, len(df))
    df["longitude"] = city_lon + np.random.normal(0, 0.01, len(df))

# ---------------------------------------
# Pricing model
# ---------------------------------------

def dynamic_pricing(df):
    base_price = 10
    df["occupancy_rate"] = df["Occupancy"] / df["Capacity"]
    traffic_map = {"low": 1, "medium": 1.5, "high": 2}
    df["traffic_weight"] = df["TrafficConditionNearby"].map(traffic_map).fillna(1)
    df["dynamic_price"] = (
        base_price
        * (1 + 1.5 * df["occupancy_rate"])
        * (1 + 0.2 * df["traffic_weight"])
        * (1 + 0.1 * df["QueueLength"])
    )
    return df

# ---------------------------------------
# Real-time demand simulation
# ---------------------------------------

if simulate:
    df["Occupancy"] = df["Occupancy"] + np.random.randint(-2, 5, len(df))
    df["Occupancy"] = df["Occupancy"].clip(0, df["Capacity"])
    df["QueueLength"] = np.random.randint(0, 5, len(df))

# ---------------------------------------
# Run pricing model
# ---------------------------------------

df_result = dynamic_pricing(df.copy())

# ---------------------------------------
# KPI Metrics
# ---------------------------------------

st.subheader("📊 Pricing KPIs")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Occupancy",
    f"{df_result['occupancy_rate'].mean():.2f}"
)

col2.metric(
    "Average Dynamic Price",
    f"${df_result['dynamic_price'].mean():.2f}"
)

estimated_revenue = (
    df_result["dynamic_price"] * df_result["Occupancy"]
).sum()

col3.metric(
    "Estimated Revenue",
    f"${estimated_revenue:,.0f}"
)

# ---------------------------------------
# Pricing comparison chart
# ---------------------------------------

st.subheader("📈 Pricing Distribution")

fig = px.line(
    df_result,
    y="dynamic_price",
    title="Dynamic Pricing Across Parking Lots"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------
# Occupancy vs price analysis
# ---------------------------------------

st.subheader("📊 Occupancy Impact on Price")

fig2 = px.scatter(
    df_result,
    x="occupancy_rate",
    y="dynamic_price",
    title="Occupancy Rate vs Dynamic Price"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------
# Top revenue parking lots
# ---------------------------------------

st.subheader("🏆 Highest Revenue Parking Lots")

df_result["revenue"] = (
    df_result["dynamic_price"] * df_result["Occupancy"]
)

top_lots = df_result.sort_values(
    "revenue",
    ascending=False
).head(10)

st.dataframe(
    top_lots[
        [
            "SystemCodeNumber",
            "Occupancy",
            "Capacity",
            "dynamic_price",
            "revenue"
        ]
    ],
    use_container_width=True
)

# ---------------------------------------
# Parking Map
# ---------------------------------------

st.subheader("🗺 Parking Locations")

m = folium.Map(
    location=[
        df_result["latitude"].mean(),
        df_result["longitude"].mean()
    ],
    zoom_start=13
)

for _, row in df_result.head(200).iterrows():
    popup_text = f"""
    Parking Lot: {row['SystemCodeNumber']} <br>
    Occupancy: {row['Occupancy']}/{row['Capacity']} <br>
    Price: ${row['dynamic_price']:.2f}
    """
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=6,
        popup=popup_text,
        color="blue",
        fill=True
    ).add_to(m)

st_folium(m, width=900, height=500)

# ---------------------------------------
# Demand Heatmap
# ---------------------------------------

st.subheader("🔥 Parking Demand Heatmap")

heat_data = [
    [row["latitude"], row["longitude"], row["occupancy_rate"]]
    for _, row in df_result.iterrows()
]

m2 = folium.Map(
    location=[
        df_result["latitude"].mean(),
        df_result["longitude"].mean()
    ],
    zoom_start=13
)

HeatMap(heat_data).add_to(m2)

st_folium(m2, width=900, height=500)

# ---------------------------------------
# Dataset preview
# ---------------------------------------

st.subheader("📂 Dataset Preview")

st.dataframe(
    df_result.head(50),
    use_container_width=True
)

# ---------------------------------------
# Model explanation
# ---------------------------------------

st.subheader("⚙️ Pricing Model Logic")

st.markdown("""
Dynamic price is calculated using demand signals:

Dynamic Price =  
Base Price × Occupancy Impact × Traffic Factor × Queue Impact

Drivers:

• High occupancy increases price  
• Heavy traffic increases demand  
• Long queues signal higher demand  
• Pricing adapts dynamically to parking utilization  

This simulation demonstrates **data-driven pricing strategies for smart city parking systems**.
""")


# ================================================================
# ================================================================
# A/B TESTING + PRODUCT STRATEGY MODULE
# (Added below — original code above is untouched)
# ================================================================
# ================================================================

st.markdown("---")
st.markdown("# 🧪 A/B Testing & Product Strategy Module")
st.markdown("""
This module enables **experimentation-driven product decisions** — 
working across PM, Engineering, and Data roles to measure what truly moves the needle.
""")

# ================================================================
# TAB LAYOUT
# ================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔬 A/B Test Engine",
    "📌 Product KPIs",
    "👤 User Behavior",
    "🤝 PM + Eng Collaboration",
    "🎯 Decision Influence"
])


# ================================================================
# TAB 1: A/B TEST ENGINE
# ================================================================

with tab1:
    st.header("🔬 A/B Test Engine — Pricing Strategy Experiments")

    st.markdown("""
    Test two different pricing strategies head-to-head and use 
    statistical significance to decide which one wins.
    """)

    # ---- Experiment Configuration ----
    st.subheader("⚙️ Experiment Configuration")

    col1, col2, col3 = st.columns(3)
    with col1:
        test_name = st.text_input("Experiment Name", value="Dynamic vs Flat Pricing")
        split_pct = st.slider("Traffic Split (% to Variant B)", 10, 50, 50)
    with col2:
        confidence_level = st.selectbox("Confidence Level", [90, 95, 99], index=1)
        metric_choice = st.selectbox(
            "Primary Metric",
            ["Revenue per Lot", "Occupancy Rate", "Price per Slot", "Queue Reduction"]
        )
    with col3:
        st.markdown("**Variant A — Control**")
        st.caption("Current dynamic pricing model")
        st.markdown("**Variant B — Treatment**")
        variant_b_type = st.selectbox(
            "Pricing Strategy",
            ["Flat Rate ($15)", "Surge Only (>80% occ)", "Time-of-Day Tiered", "Competitor-Aware"]
        )

    # ---- Generate A/B Data ----
    np.random.seed(123)
    n_lots = len(df_result)
    n_b = int(n_lots * split_pct / 100)
    n_a = n_lots - n_b

    # Control A = existing dynamic pricing
    group_a = df_result.sample(n_a, random_state=1).copy()
    group_a["group"] = "A — Control (Dynamic)"
    group_a["test_price"] = group_a["dynamic_price"]
    group_a["test_revenue"] = group_a["test_price"] * group_a["Occupancy"]
    group_a["test_occupancy"] = group_a["occupancy_rate"]

    # Variant B = alternative strategy
    group_b = df_result.sample(n_b, random_state=2).copy()
    group_b["group"] = f"B — {variant_b_type}"

    if variant_b_type == "Flat Rate ($15)":
        group_b["test_price"] = 15.0
        group_b["test_occupancy"] = group_b["occupancy_rate"] * np.random.uniform(0.85, 1.05, n_b)
    elif variant_b_type == "Surge Only (>80% occ)":
        group_b["test_price"] = np.where(
            group_b["occupancy_rate"] > 0.8,
            group_b["dynamic_price"] * 1.3,
            10.0
        )
        group_b["test_occupancy"] = group_b["occupancy_rate"] * np.random.uniform(0.9, 1.1, n_b)
    elif variant_b_type == "Time-of-Day Tiered":
        group_b["test_price"] = group_b["dynamic_price"] * np.random.uniform(0.9, 1.2, n_b)
        group_b["test_occupancy"] = group_b["occupancy_rate"] * np.random.uniform(0.95, 1.05, n_b)
    else:  # Competitor-Aware
        group_b["test_price"] = group_b["dynamic_price"] * np.random.uniform(0.85, 1.15, n_b)
        group_b["test_occupancy"] = group_b["occupancy_rate"] * np.random.uniform(0.92, 1.08, n_b)

    group_b["test_occupancy"] = group_b["test_occupancy"].clip(0, 1)
    group_b["test_revenue"] = group_b["test_price"] * group_b["Occupancy"]

    ab_data = pd.concat([group_a, group_b], ignore_index=True)

    # ---- Statistical Test ----
    alpha = 1 - confidence_level / 100

    if metric_choice == "Revenue per Lot":
        metric_col = "test_revenue"
    elif metric_choice == "Occupancy Rate":
        metric_col = "test_occupancy"
    elif metric_choice == "Price per Slot":
        metric_col = "test_price"
    else:
        metric_col = "QueueLength"

    a_vals = group_a[metric_col].dropna()
    b_vals = group_b[metric_col].dropna()

    t_stat, p_value = stats.ttest_ind(a_vals, b_vals)
    significant = p_value < alpha
    lift = ((b_vals.mean() - a_vals.mean()) / a_vals.mean()) * 100

    # ---- Results Summary ----
    st.subheader("📊 Experiment Results")

    r1, r2, r3, r4, r5 = st.columns(5)
    r1.metric("Control (A) Mean", f"{a_vals.mean():.2f}")
    r2.metric("Variant (B) Mean", f"{b_vals.mean():.2f}")
    r3.metric("Lift", f"{lift:+.1f}%", delta=f"{lift:+.1f}%")
    r4.metric("p-value", f"{p_value:.4f}")
    r5.metric(
        "Significant?",
        "✅ YES" if significant else "❌ NO",
        delta="Reject H₀" if significant else "Fail to reject H₀"
    )

    # ---- Decision Banner ----
    if significant and lift > 0:
        st.success(f"🏆 **SHIP IT** — Variant B ({variant_b_type}) wins with {lift:+.1f}% lift at {confidence_level}% confidence. Recommend full rollout.")
    elif significant and lift < 0:
        st.error(f"🚫 **DO NOT SHIP** — Variant B hurts {metric_choice} by {lift:.1f}%. Keep Control A.")
    else:
        st.warning(f"⏳ **INCONCLUSIVE** — No statistically significant difference detected (p={p_value:.4f}). Extend the experiment or increase sample size.")

    # ---- Distribution Chart ----
    st.subheader("📈 Metric Distribution — A vs B")

    fig_ab = go.Figure()
    fig_ab.add_trace(go.Histogram(
        x=a_vals, name="A — Control",
        opacity=0.65, marker_color="#3B82F6", nbinsx=30
    ))
    fig_ab.add_trace(go.Histogram(
        x=b_vals, name=f"B — {variant_b_type}",
        opacity=0.65, marker_color="#F59E0B", nbinsx=30
    ))
    fig_ab.update_layout(
        barmode="overlay",
        title=f"{metric_choice} Distribution — A vs B",
        xaxis_title=metric_choice,
        yaxis_title="Count",
        legend=dict(x=0.75, y=0.95)
    )
    st.plotly_chart(fig_ab, use_container_width=True)

    # ---- Box Plot ----
    fig_box = px.box(
        ab_data,
        x="group",
        y=metric_col,
        color="group",
        title=f"{metric_choice} — Variant Comparison Box Plot",
        color_discrete_sequence=["#3B82F6", "#F59E0B"]
    )
    st.plotly_chart(fig_box, use_container_width=True)

    # ---- Statistical Summary Table ----
    st.subheader("📋 Statistical Summary")
    stat_summary = pd.DataFrame({
        "Group": ["A — Control", f"B — {variant_b_type}"],
        "N": [len(a_vals), len(b_vals)],
        "Mean": [a_vals.mean(), b_vals.mean()],
        "Std Dev": [a_vals.std(), b_vals.std()],
        "Min": [a_vals.min(), b_vals.min()],
        "Max": [a_vals.max(), b_vals.max()],
        "95% CI Lower": [
            a_vals.mean() - 1.96 * a_vals.std() / np.sqrt(len(a_vals)),
            b_vals.mean() - 1.96 * b_vals.std() / np.sqrt(len(b_vals))
        ],
        "95% CI Upper": [
            a_vals.mean() + 1.96 * a_vals.std() / np.sqrt(len(a_vals)),
            b_vals.mean() + 1.96 * b_vals.std() / np.sqrt(len(b_vals))
        ]
    }).round(3)
    st.dataframe(stat_summary, use_container_width=True)

    # ---- Sample Size Calculator ----
    st.subheader("🧮 Sample Size Calculator")
    st.markdown("Estimate how many parking lots you need for a reliable experiment.")

    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        mde = st.slider("Minimum Detectable Effect (%)", 1, 30, 5)
    with sc2:
        power = st.slider("Statistical Power (%)", 70, 95, 80)
    with sc3:
        baseline_std = st.number_input(
            "Baseline Std Dev",
            value=float(a_vals.std()),
            step=0.5
        )

    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power / 100)
    effect_size = (mde / 100) * a_vals.mean()
    required_n = int(2 * ((z_alpha + z_beta) ** 2 * baseline_std ** 2) / (effect_size ** 2)) + 1

    st.info(f"📐 **Required sample size per group: {required_n} parking lots** — "
            f"to detect a {mde}% change with {power}% power at {confidence_level}% confidence.")


# ================================================================
# TAB 2: PRODUCT KPIs
# ================================================================

with tab2:
    st.header("📌 Product KPIs — Beyond the Dashboard")
    st.markdown("""
    Product KPIs are **outcome metrics**, not output metrics. 
    They connect pricing decisions to real business and user impact.
    """)

    # ---- KPI Framework ----
    st.subheader("🎯 KPI Framework — North Star → Input Metrics")

    kpi_data = {
        "Level": ["North Star", "North Star",
                  "L1 — Revenue", "L1 — Revenue", "L1 — Revenue",
                  "L2 — Demand", "L2 — Demand", "L2 — Demand",
                  "L3 — Experience", "L3 — Experience"],
        "KPI": [
            "Revenue per Available Slot (RevPAS)",
            "Parking Utilization Rate",
            "Dynamic Pricing Lift vs Flat",
            "Price Elasticity Index",
            "Revenue per Occupied Hour",
            "Peak Hour Fill Rate",
            "Queue Abandonment Rate",
            "Demand Forecast Accuracy",
            "Driver Wait Time (avg)",
            "Re-visit Rate (30 days)"
        ],
        "Owner": [
            "PM + Finance", "PM + Ops",
            "Data Science", "Analytics", "Finance",
            "Ops + Engineering", "Product", "ML Team",
            "UX + Ops", "Product"
        ],
        "Target": [
            "> $18", "> 75%",
            "> +12%", "< 0.8", "> $22",
            "> 90%", "< 5%", "> 85%",
            "< 3 min", "> 40%"
        ],
        "Current": [
            f"${df_result['dynamic_price'].mean():.2f}",
            f"{df_result['occupancy_rate'].mean():.1%}",
            "+8.3%", "0.72", "$24.10",
            "83%", "7.2%", "79%",
            "4.1 min", "33%"
        ],
        "Status": [
            "🟡 At Risk", "🟢 On Track",
            "🔴 Off Target", "🟢 On Track", "🟢 On Track",
            "🟡 At Risk", "🔴 Off Target", "🟡 At Risk",
            "🔴 Off Target", "🟡 At Risk"
        ]
    }

    kpi_df = pd.DataFrame(kpi_data)
    st.dataframe(kpi_df, use_container_width=True, height=380)

    # ---- KPI Trend Simulation ----
    st.subheader("📈 KPI Trends Over Time (Last 30 Days)")

    days = pd.date_range(end=pd.Timestamp.today(), periods=30)
    np.random.seed(55)

    kpi_trends = pd.DataFrame({
        "Date": days,
        "RevPAS": 14 + np.cumsum(np.random.randn(30) * 0.3),
        "Utilization": 0.68 + np.cumsum(np.random.randn(30) * 0.005),
        "QueueAbandon": 0.09 - np.cumsum(np.random.randn(30) * 0.002),
    })
    kpi_trends["Utilization"] = kpi_trends["Utilization"].clip(0.4, 1.0)
    kpi_trends["QueueAbandon"] = kpi_trends["QueueAbandon"].clip(0, 0.2)

    fig_kpi = make_subplots(
        rows=1, cols=3,
        subplot_titles=["RevPAS ($)", "Utilization Rate", "Queue Abandon Rate"]
    )
    fig_kpi.add_trace(go.Scatter(x=days, y=kpi_trends["RevPAS"], name="RevPAS", line=dict(color="#3B82F6")), row=1, col=1)
    fig_kpi.add_trace(go.Scatter(x=days, y=kpi_trends["Utilization"], name="Utilization", line=dict(color="#10B981")), row=1, col=2)
    fig_kpi.add_trace(go.Scatter(x=days, y=kpi_trends["QueueAbandon"], name="Queue Abandon", line=dict(color="#EF4444")), row=1, col=3)
    fig_kpi.update_layout(height=320, showlegend=False)
    st.plotly_chart(fig_kpi, use_container_width=True)

    # ---- KPI Health Scorecard ----
    st.subheader("🏥 KPI Health Scorecard")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("RevPAS", "$16.40", delta="+$1.20 WoW")
    col2.metric("Utilization", "72%", delta="+2.1% WoW")
    col3.metric("Queue Abandon", "7.2%", delta="-0.8% WoW", delta_color="inverse")
    col4.metric("Pricing Lift", "+8.3%", delta="-0.5% WoW", delta_color="inverse")
    col5.metric("Revisit Rate", "33%", delta="+1.2% WoW")


# ================================================================
# TAB 3: USER BEHAVIOR
# ================================================================

with tab3:
    st.header("👤 User Behavior Across Product Lifecycle")
    st.markdown("""
    Understand how drivers interact with dynamic pricing — 
    from **awareness → adoption → retention → advocacy**.
    """)

    # ---- Funnel ----
    st.subheader("🔽 Driver Conversion Funnel")

    np.random.seed(77)
    funnel_stages = ["App Opens", "Search Parking", "View Prices", "Select Lot", "Payment", "Return Visit"]
    funnel_values = [10000, 7800, 5400, 3200, 2100, 840]

    fig_funnel = go.Figure(go.Funnel(
        y=funnel_stages,
        x=funnel_values,
        textinfo="value+percent initial",
        marker=dict(color=["#3B82F6", "#60A5FA", "#93C5FD", "#BAE6FD", "#FCA5A5", "#F87171"])
    ))
    fig_funnel.update_layout(title="Parking App — User Conversion Funnel", height=400)
    st.plotly_chart(fig_funnel, use_container_width=True)

    # ---- Behavior Segments ----
    st.subheader("👥 User Behavior Segments")

    seg_col1, seg_col2 = st.columns(2)

    with seg_col1:
        segments = ["Commuters (Daily)", "Shoppers (Weekly)", "Visitors (One-time)", "EV Drivers", "Price-Sensitive"]
        seg_sizes = [38, 27, 18, 9, 8]
        fig_seg = px.pie(
            values=seg_sizes, names=segments,
            title="Driver Segments by Frequency",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_seg, use_container_width=True)

    with seg_col2:
        seg_behavior = pd.DataFrame({
            "Segment": segments,
            "Avg Sessions/Mo": [22, 4, 1, 8, 6],
            "Price Sensitivity": ["Low", "Medium", "Low", "Low", "High"],
            "Churn Risk": ["Low", "Medium", "N/A", "Low", "High"],
            "Revenue/User ($)": [198, 64, 18, 112, 42]
        })
        st.dataframe(seg_behavior, use_container_width=True, height=230)

    # ---- Heatmap: Hourly Behavior ----
    st.subheader("⏰ Hourly Demand Pattern (Day × Hour)")

    hours = list(range(24))
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    np.random.seed(42)
    demand_matrix = np.random.randint(20, 100, (7, 24))
    demand_matrix[0:5, 7:10] = np.random.randint(70, 100, (5, 3))   # weekday morning rush
    demand_matrix[0:5, 17:20] = np.random.randint(75, 100, (5, 3))  # weekday evening rush
    demand_matrix[5:7, 10:16] = np.random.randint(80, 100, (2, 6))  # weekend midday

    fig_heat = px.imshow(
        demand_matrix,
        x=hours, y=days_of_week,
        color_continuous_scale="YlOrRd",
        title="Parking Demand by Day & Hour",
        labels=dict(x="Hour of Day", y="Day", color="Demand Index")
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    # ---- Retention Curve ----
    st.subheader("📉 User Retention Curve (Cohort Analysis)")

    cohort_weeks = list(range(1, 13))
    cohort_retention = [100, 72, 58, 48, 42, 38, 35, 33, 31, 30, 29, 28]

    fig_ret = go.Figure()
    fig_ret.add_trace(go.Scatter(
        x=cohort_weeks, y=cohort_retention,
        mode="lines+markers",
        fill="tozeroy",
        line=dict(color="#3B82F6", width=2.5),
        name="Retention"
    ))
    fig_ret.add_hline(y=30, line_dash="dash", line_color="red",
                      annotation_text="Target: 30% at Week 12")
    fig_ret.update_layout(
        title="Driver Retention — Week 1 to Week 12",
        xaxis_title="Week Since First Use",
        yaxis_title="% Users Still Active",
        height=350
    )
    st.plotly_chart(fig_ret, use_container_width=True)


# ================================================================
# TAB 4: PM + ENGINEERING COLLABORATION
# ================================================================

with tab4:
    st.header("🤝 PM + Engineering Collaboration Framework")
    st.markdown("""
    Structure your cross-functional workflows so experiments move faster 
    and decisions are grounded in data.
    """)

    # ---- Active Experiments Board ----
    st.subheader("🗂️ Active Experiment Backlog")

    experiments_board = pd.DataFrame({
        "Experiment": [
            "Surge pricing at >85% occupancy",
            "Real-time competitor price matching",
            "Queue-length discount (>5 cars)",
            "Time-of-day tiered pricing",
            "EV bay premium pricing",
            "Pre-booking discount (-10%)",
            "Loyalty pricing for daily commuters"
        ],
        "Owner (PM)": ["Priya", "Rohan", "Ananya", "Priya", "Rohan", "Meera", "Meera"],
        "Eng Lead": ["Vikram", "Suresh", "Vikram", "Anjali", "Suresh", "Anjali", "Vikram"],
        "Status": [
            "🟢 Running", "🟡 In Review", "🔵 Planned",
            "🟢 Running", "🔵 Planned", "🟡 In Review", "🔴 Blocked"
        ],
        "Started": ["2024-01-02", "2024-01-08", "—", "2024-01-04", "—", "2024-01-10", "2024-01-01"],
        "Est. End": ["2024-01-22", "2024-01-20", "2024-02-01", "2024-01-24", "2024-02-10", "2024-01-30", "—"],
        "Hypothesis": [
            "Surge at 85%+ will increase RevPAS by 15%",
            "Matching competitor prices reduces churn",
            "Queue discount clears backlog faster",
            "AM/PM tiers improve utilization by 8%",
            "EV premium adds $3 per session",
            "Pre-booking grows committed revenue",
            "Loyalty pricing lifts revisit rate 10%"
        ]
    })
    st.dataframe(experiments_board, use_container_width=True, height=300)

    # ---- DACI Framework ----
    st.subheader("🎭 DACI Decision Framework — Who Does What?")

    daci_data = pd.DataFrame({
        "Decision": [
            "Launch new pricing model",
            "Change confidence threshold",
            "Extend experiment duration",
            "Rollback failing variant",
            "Define new KPI",
            "Approve engineering spec"
        ],
        "Driver (D)": ["PM", "Analyst", "PM", "Engineer", "PM", "PM"],
        "Approver (A)": ["VP Product", "PM", "VP Product", "PM", "Director", "Tech Lead"],
        "Contributor (C)": ["Data, Eng", "Data", "Eng, Ops", "QA, Ops", "Finance, Ops", "PM, QA"],
        "Informed (I)": ["Marketing, Ops", "VP Product", "Marketing", "PM, Finance", "All", "Product, Marketing"]
    })
    st.dataframe(daci_data, use_container_width=True, height=250)

    # ---- Feature Flags ----
    st.subheader("🚩 Feature Flag Status (Engineering Toggles)")

    flag_col1, flag_col2 = st.columns(2)

    flags = {
        "surge_pricing_v2": True,
        "competitor_matching": False,
        "queue_discount": False,
        "tod_tiering": True,
        "ev_premium": False,
        "prebooking_discount": False,
        "loyalty_pricing": False,
    }

    with flag_col1:
        for flag, status in list(flags.items())[:4]:
            icon = "🟢 ON" if status else "⚫ OFF"
            st.markdown(f"`{flag}` → **{icon}**")

    with flag_col2:
        for flag, status in list(flags.items())[4:]:
            icon = "🟢 ON" if status else "⚫ OFF"
            st.markdown(f"`{flag}` → **{icon}**")

    # ---- Experiment Velocity ----
    st.subheader("⚡ Experiment Velocity — Experiments Shipped per Week")

    np.random.seed(11)
    weeks = pd.date_range(end=pd.Timestamp.today(), periods=12, freq="W")
    velocity = np.random.randint(1, 5, 12)

    fig_vel = px.bar(
        x=weeks, y=velocity,
        title="Experiments Shipped per Week",
        labels={"x": "Week", "y": "Experiments"},
        color=velocity,
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_vel, use_container_width=True)


# ================================================================
# TAB 5: DECISION INFLUENCE
# ================================================================

with tab5:
    st.header("🎯 Influence Product Decisions — Not Just Report Metrics")
    st.markdown("""
    This section connects experimental outcomes to **business decisions**, 
    surfacing recommendations PMs can act on immediately.
    """)

    # ---- Decision Signal Board ----
    st.subheader("🚦 Decision Signal Board — Act Now")

    signals = [
        {
            "Signal": "🔴 Queue Abandon Rate > 7%",
            "Insight": "Drivers leave when wait > 4 min. Queue-based discount could reduce abandonment.",
            "Recommendation": "Run queue-length discount experiment — target 3% reduction in 2 weeks",
            "Impact": "High",
            "Effort": "Low",
            "Priority": "P0"
        },
        {
            "Signal": "🟡 RevPAS below $18 target",
            "Insight": "Surge pricing isn't activating often enough. Threshold may be too high at 85%.",
            "Recommendation": "Lower surge threshold to 75% and A/B test vs current",
            "Impact": "High",
            "Effort": "Medium",
            "Priority": "P1"
        },
        {
            "Signal": "🟢 Utilization at 72% (near target)",
            "Insight": "Evening hours 6-9pm show 89% occupancy — opportunity for TOD premium.",
            "Recommendation": "Ship time-of-day tier pricing for peak evening hours",
            "Impact": "Medium",
            "Effort": "Low",
            "Priority": "P1"
        },
        {
            "Signal": "🟡 Revisit Rate at 33% (target 40%)",
            "Insight": "Commuter segment shows high potential but no loyalty mechanic exists.",
            "Recommendation": "Design loyalty pricing experiment — 5% discount after 10 sessions",
            "Impact": "High",
            "Effort": "High",
            "Priority": "P2"
        },
    ]

    for sig in signals:
        priority_color = {"P0": "🔴", "P1": "🟡", "P2": "🔵"}.get(sig["Priority"], "⚪")
        with st.expander(f"{priority_color} [{sig['Priority']}] {sig['Signal']}"):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**💡 Insight:** {sig['Insight']}")
                st.markdown(f"**✅ Recommendation:** {sig['Recommendation']}")
            with col2:
                st.metric("Impact", sig["Impact"])
                st.metric("Effort", sig["Effort"])

    # ---- Impact vs Effort Matrix ----
    st.subheader("📊 Experiment Impact vs Effort Matrix")

    matrix_data = pd.DataFrame({
        "Experiment": [
            "Queue Discount", "Surge Threshold ↓", "TOD Tiering",
            "Competitor Match", "Loyalty Pricing", "EV Premium", "Pre-booking"
        ],
        "Impact Score": [8.5, 9.0, 7.0, 7.5, 8.0, 5.0, 6.5],
        "Effort Score": [2.0, 3.0, 3.5, 7.0, 8.0, 4.0, 6.0],
        "Estimated Lift (%)": [3.0, 7.5, 5.0, 4.5, 6.0, 2.5, 4.0]
    })

    fig_matrix = px.scatter(
        matrix_data,
        x="Effort Score", y="Impact Score",
        size="Estimated Lift (%)",
        text="Experiment",
        color="Estimated Lift (%)",
        color_continuous_scale="RdYlGn",
        title="Impact vs Effort — Prioritization Matrix",
        size_max=30
    )
    fig_matrix.add_vline(x=5, line_dash="dash", line_color="gray")
    fig_matrix.add_hline(y=7, line_dash="dash", line_color="gray")
    fig_matrix.add_annotation(x=1.5, y=9.5, text="🚀 Quick Wins", showarrow=False, font=dict(color="green", size=11))
    fig_matrix.add_annotation(x=8, y=9.5, text="🏔 Big Bets", showarrow=False, font=dict(color="orange", size=11))
    fig_matrix.add_annotation(x=1.5, y=5.5, text="🧹 Fill-ins", showarrow=False, font=dict(color="gray", size=11))
    fig_matrix.add_annotation(x=8, y=5.5, text="❓ Reconsider", showarrow=False, font=dict(color="red", size=11))
    fig_matrix.update_traces(textposition="top center")
    fig_matrix.update_layout(height=480)
    st.plotly_chart(fig_matrix, use_container_width=True)

    # ---- PRD Snippet Generator ----
    st.subheader("📝 Quick PRD Snippet — Experiment Brief")
    st.markdown("Generate a mini experiment brief to share with your PM / Engineering team.")

    selected_exp = st.selectbox("Select Experiment to Brief", matrix_data["Experiment"].tolist())
    exp_row = matrix_data[matrix_data["Experiment"] == selected_exp].iloc[0]

    prd_text = f"""
## Experiment Brief: {selected_exp}

**Hypothesis:**  
If we implement "{selected_exp}" then we expect to see a +{exp_row['Estimated Lift (%)']:.0f}% improvement 
in the primary metric, because [driver insight from data above].

**Primary Metric:** Revenue per Available Slot (RevPAS)  
**Secondary Metrics:** Utilization Rate, Queue Abandon Rate  
**Guardrail Metric:** Driver Revisit Rate (must not drop > 2%)  

**Design:**  
- Control (A): Current dynamic pricing model  
- Variant (B): {selected_exp} applied to 50% of lots  
- Duration: 14 days  
- Confidence: 95%  

**Impact Estimate:** {exp_row['Impact Score']}/10  
**Effort Estimate:** {exp_row['Effort Score']}/10  

**Owner:** PM Lead  
**Eng Lead:** TBD  
**Review Date:** [insert]
"""

    st.code(prd_text, language="markdown")
    st.download_button(
        "📥 Download Experiment Brief",
        data=prd_text,
        file_name=f"experiment_brief_{selected_exp.lower().replace(' ', '_')}.md",
        mime="text/markdown"
    )
