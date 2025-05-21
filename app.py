import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from fuzzy_parking_system import FuzzyParkingSystem

st.set_page_config(page_title="Fuzzy Parking System", layout="wide")

st.title("Fuzzy Parking System Demo")

# Sidebar for inputs
st.sidebar.header("Input Parameters")

# Input sliders
distance = st.sidebar.slider("Distance to Parking Spot (meters)", 0, 10, 5)
angle = st.sidebar.slider("Angle of Approach (degrees)", 0, 90, 45)

# Create fuzzy system
fuzzy_system = FuzzyParkingSystem()

# Calculate steering angle
steering_angle = fuzzy_system.calculate_steering_angle(distance, angle)

# Display results
st.header("Results")
st.write(f"Calculated Steering Angle: {steering_angle:.2f} degrees")

# Create visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Plot membership functions
fuzzy_system.plot_membership_functions(ax1)
ax1.set_title("Membership Functions")

# Plot current input values
fuzzy_system.plot_current_values(distance, angle, steering_angle, ax2)
ax2.set_title("Current Values")

st.pyplot(fig)

# Add explanation
st.markdown("""
### How it works
This system uses fuzzy logic to determine the optimal steering angle for parking.
- **Distance**: How far the car is from the parking spot
- **Angle**: The approach angle of the car
- **Steering Angle**: The calculated optimal steering angle for parking
""") 