# Fuzzy Logic Parking Guidance System 
# ** Ahmet Feyzi Gülmez **

A Python-based fuzzy logic control system for recommending optimal parking areas and estimating waiting times based on multiple input factors like traffic density, time of day, weather conditions, vacancy rate, and user type.

## Project Overview

This parking guidance system uses fuzzy logic to handle imprecise information and make human-like decisions based on linguistic variables. It provides recommendations about which parking area to use (from Area A to E) and estimates waiting time (from very short to very long) based on current conditions.

### Features

- Processes 5 input variables: traffic density, time of day, weather condition, vacancy rate, and user type
- Produces 2 output recommendations: parking area and waiting time
- Interactive GUI with sliders, radio buttons, and dropdown menus for input
- Real-time visualization of fuzzy membership functions
- Current time synchronization
- Detailed result display

## System Architecture

### Input Variables

1. **Traffic Density (0-100%)**
   - Linguistic values: Low, Medium, High

2. **Time of Day (0-24 hours)**
   - Linguistic values: Early Morning, Morning, Noon, Afternoon, Evening, Night

3. **Weather Condition (0-10)**
   - Linguistic values: Clear, Light Rain, Heavy Rain, Snow

4. **Vacancy Rate (0-100%)**
   - Linguistic values: Very Low, Low, Medium, High, Very High

5. **User Type (1-5)**
   - Linguistic values: Regular, Member, VIP, Disabled, Staff

### Output Variables

1. **Recommended Parking Area (1-5)**
   - Linguistic values: Area A (closest), Area B, Area C, Area D, Area E (farthest)

2. **Estimated Waiting Time (0-30 minutes)**
   - Linguistic values: Very Short, Short, Medium, Long, Very Long

### Fuzzy Rules

The system uses 32 fuzzy rules to determine the outputs based on the inputs. Some examples include:

- If vacancy rate is very high, then recommend Area A
- If traffic density is high and vacancy rate is low, then waiting time is very long
- If weather is snow and user is disabled, then recommend Area A

## Installation and Setup

### Prerequisites

- Python 3.6 or higher

### Dependencies

The project requires the following Python packages:
- numpy
- scikit-fuzzy
- matplotlib
- tkinter (usually comes with Python)

### Installation Steps

1. Clone the repository:
   ```
   git clone https://github.com/needforcoding/fuzzy-parking.git
   cd fuzzy-parking
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## How to Run

Run the application with:

```
python main.py
```

This will open the GUI application where you can:

1. Adjust the input parameters using sliders, radio buttons, and dropdowns
2. Click the "Calculate Recommendation" button to get parking recommendations
3. View the recommended parking area and estimated waiting time
4. Explore the fuzzy membership functions through the visualization tabs

## User Interface Guide

### Input Controls
- **Traffic Density**: Use the slider to set the current traffic congestion (0-100%)
- **Time of Day**: Set the hour of the day (0-24) or click "Current" to use the current time
- **Weather Condition**: Either use the slider or select a weather condition from the dropdown
- **Vacancy Rate**: Set the percentage of available parking spaces (0-100%)
- **User Type**: Select the user type from Regular, Member, VIP, Disabled, or Staff

### Recommendation Output
- The system will display the recommended parking area (A through E)
- The system will display the estimated waiting time in minutes
- Numeric values for both recommendations are also provided

### Visualization
- View the membership functions for all input and output variables
- Select different variables from the dropdown menus to see their respective fuzzy sets

## System Logic

The system uses the following process to generate recommendations:

1. Input values are fuzzified using membership functions
2. The fuzzy rules are evaluated to determine the degree of activation
3. The activated rules are aggregated
4. The centroid method is used for defuzzification to produce crisp output values

## Project Structure

- `fuzzy_parking_system.py`: Core implementation of the fuzzy logic system
- `fuzzy_parking_gui.py`: GUI implementation using Tkinter
- `main.py`: Entry point for the application
- `requirements.txt`: Required Python packages

## Future Enhancements

- Real-time data integration from parking sensors
- Mobile application interface
- Historical data analysis for predictive recommendations
- User feedback integration to improve recommendations

## Acknowledgements

This project was developed as an educational demonstration of fuzzy logic control systems.

## Online Demo

You can try the Fuzzy Parking System online without installing anything on your computer. Just visit our Streamlit demo:
[Online Demo](https://fuzzy-parking.streamlit.app/)

The online demo allows you to:

- Adjust the distance and angle parameters using interactive sliders
- See the calculated steering angle in real-time
- View the membership functions and current values visualization
- Understand how the fuzzy logic system works
