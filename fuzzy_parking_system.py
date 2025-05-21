# fuzzy_parking_system.py
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class ParkingGuidanceSystem:
    """
    A fuzzy logic-based parking guidance system that recommends optimal parking areas
    and estimates waiting times based on multiple input factors.
    """
    
    def __init__(self):
        """Initialize the fuzzy logic control system for parking guidance."""
        # Create input variables
        self.traffic_density = ctrl.Antecedent(np.arange(0, 101, 1), 'traffic_density')
        self.time_of_day = ctrl.Antecedent(np.arange(0, 25, 1), 'time_of_day')
        self.weather_condition = ctrl.Antecedent(np.arange(0, 11, 1), 'weather_condition')
        self.vacancy_rate = ctrl.Antecedent(np.arange(0, 101, 1), 'vacancy_rate')
        self.user_type = ctrl.Antecedent(np.arange(1, 6, 1), 'user_type')
        
        # Create output variables
        self.recommended_area = ctrl.Consequent(np.arange(1, 6, 1), 'recommended_area')
        self.waiting_time = ctrl.Consequent(np.arange(0, 31, 1), 'waiting_time')
        
        # Define membership functions for each input variable
        self._define_input_membership_functions()
        
        # Define membership functions for each output variable
        self._define_output_membership_functions()
        
        # Define fuzzy rules for the system
        self._define_fuzzy_rules()
        
        # Create and simulate control systems
        self._create_control_system()

    def _define_input_membership_functions(self):
        """Define membership functions for all input variables."""
        # Traffic Density membership functions
        self.traffic_density['Low'] = fuzz.trapmf(self.traffic_density.universe, [0, 0, 20, 40])
        self.traffic_density['Medium'] = fuzz.trimf(self.traffic_density.universe, [30, 50, 70])
        self.traffic_density['High'] = fuzz.trapmf(self.traffic_density.universe, [60, 80, 100, 100])
        
        # Time of Day membership functions
        self.time_of_day['EarlyMorning'] = fuzz.trapmf(self.time_of_day.universe, [0, 0, 6, 8])
        self.time_of_day['Morning'] = fuzz.trimf(self.time_of_day.universe, [7, 9, 11])
        self.time_of_day['Noon'] = fuzz.trimf(self.time_of_day.universe, [10, 12, 14])
        self.time_of_day['Afternoon'] = fuzz.trimf(self.time_of_day.universe, [13, 15, 18])
        self.time_of_day['Evening'] = fuzz.trimf(self.time_of_day.universe, [17, 19, 22])
        self.time_of_day['Night'] = fuzz.trapmf(self.time_of_day.universe, [21, 23, 24, 24])
        
        # Weather Condition membership functions
        self.weather_condition['Clear'] = fuzz.trapmf(self.weather_condition.universe, [0, 0, 2, 3])
        self.weather_condition['LightRain'] = fuzz.trimf(self.weather_condition.universe, [2, 4, 6])
        self.weather_condition['HeavyRain'] = fuzz.trimf(self.weather_condition.universe, [5, 7, 9])
        self.weather_condition['Snow'] = fuzz.trapmf(self.weather_condition.universe, [8, 9, 10, 10])
        
        # Vacancy Rate membership functions
        self.vacancy_rate['VeryLow'] = fuzz.trapmf(self.vacancy_rate.universe, [0, 0, 10, 20])
        self.vacancy_rate['Low'] = fuzz.trimf(self.vacancy_rate.universe, [15, 25, 35])
        self.vacancy_rate['Medium'] = fuzz.trimf(self.vacancy_rate.universe, [30, 50, 70])
        self.vacancy_rate['High'] = fuzz.trimf(self.vacancy_rate.universe, [60, 75, 90])
        self.vacancy_rate['VeryHigh'] = fuzz.trapmf(self.vacancy_rate.universe, [85, 95, 100, 100])
        
        # User Type membership functions
        self.user_type['Regular'] = fuzz.trimf(self.user_type.universe, [1, 1, 2])
        self.user_type['Member'] = fuzz.trimf(self.user_type.universe, [1, 2, 3])
        self.user_type['VIP'] = fuzz.trimf(self.user_type.universe, [2, 3, 4])
        self.user_type['Disabled'] = fuzz.trimf(self.user_type.universe, [3, 4, 5])
        self.user_type['Staff'] = fuzz.trimf(self.user_type.universe, [4, 5, 5])
    
    def _define_output_membership_functions(self):
        """Define membership functions for all output variables."""
        # Recommended Parking Area membership functions
        self.recommended_area['AreaA'] = fuzz.trimf(self.recommended_area.universe, [1, 1, 2])
        self.recommended_area['AreaB'] = fuzz.trimf(self.recommended_area.universe, [1, 2, 3])
        self.recommended_area['AreaC'] = fuzz.trimf(self.recommended_area.universe, [2, 3, 4])
        self.recommended_area['AreaD'] = fuzz.trimf(self.recommended_area.universe, [3, 4, 5])
        self.recommended_area['AreaE'] = fuzz.trimf(self.recommended_area.universe, [4, 5, 5])
        
        # Estimated Waiting Time membership functions
        self.waiting_time['VeryShort'] = fuzz.trapmf(self.waiting_time.universe, [0, 0, 2, 5])
        self.waiting_time['Short'] = fuzz.trimf(self.waiting_time.universe, [3, 7, 11])
        self.waiting_time['Medium'] = fuzz.trimf(self.waiting_time.universe, [9, 13, 17])
        self.waiting_time['Long'] = fuzz.trimf(self.waiting_time.universe, [15, 20, 25])
        self.waiting_time['VeryLong'] = fuzz.trapmf(self.waiting_time.universe, [23, 28, 30, 30])
    
    def _define_fuzzy_rules(self):
        """Define fuzzy rules for the control system."""
        # Create empty rules list
        self.rules = []
        
        # Rules for Recommended Parking Area
        self.rules.append(ctrl.Rule(self.vacancy_rate['VeryHigh'], self.recommended_area['AreaA']))
        self.rules.append(ctrl.Rule(self.vacancy_rate['High'] & self.user_type['Regular'], self.recommended_area['AreaB']))
        self.rules.append(ctrl.Rule(self.vacancy_rate['High'] & ~self.user_type['Regular'], self.recommended_area['AreaA']))
        self.rules.append(ctrl.Rule(self.vacancy_rate['Medium'] & self.user_type['Regular'], self.recommended_area['AreaC']))
        self.rules.append(ctrl.Rule(self.vacancy_rate['Medium'] & self.user_type['Member'], self.recommended_area['AreaB']))
        self.rules.append(ctrl.Rule(self.vacancy_rate['Medium'] & (self.user_type['VIP'] | self.user_type['Disabled'] | self.user_type['Staff']), self.recommended_area['AreaA']))
        self.rules.append(ctrl.Rule(self.vacancy_rate['Low'] & self.user_type['Regular'], self.recommended_area['AreaD']))
        self.rules.append(ctrl.Rule(self.vacancy_rate['Low'] & self.user_type['Member'], self.recommended_area['AreaC']))
        self.rules.append(ctrl.Rule(self.vacancy_rate['Low'] & self.user_type['VIP'], self.recommended_area['AreaB']))
        self.rules.append(ctrl.Rule(self.vacancy_rate['Low'] & (self.user_type['Disabled'] | self.user_type['Staff']), self.recommended_area['AreaA']))
        self.rules.append(ctrl.Rule(self.vacancy_rate['VeryLow'] & (self.user_type['Regular'] | self.user_type['Member']), self.recommended_area['AreaE']))
        self.rules.append(ctrl.Rule(self.vacancy_rate['VeryLow'] & self.user_type['VIP'], self.recommended_area['AreaD']))
        self.rules.append(ctrl.Rule(self.vacancy_rate['VeryLow'] & (self.user_type['Disabled'] | self.user_type['Staff']), self.recommended_area['AreaC']))
        self.rules.append(ctrl.Rule(self.weather_condition['Snow'] & self.user_type['Disabled'], self.recommended_area['AreaA']))
        self.rules.append(ctrl.Rule(self.weather_condition['HeavyRain'] & self.user_type['Disabled'], self.recommended_area['AreaA']))
        
        # Rules for Estimated Waiting Time
        self.rules.append(ctrl.Rule(self.traffic_density['Low'] & self.vacancy_rate['VeryHigh'], self.waiting_time['VeryShort']))
        self.rules.append(ctrl.Rule(self.traffic_density['Low'] & self.vacancy_rate['High'], self.waiting_time['VeryShort']))
        self.rules.append(ctrl.Rule(self.traffic_density['Low'] & self.vacancy_rate['Medium'], self.waiting_time['Short']))
        self.rules.append(ctrl.Rule(self.traffic_density['Low'] & self.vacancy_rate['Low'], self.waiting_time['Medium']))
        self.rules.append(ctrl.Rule(self.traffic_density['Low'] & self.vacancy_rate['VeryLow'], self.waiting_time['Long']))
        self.rules.append(ctrl.Rule(self.traffic_density['Medium'] & self.vacancy_rate['VeryHigh'], self.waiting_time['Short']))
        self.rules.append(ctrl.Rule(self.traffic_density['Medium'] & self.vacancy_rate['High'], self.waiting_time['Short']))
        self.rules.append(ctrl.Rule(self.traffic_density['Medium'] & self.vacancy_rate['Medium'], self.waiting_time['Medium']))
        self.rules.append(ctrl.Rule(self.traffic_density['Medium'] & self.vacancy_rate['Low'], self.waiting_time['Long']))
        self.rules.append(ctrl.Rule(self.traffic_density['Medium'] & self.vacancy_rate['VeryLow'], self.waiting_time['VeryLong']))
        self.rules.append(ctrl.Rule(self.traffic_density['High'] & self.vacancy_rate['VeryHigh'], self.waiting_time['Medium']))
        self.rules.append(ctrl.Rule(self.traffic_density['High'] & self.vacancy_rate['High'], self.waiting_time['Medium']))
        self.rules.append(ctrl.Rule(self.traffic_density['High'] & self.vacancy_rate['Medium'], self.waiting_time['Long']))
        self.rules.append(ctrl.Rule(self.traffic_density['High'] & self.vacancy_rate['Low'], self.waiting_time['VeryLong']))
        self.rules.append(ctrl.Rule(self.traffic_density['High'] & self.vacancy_rate['VeryLow'], self.waiting_time['VeryLong']))
        self.rules.append(ctrl.Rule((self.time_of_day['Morning'] | self.time_of_day['Afternoon']) & self.traffic_density['High'], self.waiting_time['VeryLong']))
        self.rules.append(ctrl.Rule(self.weather_condition['HeavyRain'] | self.weather_condition['Snow'], self.waiting_time['Long']))
        self.rules.append(ctrl.Rule(self.time_of_day['Night'] & ~self.vacancy_rate['VeryLow'], self.waiting_time['VeryShort']))
        
        # Time-based rules
        self.rules.append(ctrl.Rule(self.time_of_day['Morning'] & (self.vacancy_rate['High'] | self.vacancy_rate['VeryHigh']), self.recommended_area['AreaA']))
        self.rules.append(ctrl.Rule(self.time_of_day['Evening'] & self.traffic_density['High'], self.waiting_time['VeryLong']))
        self.rules.append(ctrl.Rule(self.time_of_day['Night'], self.recommended_area['AreaA']))
    
    def _create_control_system(self):
        """Create the fuzzy control system."""
        self.area_control = ctrl.ControlSystem(self.rules)
        self.area_simulation = ctrl.ControlSystemSimulation(self.area_control)
    
    def get_recommendation(self, traffic_density_val, time_of_day_val, weather_condition_val, vacancy_rate_val, user_type_val):
        """
        Get parking recommendations based on input values.
        
        Args:
            traffic_density_val (float): Traffic density value (0-100%)
            time_of_day_val (float): Time of day value (0-24 hours)
            weather_condition_val (float): Weather condition value (0-10)
            vacancy_rate_val (float): Vacancy rate value (0-100%)
            user_type_val (int): User type value (1-5)
            
        Returns:
            dict: Recommendation results containing area and waiting time values and text descriptions
        """
        try:
            # Input validation
            if not (0 <= traffic_density_val <= 100):
                return {"error": "Traffic density must be between 0 and 100%"}
            if not (0 <= time_of_day_val <= 24):
                return {"error": "Time of day must be between 0 and 24 hours"}
            if not (0 <= weather_condition_val <= 10):
                return {"error": "Weather condition must be between 0 and 10"}
            if not (0 <= vacancy_rate_val <= 100):
                return {"error": "Vacancy rate must be between 0 and 100%"}
            if not (1 <= user_type_val <= 5):
                return {"error": "User type must be between 1 and 5"}
                
            # Set input values
            self.area_simulation.input['traffic_density'] = traffic_density_val
            self.area_simulation.input['time_of_day'] = time_of_day_val
            self.area_simulation.input['weather_condition'] = weather_condition_val
            self.area_simulation.input['vacancy_rate'] = vacancy_rate_val
            self.area_simulation.input['user_type'] = user_type_val
            
            # Compute the result
            self.area_simulation.compute()
            
            # Get the output values
            recommended_area_val = self.area_simulation.output['recommended_area']
            waiting_time_val = self.area_simulation.output['waiting_time']
            
            # Convert numeric values to text descriptions
            recommended_area_text = self._get_area_text(recommended_area_val)
            waiting_time_text = self._get_waiting_time_text(waiting_time_val)
            
            return {
                'recommended_area_value': recommended_area_val,
                'recommended_area_text': recommended_area_text,
                'waiting_time_value': waiting_time_val,
                'waiting_time_text': waiting_time_text
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _get_area_text(self, area_value):
        """
        Convert the numeric area value to a text description.
        
        Args:
            area_value (float): Numeric area value
            
        Returns:
            str: Text description of the area
        """
        if area_value < 1.5:
            return "Area A (Closest to entrance)"
        elif area_value < 2.5:
            return "Area B"
        elif area_value < 3.5:
            return "Area C"
        elif area_value < 4.5:
            return "Area D"
        else:
            return "Area E (Farthest from entrance)"
    
    def _get_waiting_time_text(self, time_value):
        """
        Convert the numeric waiting time to a text description.
        
        Args:
            time_value (float): Numeric time value
            
        Returns:
            str: Text description of the waiting time
        """
        if time_value < 3:
            return "Very Short (< 3 minutes)"
        elif time_value < 9:
            return "Short (3-9 minutes)"
        elif time_value < 15:
            return "Medium (9-15 minutes)"
        elif time_value < 23:
            return "Long (15-23 minutes)"
        else:
            return "Very Long (>23 minutes)"
    
    def get_user_type_mapping(self):
        """
        Get mapping for user type values to descriptions
        
        Returns:
            dict: Dictionary mapping user type values to descriptions
        """
        return {
            1: "Regular",
            2: "Member",
            3: "VIP",
            4: "Disabled",
            5: "Staff"
        }
    
    def get_weather_condition_mapping(self):
        """
        Get mapping for weather condition values to descriptions
        
        Returns:
            dict: Dictionary mapping weather condition values to descriptions
        """
        return {
            0: "Clear (0)",
            1: "Clear (1)",
            2: "Clear (2)",
            3: "Light Rain (3)",
            4: "Light Rain (4)",
            5: "Light Rain (5)",
            6: "Heavy Rain (6)",
            7: "Heavy Rain (7)",
            8: "Heavy Rain (8)",
            9: "Snow (9)",
            10: "Snow (10)"
        }