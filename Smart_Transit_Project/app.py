import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Smart Transit Load Balancer",
    layout="wide"
)

st.title("Smart Transit Load Balancer")
st.write("Big Data Analytics and Cloud Computing Project")

from pathlib import Path

csv_path = Path(__file__).parent / "final_transit_data.csv"
data = pd.read_csv(csv_path)

# Summary values
total_records = len(data)
avg_passengers = data["Passenger_Count"].mean()
avg_load = data["Load_Percentage"].mean()
overloaded = len(data[data["Load_Status"] == "Overloaded"])

# Display summary
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", total_records)
col2.metric("Average Passengers", round(avg_passengers, 2))
col3.metric("Average Load %", round(avg_load, 2))
col4.metric("Overloaded Trips", overloaded)

st.divider()

# Route-wise analysis
st.subheader("Average Passengers by Route")

route_analysis = data.groupby("Route_ID")["Passenger_Count"].mean()
st.bar_chart(route_analysis)

# Demand distribution
st.subheader("Demand Level Distribution")

demand_count = data["Demand_Level"].value_counts()
st.bar_chart(demand_count)

# Select route
st.subheader("Route Details")

selected_route = st.selectbox(
    "Select Route",
    sorted(data["Route_ID"].unique())
)

route_data = data[data["Route_ID"] == selected_route]

st.dataframe(
    route_data[
        [
            "Bus_ID",
            "Time",
            "Passenger_Count",
            "Bus_Capacity",
            "Load_Percentage",
            "Load_Status",
            "Demand_Level",
            "Recommendation"
        ]
    ]
)

# Overloaded buses
st.subheader("Overloaded Trips")

overloaded_data = data[data["Load_Status"] == "Overloaded"]

st.dataframe(
    overloaded_data[
        [
            "Route_ID",
            "Bus_ID",
            "Passenger_Count",
            "Bus_Capacity",
            "Load_Percentage",
            "Recommendation"
        ]
    ]
)
