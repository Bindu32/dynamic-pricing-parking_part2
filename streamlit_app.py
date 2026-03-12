import streamlit as st
import pandas as pd
from bokeh.plotting import figure

# -----------------------------------
# Page configuration
# -----------------------------------
st.set_page_config(
    page_title="Dynamic Parking Pricing Dashboard",
    layout="wide"
)

# -----------------------------------
# Title
# -----------------------------------
st.title("🚗 Dynamic Parking Pricing Dashboard")

st.markdown("""
This dashboard demonstrates **dynamic pricing optimization for urban parking systems**.

Pricing adjusts based on:

- Parking occupancy
- Nearby traffic conditions
- Queue length
- Competitor pricing

The goal is to **maximize revenue while remaining competitive**.
""")

# -----------------------------------
# Sidebar
# -----------------------------------
st.sidebar.header("Dashboard Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload Parking Dataset (CSV)",
    type=["csv"]
)

# -----------------------------------
# Load dataset
# -----------------------------------
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("Custom dataset loaded")
else:
    df = pd.read_csv("dataset.csv")
    st.sidebar.info("Using default dataset")

# -----------------------------------
# Filters
# -----------------------------------
st.sidebar.subheader("Filters")

min_occupancy = st.sidebar.slider(
    "Minimum Occupancy",
    0,
    int(df["Occupancy"].max()),
    0
)

df = df[df["Occupancy"] >= min_occupancy]

# -----------------------------------
# Dynamic pricing pipeline
# -----------------------------------
def dynamic_pricing_pipeline(df):

    base_price = 10.0

    df["occupancy_rate"] = df["Occupancy"] / df["Capacity"]

    # Linear pricing
    df["linear_price"] = base_price * (1 + df["occupancy_rate"])

    # Traffic weight
    traffic_map = {
        "low": 1.0,
        "medium": 1.5,
        "high": 2.0
    }

    df["traffic_weight"] = df["TrafficConditionNearby"].map(
        traffic_map
    ).fillna(1.0)

    # Dynamic pricing
    df["dynamic_price"] = (
        base_price
        * (1 + 1.5 * df["occupancy_rate"])
        * (1 + 0.2 * df["traffic_weight"])
        * (1 + 0.1 * df["QueueLength"])
    )

    # Competitor pricing
    if "competitor_price" not in df.columns:
        df["competitor_price"] = df["linear_price"] * 0.95

    df["competitive_price"] = df[
        ["dynamic_price", "competitor_price"]
    ].min(axis=1)

    return df


# -----------------------------------
# Run pricing model automatically
# -----------------------------------
df_result = dynamic_pricing_pipeline(df.copy())

# -----------------------------------
# KPI Metrics
# -----------------------------------
st.subheader("📊 Pricing Metrics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Avg Linear Price",
    f"{df_result['linear_price'].mean():.2f}"
)

col2.metric(
    "Avg Dynamic Price",
    f"{df_result['dynamic_price'].mean():.2f}"
)

col3.metric(
    "Avg Competitive Price",
    f"{df_result['competitive_price'].mean():.2f}"
)

# -----------------------------------
# Business Impact (Revenue)
# -----------------------------------
st.subheader("💰 Revenue Impact")

estimated_linear_revenue = (
    df_result["linear_price"] * df_result["Occupancy"]
).sum()

estimated_dynamic_revenue = (
    df_result["dynamic_price"] * df_result["Occupancy"]
).sum()

revenue_gain = (
    estimated_dynamic_revenue - estimated_linear_revenue
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Linear Pricing Revenue",
    f"${estimated_linear_revenue:,.0f}"
)

col2.metric(
    "Dynamic Pricing Revenue",
    f"${estimated_dynamic_revenue:,.0f}"
)

col3.metric(
    "Revenue Increase",
    f"${revenue_gain:,.0f}"
)

# -----------------------------------
# Pricing comparison chart
# -----------------------------------
st.subheader("📈 Pricing Comparison")

p = figure(
    title="Linear vs Dynamic vs Competitive Pricing",
    x_axis_label="Parking Lot Index",
    y_axis_label="Price",
    height=400
)

x = list(range(len(df_result)))

p.line(
    x,
    df_result["linear_price"],
    legend_label="Linear Price",
    line_width=2
)

p.line(
    x,
    df_result["dynamic_price"],
    legend_label="Dynamic Price",
    line_width=2
)

p.line(
    x,
    df_result["competitive_price"],
    legend_label="Competitive Price",
    line_width=2
)

p.legend.location = "top_left"

st.bokeh_chart(p, use_container_width=True)

# -----------------------------------
# Occupancy vs price analysis
# -----------------------------------
st.subheader("📊 Occupancy Impact on Price")

p2 = figure(
    title="Occupancy Rate vs Dynamic Price",
    x_axis_label="Occupancy Rate",
    y_axis_label="Dynamic Price",
    height=400
)

p2.circle(
    df_result["occupancy_rate"],
    df_result["dynamic_price"],
    size=8
)

st.bokeh_chart(p2, use_container_width=True)

# -----------------------------------
# Top revenue parking lots
# -----------------------------------
st.subheader("🏆 Highest Revenue Parking Lots")

df_result["revenue_dynamic"] = (
    df_result["dynamic_price"] * df_result["Occupancy"]
)

top_lots = df_result.sort_values(
    "revenue_dynamic",
    ascending=False
).head(10)

st.dataframe(
    top_lots[
        [
            "SystemCodeNumber",
            "Occupancy",
            "Capacity",
            "dynamic_price",
            "revenue_dynamic"
        ]
    ],
    use_container_width=True
)

# -----------------------------------
# Dataset preview
# -----------------------------------
st.subheader("📂 Dataset Preview")

st.dataframe(df_result.head(50), use_container_width=True)

# -----------------------------------
# Model explanation
# -----------------------------------
st.subheader("⚙️ Pricing Model Logic")

st.markdown("""
Dynamic pricing is calculated using multiple real-world demand signals.

Dynamic Price = Base Price  × Occupancy Impact  × Traffic Factor  × Queue Impact

Key Drivers:

• Higher occupancy increases demand → price increases  
• Heavy nearby traffic increases parking demand  
• Longer queue length indicates higher demand  
• Competitor price ensures competitive market pricing  

This simulation demonstrates how **smart city parking systems can use
data-driven pricing strategies to optimize revenue and demand allocation.**
""")

