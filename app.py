import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from fuzzy_parking_system import ParkingGuidanceSystem

st.set_page_config(page_title="Fuzzy Parking System", layout="wide")

st.title("Fuzzy Parking System Demo")

# Sidebar for inputs
st.sidebar.header("Input Parameters")

# Input sliders
traffic_density = st.sidebar.slider("Traffic Density (%)", 0, 100, 50)
time_of_day = st.sidebar.slider("Time of Day (hours)", 0, 24, 12)
weather_condition = st.sidebar.slider("Weather Condition (0-10)", 0, 10, 5)
vacancy_rate = st.sidebar.slider("Vacancy Rate (%)", 0, 100, 50)
user_type = st.sidebar.selectbox("User Type", [1, 2, 3, 4, 5], format_func=lambda x: {
    1: "Regular",
    2: "Member",
    3: "VIP",
    4: "Disabled",
    5: "Staff"
}[x])

# Create fuzzy system
fuzzy_system = ParkingGuidanceSystem()

# Get recommendation
result = fuzzy_system.get_recommendation(
    traffic_density, time_of_day, weather_condition, vacancy_rate, user_type
)

# Display results
st.header("Results")
if "error" in result:
    st.error(result["error"])
else:
    st.write(f"Recommended Area: {result['recommended_area_text']}")
    st.write(f"Estimated Waiting Time: {result['waiting_time_text']}")

# Add explanation
st.markdown("""
### How it works
This system uses fuzzy logic to determine the optimal parking area and estimate waiting times based on:
- **Traffic Density**: Current traffic conditions
- **Time of Day**: Current time
- **Weather Condition**: Current weather
- **Vacancy Rate**: Available parking spaces
- **User Type**: Type of user (Regular, Member, VIP, etc.)
""") 
