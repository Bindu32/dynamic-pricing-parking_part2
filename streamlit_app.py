import streamlit as st
import pandas as pd
import numpy as np
import time
from bokeh.plotting import figure

st.set_page_config(page_title="Real-Time Parking Pricing", layout="wide")

st.title("🚗 Real-Time Dynamic Parking Pricing")

st.markdown(
"""
This dashboard simulates **real-time parking demand and dynamic pricing**.
Prices adjust automatically based on occupancy, traffic and queue length.
"""
)

# -----------------------
# Load dataset
# -----------------------
df = pd.read_csv("dataset.csv")

# -----------------------
# Pricing model
# -----------------------
def dynamic_pricing(df):

    base_price = 10

    df["occupancy_rate"] = df["Occupancy"] / df["Capacity"]

    traffic_map = {"low":1,"medium":1.5,"high":2}
    df["traffic_weight"] = df["TrafficConditionNearby"].map(traffic_map).fillna(1)

    df["dynamic_price"] = (
        base_price
        * (1 + 1.5*df["occupancy_rate"])
        * (1 + 0.2*df["traffic_weight"])
        * (1 + 0.1*df["QueueLength"])
    )

    return df

# -----------------------
# Real-time simulation
# -----------------------
placeholder = st.empty()

for step in range(50):

    # simulate new demand
    df["Occupancy"] = df["Occupancy"] + np.random.randint(-2,5,len(df))

    df["Occupancy"] = df["Occupancy"].clip(0,df["Capacity"])

    df["QueueLength"] = np.random.randint(0,5,len(df))

    df = dynamic_pricing(df)

    with placeholder.container():

        st.subheader("Live Parking Metrics")

        col1,col2,col3 = st.columns(3)

        col1.metric("Avg Occupancy",
                    f"{df['occupancy_rate'].mean():.2f}")

        col2.metric("Avg Price",
                    f"${df['dynamic_price'].mean():.2f}")

        revenue = (df["dynamic_price"]*df["Occupancy"]).sum()

        col3.metric("Estimated Revenue",
                    f"${revenue:,.0f}")

        # price chart
        p = figure(
            title="Live Pricing",
            x_axis_label="Parking Lot",
            y_axis_label="Price",
            height=400
        )

        x = list(range(len(df)))

        p.line(x, df["dynamic_price"], line_width=2)

        st.bokeh_chart(p, use_container_width=True)

        st.dataframe(
            df[[
                "SystemCodeNumber",
                "Occupancy",
                "Capacity",
                "dynamic_price"
            ]].head(10)
        )

    time.sleep(3)
