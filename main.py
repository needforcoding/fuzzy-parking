# main.py
import tkinter as tk
from fuzzy_parking_gui import ParkingGuidanceGUI

def main():
    """
    Main function to run the Fuzzy Logic Parking Guidance System.
    """
    # Create the main tkinter window
    root = tk.Tk()
    
    # Initialize the GUI application
    app = ParkingGuidanceGUI(root)
    
    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()