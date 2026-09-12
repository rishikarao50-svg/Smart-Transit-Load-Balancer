import streamlit as st
import pandas as pd
from pathlib import Path

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(
    page_title="Smart Transit Load Balancer",
    page_icon="🚌",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
csv_path = Path(__file__).parent / "final_transit_data.csv"
data = pd.read_csv(csv_path)

# -----------------------------
# TITLE
# -----------------------------
st.title("🚌 Smart Transit Load Balancer")
st.caption("Big Data Analytics and Cloud Computing Project")

st.divider()

# -----------------------------
# OVERALL METRICS
# -----------------------------
total_records = len(data)
avg_passengers = data["Passenger_Count"].mean()
avg_load = data["Load_Percentage"].mean()
overloaded = len(data[data["Load_Status"] == "Overloaded"])

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Transit Records", total_records)
col2.metric("Average Passengers", round(avg_passengers, 2))
col3.metric("Average Load", f"{round(avg_load, 2)}%")
col4.metric("Overloaded Trips", overloaded)

st.divider()

# -----------------------------
# ROUTE FILTER
# -----------------------------
st.subheader("🔎 Route Analysis")

selected_route = st.selectbox(
    "Select a Route",
    ["All Routes"] + sorted(data["Route_ID"].unique().tolist())
)

if selected_route == "All Routes":
    filtered_data = data
else:
    filtered_data = data[data["Route_ID"] == selected_route]

# -----------------------------
# ROUTE GRAPH
# -----------------------------
st.subheader("📊 Average Passenger Count by Route")

route_analysis = (
    filtered_data.groupby("Route_ID")["Passenger_Count"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(route_analysis)

# -----------------------------
# DEMAND DISTRIBUTION
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Demand Level Distribution")
    demand_count = filtered_data["Demand_Level"].value_counts()
    st.bar_chart(demand_count)

with col2:
    st.subheader("Load Status Distribution")
    load_count = filtered_data["Load_Status"].value_counts()
    st.bar_chart(load_count)

st.divider()

# -----------------------------
# SMART RECOMMENDATION
# -----------------------------
st.subheader("🤖 Smart Transit Recommendation")

route_summary = (
    filtered_data.groupby("Route_ID")
    .agg(
        Average_Passengers=("Passenger_Count", "mean"),
        Average_Load=("Load_Percentage", "mean")
    )
    .reset_index()
)

for _, row in route_summary.iterrows():
    route = row["Route_ID"]
    load = row["Average_Load"]

    if load > 100:
        st.error(
            f"{route}: Overloaded - Add an additional bus immediately."
        )

    elif load >= 80:
        st.warning(
            f"{route}: High demand - Consider increasing bus frequency."
        )

    elif load >= 50:
        st.success(
            f"{route}: Normal load - Current service is sufficient."
        )

    else:
        st.info(
            f"{route}: Low demand - Bus frequency can be reduced."
        )

st.divider()

# -----------------------------
# HIGH DEMAND TRIPS
# -----------------------------
st.subheader("🚨 High Demand and Overloaded Trips")

high_demand = filtered_data[
    (filtered_data["Demand_Level"] == "High Demand") |
    (filtered_data["Load_Status"] == "Overloaded")
]

st.dataframe(
    high_demand[
        [
            "Route_ID",
            "Bus_ID",
            "Time",
            "Passenger_Count",
            "Bus_Capacity",
            "Load_Percentage",
            "Load_Status",
            "Demand_Level",
            "Recommendation"
        ]
    ],
    use_container_width=True
)

# -----------------------------
# FULL DATA
# -----------------------------
with st.expander("View Complete Transit Data"):
    st.dataframe(filtered_data, use_container_width=True)

st.divider()

st.write(
    "This system uses Big Data Analytics and K-Means clustering "
    "to identify transit demand patterns and recommend better "
    "allocation of buses."
)
