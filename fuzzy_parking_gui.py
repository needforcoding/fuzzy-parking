# fuzzy_parking_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import os
from datetime import datetime

# Import the local fuzzy parking system
from fuzzy_parking_system import ParkingGuidanceSystem

class ParkingGuidanceGUI:
    """
    Graphical User Interface for the Parking Guidance System using Tkinter.
    """
    
    def __init__(self, root):
        """
        Initialize the GUI components.
        
        Args:
            root (Tk): The root Tkinter window
        """
        self.root = root
        self.root.title("Fuzzy Logic Parking Guidance System")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize the parking guidance system
        try:
            self.parking_system = ParkingGuidanceSystem()
            self.setup_ui()
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Failed to initialize the parking system: {str(e)}")
            self.root.destroy()
    
    def setup_ui(self):
        """Setup all UI components for the application."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title label
        title_label = ttk.Label(main_frame, text="Parking Guidance System", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # Create frames for inputs, outputs, and visualization
        input_frame = ttk.LabelFrame(main_frame, text="Input Parameters", padding=10)
        input_frame.pack(fill=tk.X, pady=10)
        
        output_frame = ttk.LabelFrame(main_frame, text="Recommendations", padding=10)
        output_frame.pack(fill=tk.X, pady=10)
        
        viz_frame = ttk.LabelFrame(main_frame, text="System Visualization", padding=10)
        viz_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Input controls
        self.setup_input_controls(input_frame)
        
        # Output displays
        self.setup_output_displays(output_frame)
        
        # Visualization area
        self.setup_visualization(viz_frame)
        
        # Calculate button
        calculate_btn = ttk.Button(main_frame, text="Calculate Recommendation", 
                                  command=self.calculate_recommendation)
        calculate_btn.pack(pady=10)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initialize with default values
        self.update_time()
    
    def setup_input_controls(self, parent):
        """
        Create all input controls.
        
        Args:
            parent (Widget): Parent widget to place controls in
        """
        # Create a grid layout for inputs
        input_grid = ttk.Frame(parent)
        input_grid.pack(fill=tk.X, pady=5)
        
        # Traffic Density slider
        ttk.Label(input_grid, text="Traffic Density:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.traffic_density_var = tk.DoubleVar(value=50)
        self.traffic_density_slider = ttk.Scale(input_grid, from_=0, to=100, variable=self.traffic_density_var,
                                              orient=tk.HORIZONTAL, length=200)
        self.traffic_density_slider.grid(row=0, column=1, padx=5, pady=5)
        self.traffic_density_label = ttk.Label(input_grid, text="50%")
        self.traffic_density_label.grid(row=0, column=2, padx=5, pady=5)
        self.traffic_density_var.trace_add("write", lambda *args: self.traffic_density_label.config(
            text=f"{int(self.traffic_density_var.get())}%"))
        
        # Time of Day slider with current time button
        ttk.Label(input_grid, text="Time of Day:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.time_of_day_var = tk.DoubleVar(value=12)
        self.time_of_day_slider = ttk.Scale(input_grid, from_=0, to=24, variable=self.time_of_day_var,
                                         orient=tk.HORIZONTAL, length=200)
        self.time_of_day_slider.grid(row=1, column=1, padx=5, pady=5)
        
        time_frame = ttk.Frame(input_grid)
        time_frame.grid(row=1, column=2, padx=5, pady=5)
        
        self.time_of_day_label = ttk.Label(time_frame, text="12:00")
        self.time_of_day_label.pack(side=tk.LEFT)
        
        current_time_btn = ttk.Button(time_frame, text="Current", width=7, command=self.update_time)
        current_time_btn.pack(side=tk.LEFT, padx=5)
        
        self.time_of_day_var.trace_add("write", lambda *args: self.time_of_day_label.config(
            text=f"{int(self.time_of_day_var.get()):02d}:{int((self.time_of_day_var.get() % 1) * 60):02d}"))
        
        # Weather Condition slider
        ttk.Label(input_grid, text="Weather Condition:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.weather_condition_var = tk.DoubleVar(value=0)
        self.weather_condition_slider = ttk.Scale(input_grid, from_=0, to=10, variable=self.weather_condition_var,
                                               orient=tk.HORIZONTAL, length=200)
        self.weather_condition_slider.grid(row=2, column=1, padx=5, pady=5)
        
        # Get weather condition mapping for combobox
        weather_mapping = self.parking_system.get_weather_condition_mapping()
        self.weather_combo = ttk.Combobox(input_grid, width=15, state="readonly")
        self.weather_combo["values"] = [value for value in weather_mapping.values()]
        self.weather_combo.current(0)  # Set to first weather condition
        self.weather_combo.grid(row=2, column=2, padx=5, pady=5)
        self.weather_combo.bind("<<ComboboxSelected>>", self.on_weather_selected)
        
        # Update weather label when slider changes
        self.weather_condition_var.trace_add("write", lambda *args: self.update_weather_combo())
        
        # Vacancy Rate slider
        ttk.Label(input_grid, text="Vacancy Rate:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.vacancy_rate_var = tk.DoubleVar(value=50)
        self.vacancy_rate_slider = ttk.Scale(input_grid, from_=0, to=100, variable=self.vacancy_rate_var,
                                          orient=tk.HORIZONTAL, length=200)
        self.vacancy_rate_slider.grid(row=3, column=1, padx=5, pady=5)
        self.vacancy_rate_label = ttk.Label(input_grid, text="50%")
        self.vacancy_rate_label.grid(row=3, column=2, padx=5, pady=5)
        self.vacancy_rate_var.trace_add("write", lambda *args: self.vacancy_rate_label.config(
            text=f"{int(self.vacancy_rate_var.get())}%"))
        
        # User Type radio buttons
        ttk.Label(input_grid, text="User Type:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.user_type_var = tk.IntVar(value=1)  # Default to Regular user
        
        user_type_frame = ttk.Frame(input_grid)
        user_type_frame.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        # Get user type mapping for radio buttons
        user_mapping = self.parking_system.get_user_type_mapping()
        for i, (value, text) in enumerate(user_mapping.items()):
            ttk.Radiobutton(user_type_frame, text=text, variable=self.user_type_var, value=value).pack(side=tk.LEFT, padx=10)
    
    def setup_output_displays(self, parent):
        """
        Create output displays for recommendations.
        
        Args:
            parent (Widget): Parent widget to place displays in
        """
        # Results display frame
        output_inner = ttk.Frame(parent)
        output_inner.pack(fill=tk.X, pady=5)
        
        # Recommended Area
        ttk.Label(output_inner, text="Recommended Parking Area:", font=("Arial", 11)).grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.area_result_var = tk.StringVar(value="Not calculated")
        ttk.Label(output_inner, textvariable=self.area_result_var, font=("Arial", 11, "bold")).grid(
            row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Area Value
        ttk.Label(output_inner, text="Area Value:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.area_value_var = tk.StringVar(value="N/A")
        ttk.Label(output_inner, textvariable=self.area_value_var).grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Estimated Waiting Time
        ttk.Label(output_inner, text="Estimated Waiting Time:", font=("Arial", 11)).grid(
            row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.time_result_var = tk.StringVar(value="Not calculated")
        ttk.Label(output_inner, textvariable=self.time_result_var, font=("Arial", 11, "bold")).grid(
            row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Time Value
        ttk.Label(output_inner, text="Time Value:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.time_value_var = tk.StringVar(value="N/A")
        ttk.Label(output_inner, textvariable=self.time_value_var).grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
    
    def setup_visualization(self, parent):
        """
        Create visualization area for membership functions.
        
        Args:
            parent (Widget): Parent widget to place visualization in
        """
        # Create tabs for different visualizations
        tab_control = ttk.Notebook(parent)
        tab_control.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.input_tab = ttk.Frame(tab_control)
        self.output_tab = ttk.Frame(tab_control)
        
        tab_control.add(self.input_tab, text="Input Variables")
        tab_control.add(self.output_tab, text="Output Variables")
        
        # Create dropdown for selecting input variable to visualize
        input_select_frame = ttk.Frame(self.input_tab)
        input_select_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_select_frame, text="Select Input Variable:").pack(side=tk.LEFT, padx=5)
        
        self.input_var_selector = ttk.Combobox(input_select_frame, state="readonly", width=20)
        self.input_var_selector["values"] = ["Traffic Density", "Time of Day", "Weather Condition", 
                                           "Vacancy Rate", "User Type"]
        self.input_var_selector.current(0)  # Default to Traffic Density
        self.input_var_selector.pack(side=tk.LEFT, padx=5)
        self.input_var_selector.bind("<<ComboboxSelected>>", self.update_input_visualization)
        
        # Frame for the input visualization
        self.input_viz_frame = ttk.Frame(self.input_tab)
        self.input_viz_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create dropdown for selecting output variable to visualize
        output_select_frame = ttk.Frame(self.output_tab)
        output_select_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(output_select_frame, text="Select Output Variable:").pack(side=tk.LEFT, padx=5)
        
        self.output_var_selector = ttk.Combobox(output_select_frame, state="readonly", width=20)
        self.output_var_selector["values"] = ["Recommended Area", "Waiting Time"]
        self.output_var_selector.current(0)  # Default to Recommended Area
        self.output_var_selector.pack(side=tk.LEFT, padx=5)
        self.output_var_selector.bind("<<ComboboxSelected>>", self.update_output_visualization)
        
        # Frame for the output visualization
        self.output_viz_frame = ttk.Frame(self.output_tab)
        self.output_viz_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Initialize visualizations
        self.update_input_visualization()
        self.update_output_visualization()
    
    def update_time(self):
        """Update the time slider to the current time of day."""
        current_time = datetime.now()
        hour = current_time.hour
        minute = current_time.minute
        time_value = hour + (minute / 60)
        self.time_of_day_var.set(time_value)
    
    def update_weather_combo(self):
        """Update the weather condition combobox based on slider value."""
        weather_value = int(self.weather_condition_var.get())
        weather_mapping = self.parking_system.get_weather_condition_mapping()
        weather_text = weather_mapping.get(weather_value, "Unknown")
        
        # Find the index of the weather text in the combobox values
        values = self.weather_combo["values"]
        for i, value in enumerate(values):
            if value == weather_text:
                self.weather_combo.current(i)
                break
    
    def on_weather_selected(self, event):
        """
        Handle weather condition combobox selection.
        
        Args:
            event: Event object
        """
        selected_text = self.weather_combo.get()
        weather_mapping = self.parking_system.get_weather_condition_mapping()
        
        # Find the value corresponding to the selected text
        for value, text in weather_mapping.items():
            if text == selected_text:
                self.weather_condition_var.set(value)
                break
    
    def calculate_recommendation(self):
        """Calculate and display parking recommendations based on current input values."""
        try:
            self.status_var.set("Calculating recommendations...")
            self.root.update_idletasks()
            
            # Get input values
            traffic_density = self.traffic_density_var.get()
            time_of_day = self.time_of_day_var.get()
            weather_condition = self.weather_condition_var.get()
            vacancy_rate = self.vacancy_rate_var.get()
            user_type = self.user_type_var.get()
            
            # Get recommendations
            result = self.parking_system.get_recommendation(
                traffic_density, time_of_day, weather_condition, vacancy_rate, user_type
            )
            
            # Check for errors
            if "error" in result:
                messagebox.showerror("Error", result["error"])
                self.status_var.set("Error in calculation")
                return
            
            # Update output displays
            self.area_result_var.set(result["recommended_area_text"])
            self.area_value_var.set(f"{result['recommended_area_value']:.2f}")
            
            self.time_result_var.set(result["waiting_time_text"])
            self.time_value_var.set(f"{result['waiting_time_value']:.2f}")
            
            self.status_var.set("Recommendation calculated successfully")
            
        except Exception as e:
            messagebox.showerror("Calculation Error", str(e))
            self.status_var.set("Error in calculation")
    
    def update_input_visualization(self, event=None):
        """
        Update the input variable visualization based on the selected variable.
        
        Args:
            event: Event object (optional)
        """
        # Clear previous visualization
        for widget in self.input_viz_frame.winfo_children():
            widget.destroy()
        
        # Get selected variable
        selected_var = self.input_var_selector.get()
        
        # Create figure for visualization
        fig = plt.Figure(figsize=(7, 4), dpi=80)
        ax = fig.add_subplot(111)
        
        # Draw the membership functions based on selected variable
        if selected_var == "Traffic Density":
            x = np.arange(0, 101, 1)
            ax.plot(x, self.parking_system.traffic_density['Low'].mf, 'b', linewidth=1.5, label='Low')
            ax.plot(x, self.parking_system.traffic_density['Medium'].mf, 'g', linewidth=1.5, label='Medium')
            ax.plot(x, self.parking_system.traffic_density['High'].mf, 'r', linewidth=1.5, label='High')
            ax.set_title('Traffic Density Membership Functions')
            ax.set_xlabel('Traffic Density (%)')
            
        elif selected_var == "Time of Day":
            x = np.arange(0, 25, 1)
            ax.plot(x, self.parking_system.time_of_day['EarlyMorning'].mf, 'b', linewidth=1.5, label='Early Morning')
            ax.plot(x, self.parking_system.time_of_day['Morning'].mf, 'g', linewidth=1.5, label='Morning')
            ax.plot(x, self.parking_system.time_of_day['Noon'].mf, 'r', linewidth=1.5, label='Noon')
            ax.plot(x, self.parking_system.time_of_day['Afternoon'].mf, 'c', linewidth=1.5, label='Afternoon')
            ax.plot(x, self.parking_system.time_of_day['Evening'].mf, 'm', linewidth=1.5, label='Evening')
            ax.plot(x, self.parking_system.time_of_day['Night'].mf, 'y', linewidth=1.5, label='Night')
            ax.set_title('Time of Day Membership Functions')
            ax.set_xlabel('Hour of Day (0-24)')
            
        elif selected_var == "Weather Condition":
            x = np.arange(0, 11, 1)
            ax.plot(x, self.parking_system.weather_condition['Clear'].mf, 'b', linewidth=1.5, label='Clear')
            ax.plot(x, self.parking_system.weather_condition['LightRain'].mf, 'g', linewidth=1.5, label='Light Rain')
            ax.plot(x, self.parking_system.weather_condition['HeavyRain'].mf, 'r', linewidth=1.5, label='Heavy Rain')
            ax.plot(x, self.parking_system.weather_condition['Snow'].mf, 'c', linewidth=1.5, label='Snow')
            ax.set_title('Weather Condition Membership Functions')
            ax.set_xlabel('Weather Condition (0-10)')
            
        elif selected_var == "Vacancy Rate":
            x = np.arange(0, 101, 1)
            ax.plot(x, self.parking_system.vacancy_rate['VeryLow'].mf, 'b', linewidth=1.5, label='Very Low')
            ax.plot(x, self.parking_system.vacancy_rate['Low'].mf, 'g', linewidth=1.5, label='Low')
            ax.plot(x, self.parking_system.vacancy_rate['Medium'].mf, 'r', linewidth=1.5, label='Medium')
            ax.plot(x, self.parking_system.vacancy_rate['High'].mf, 'c', linewidth=1.5, label='High')
            ax.plot(x, self.parking_system.vacancy_rate['VeryHigh'].mf, 'm', linewidth=1.5, label='Very High')
            ax.set_title('Vacancy Rate Membership Functions')
            ax.set_xlabel('Vacancy Rate (%)')
            
        elif selected_var == "User Type":
            x = np.arange(1, 6, 1)  # Fixed to match universe in fuzzy_parking_system.py
            ax.plot(x, self.parking_system.user_type['Regular'].mf, 'b', linewidth=1.5, label='Regular')
            ax.plot(x, self.parking_system.user_type['Member'].mf, 'g', linewidth=1.5, label='Member')
            ax.plot(x, self.parking_system.user_type['VIP'].mf, 'r', linewidth=1.5, label='VIP')
            ax.plot(x, self.parking_system.user_type['Disabled'].mf, 'c', linewidth=1.5, label='Disabled')
            ax.plot(x, self.parking_system.user_type['Staff'].mf, 'm', linewidth=1.5, label='Staff')
            ax.set_title('User Type Membership Functions')
            ax.set_xlabel('User Type (1-5)')
        
        ax.set_ylabel('Membership Value')
        ax.grid(True)
        ax.legend(loc='upper right')
        
        # Create canvas for the figure
        canvas = FigureCanvasTkAgg(fig, master=self.input_viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def update_output_visualization(self, event=None):
        """
        Update the output variable visualization based on the selected variable.
        
        Args:
            event: Event object (optional)
        """
        # Clear previous visualization
        for widget in self.output_viz_frame.winfo_children():
            widget.destroy()
        
        # Get selected variable
        selected_var = self.output_var_selector.get()
        
        # Create figure for visualization
        fig = plt.Figure(figsize=(7, 4), dpi=80)
        ax = fig.add_subplot(111)
        
        # Draw the membership functions based on selected variable
        if selected_var == "Recommended Area":
            x = np.arange(1, 6, 1)  # Fixed to match universe in fuzzy_parking_system.py
            ax.plot(x, self.parking_system.recommended_area['AreaA'].mf, 'b', linewidth=1.5, label='Area A')
            ax.plot(x, self.parking_system.recommended_area['AreaB'].mf, 'g', linewidth=1.5, label='Area B')
            ax.plot(x, self.parking_system.recommended_area['AreaC'].mf, 'r', linewidth=1.5, label='Area C')
            ax.plot(x, self.parking_system.recommended_area['AreaD'].mf, 'c', linewidth=1.5, label='Area D')
            ax.plot(x, self.parking_system.recommended_area['AreaE'].mf, 'm', linewidth=1.5, label='Area E')
            ax.set_title('Recommended Parking Area Membership Functions')
            ax.set_xlabel('Area (1-5, where 1 is closest to entrance)')
            
        elif selected_var == "Waiting Time":
            x = np.arange(0, 31, 1)
            ax.plot(x, self.parking_system.waiting_time['VeryShort'].mf, 'b', linewidth=1.5, label='Very Short')
            ax.plot(x, self.parking_system.waiting_time['Short'].mf, 'g', linewidth=1.5, label='Short')
            ax.plot(x, self.parking_system.waiting_time['Medium'].mf, 'r', linewidth=1.5, label='Medium')
            ax.plot(x, self.parking_system.waiting_time['Long'].mf, 'c', linewidth=1.5, label='Long')
            ax.plot(x, self.parking_system.waiting_time['VeryLong'].mf, 'm', linewidth=1.5, label='Very Long')
            ax.set_title('Estimated Waiting Time Membership Functions')
            ax.set_xlabel('Waiting Time (minutes)')
        
        ax.set_ylabel('Membership Value')
        ax.grid(True)
        ax.legend(loc='upper right')
        
        # Create canvas for the figure
        canvas = FigureCanvasTkAgg(fig, master=self.output_viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingGuidanceGUI(root)
    root.mainloop()