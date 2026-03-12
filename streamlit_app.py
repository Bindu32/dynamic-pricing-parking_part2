import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

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
    df = pd.read_csv("dataset.csv")

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

    traffic_map = {
        "low": 1,
        "medium": 1.5,
        "high": 2
    }

    df["traffic_weight"] = df["TrafficConditionNearby"].map(
        traffic_map
    ).fillna(1)

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

sst.subheader("📊 Occupancy Impact on Price")

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
    [
        row["latitude"],
        row["longitude"],
        row["occupancy_rate"]
    ]
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

