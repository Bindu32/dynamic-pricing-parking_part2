import streamlit as st
import pandas as pd
from bokeh.plotting import figure

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
    page_title="Dynamic Parking Pricing",
    layout="wide"
)

# -------------------------------
# Title & description
# -------------------------------
st.title("🚗 Dynamic Parking Pricing Dashboard")
st.markdown(
    """
    This dashboard demonstrates **dynamic and competitive pricing** for urban parking lots  
    based on **occupancy, traffic conditions, queue length, and competition**.
    """
)

# -------------------------------
# File upload
# -------------------------------
st.sidebar.header("Upload Dataset")
uploaded_file = st.sidebar.file_uploader(
    "Upload parking dataset (CSV)",
    type=["csv"]
)

# -------------------------------
# Load data
# -------------------------------
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("Dataset uploaded successfully")
else:
    st.info("Using default dataset bundled with the app")
    df = pd.read_csv("dataset.csv")
df = pd.read_csv("./dataset.csv")

# -------------------------------
# Pricing pipeline (REUSED LOGIC)
# -------------------------------
def dynamic_pricing_pipeline(df):
    base_price = 10.0

    df["occupancy_rate"] = df["Occupancy"] / df["Capacity"]

    # Linear pricing
    df["linear_price"] = base_price * (1 + df["occupancy_rate"])

    # Traffic weight
    traffic_map = {"low": 1.0, "medium": 1.5, "high": 2.0}
    df["traffic_weight"] = df["TrafficConditionNearby"].map(traffic_map).fillna(1.0)

    # Dynamic pricing
    df["dynamic_price"] = (
        base_price
        * (1 + 1.5 * df["occupancy_rate"])
        * (1 + 0.2 * df["traffic_weight"])
        * (1 + 0.1 * df["QueueLength"])
    )

    # Competitive pricing
    if "competitor_price" not in df.columns:
        df["competitor_price"] = df["linear_price"] * 0.95

    df["competitive_price"] = df[["dynamic_price", "competitor_price"]].min(axis=1)

    return df

# -------------------------------
# Run model button
# -------------------------------
if st.button("Run Pricing Model"):
    with st.spinner("Calculating prices..."):
        df_result = dynamic_pricing_pipeline(df.copy())

    st.success("Pricing model executed successfully")

    # -------------------------------
    # Output table
    # -------------------------------
    st.subheader("📊 Pricing Output (Preview)")
    st.dataframe(
        df_result[
            [
                "SystemCodeNumber",
                "Occupancy",
                "Capacity",
                "linear_price",
                "dynamic_price",
                "competitive_price",
            ]
        ].head(50),
        use_container_width=True
    )

    # -------------------------------
    # Bokeh chart
    # -------------------------------
    st.subheader("📈 Pricing Comparison")

    p = figure(
        title="Linear vs Dynamic vs Competitive Pricing",
        x_axis_label="Parking Lot Index",
        y_axis_label="Price",
        height=400,
        width=900
    )

    p.line(
        df_result.index,
        df_result["linear_price"],
        legend_label="Linear Price",
        line_width=2,
        color="blue"
    )
    p.line(
        df_result.index,
        df_result["dynamic_price"],
        legend_label="Dynamic Price",
        line_width=2,
        color="green"
    )
    p.line(
        df_result.index,
        df_result["competitive_price"],
        legend_label="Competitive Price",
        line_width=2,
        color="red"
    )

    p.legend.location = "top_left"

    st.bokeh_chart(p, use_container_width=True)

    # -------------------------------
    # Insights
    # -------------------------------
    st.subheader("🔍 Key Insights")

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
