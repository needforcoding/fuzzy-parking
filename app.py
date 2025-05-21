import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from fuzzy_parking_system import ParkingGuidanceSystem

# Page configuration
st.set_page_config(
    page_title="Fuzzy Parking System",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🚗 Fuzzy Parking System Demo")
st.markdown("""
    This intelligent parking system uses fuzzy logic to determine the optimal parking area 
    and estimate waiting times based on various factors. Adjust the parameters in the sidebar 
    and click 'Calculate' to get recommendations.
""")

# Sidebar for inputs
with st.sidebar:
    st.header("Input Parameters")
    
    # Input sliders with better formatting
    traffic_density = st.slider(
        "Traffic Density (%)",
        min_value=0,
        max_value=100,
        value=50,
        help="Current traffic conditions in the parking area"
    )
    
    time_of_day = st.slider(
        "Time of Day (hours)",
        min_value=0,
        max_value=24,
        value=12,
        help="Current time of day"
    )
    
    weather_condition = st.slider(
        "Weather Condition (0-10)",
        min_value=0,
        max_value=10,
        value=5,
        help="0: Clear, 5: Light Rain, 10: Heavy Rain/Snow"
    )
    
    vacancy_rate = st.slider(
        "Vacancy Rate (%)",
        min_value=0,
        max_value=100,
        value=50,
        help="Percentage of available parking spaces"
    )
    
    user_type = st.selectbox(
        "User Type",
        options=[1, 2, 3, 4, 5],
        format_func=lambda x: {
            1: "Regular",
            2: "Member",
            3: "VIP",
            4: "Disabled",
            5: "Staff"
        }[x],
        help="Select your user type"
    )
    
    # Add calculate button
    calculate_button = st.button("Calculate", type="primary", use_container_width=True)

# Create fuzzy system
fuzzy_system = ParkingGuidanceSystem()

# Only calculate and show results when button is clicked
if calculate_button:
    with st.spinner("Calculating recommendations..."):
        # Get recommendation
        result = fuzzy_system.get_recommendation(
            traffic_density, time_of_day, weather_condition, vacancy_rate, user_type
        )

        # Display results in a nice format
        st.header("Results")
        
        if "error" in result:
            st.error(result["error"])
        else:
            # Create two columns for results
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    label="Recommended Parking Area",
                    value=result['recommended_area_text']
                )
            
            with col2:
                st.metric(
                    label="Estimated Waiting Time",
                    value=result['waiting_time_text']
                )
            
            # Add a visual separator
            st.divider()
            
            # Show input values used for calculation
            st.subheader("Input Values Used")
            input_col1, input_col2, input_col3 = st.columns(3)
            
            with input_col1:
                st.write(f"**Traffic Density:** {traffic_density}%")
                st.write(f"**Time of Day:** {time_of_day}:00")
            
            with input_col2:
                st.write(f"**Weather Condition:** {weather_condition}/10")
                st.write(f"**Vacancy Rate:** {vacancy_rate}%")
            
            with input_col3:
                user_type_text = {
                    1: "Regular",
                    2: "Member",
                    3: "VIP",
                    4: "Disabled",
                    5: "Staff"
                }[user_type]
                st.write(f"**User Type:** {user_type_text}")

# Add explanation
with st.expander("How it works"):
    st.markdown("""
    This system uses fuzzy logic to determine the optimal parking area and estimate waiting times based on:
    
    - **Traffic Density**: Current traffic conditions in the parking area
    - **Time of Day**: Current time (0-24 hours)
    - **Weather Condition**: Current weather (0: Clear, 10: Heavy Rain/Snow)
    - **Vacancy Rate**: Percentage of available parking spaces
    - **User Type**: Type of user (Regular, Member, VIP, etc.)
    
    ### How to use:
    1. Adjust the input parameters in the sidebar
    2. Click the "Calculate" button
    3. View the results below
    
    The system will recommend the best parking area and provide an estimated waiting time based on your inputs.
    """) 
