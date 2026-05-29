import pandas as pd
import numpy as np
import os
import time
from pathlib import Path

# --- Configuration & Standards ---
# Based on WHO/EPA standards for Water Quality Index calculation
WATER_STANDARDS = {
    'PH':   {'ideal': 7.0, 'std': 8.5, 'w': 0.117},
    'Ec':   {'ideal': 0.0, 'std': 1000, 'w': 0.117},
    'TDS':  {'ideal': 0.0, 'std': 500,  'w': 0.117},
    'Na':   {'ideal': 0.0, 'std': 200,  'w': 0.117},
    'Cl':   {'ideal': 0.0, 'std': 250,  'w': 0.117},
    'SO4':  {'ideal': 0.0, 'std': 250,  'w': 0.117},
    'HCO3': {'ideal': 0.0, 'std': 120,  'w': 0.117},
    'Ca':   {'ideal': 0.0, 'std': 75,   'w': 0.080},
    'Mg':   {'ideal': 0.0, 'std': 30,   'w': 0.080}
}

def calculate_qi(parameter, value, ideal, standard):
    """Calculates Quality Rating (Qi) for a specific water parameter."""
    try:
        if parameter.upper() == 'PH':
            return ((value - 7) / (standard - 7)) * 100
        return ((value - ideal) / (standard - ideal)) * 100
    except ZeroDivisionError:
        return 0

def get_wqi_status(wqi_value):
    """Classifies water quality based on calculated WQI value."""
    if wqi_value < 25: return "Excellent"
    if 25 <= wqi_value < 50: return "Good"
    if 50 <= wqi_value < 75: return "Poor"
    if 75 <= wqi_value < 100: return "Very Poor"
    return "Unsuitable"

def safe_save_excel(df, output_path):
    """Attempts to save the Excel file, handles PermissionError if file is open."""
    attempts = 3
    for i in range(attempts):
        try:
            df.to_excel(output_path, index=False)
            print(f"Successfully saved to: {output_path.name}")
            return True
        except PermissionError:
            if i < attempts - 1:
                print(f"Retrying save for {output_path.name} (File might be open)...")
                time.sleep(2)
            else:
                alternative_path = output_path.parent / f"NEW_{output_path.name}"
                df.to_excel(alternative_path, index=False)
                print(f"Saved to alternative path: {alternative_path.name}")
    return False

def run_wqi_pipeline():
    # Path Setup
    base_path = Path(__file__).parent
    data_dir = base_path / "data"
    output_dir = base_path / "output"
    output_dir.mkdir(exist_ok=True)

    # Automatically find all annual cleaned excel files
    station_files = list(data_dir.glob("annual_cleaned_*.xlsx"))
    
    if not station_files:
        print("No input files found in /data directory. Please check file naming.")
        return

    for file_path in station_files:
        print(f"Analyzing: {file_path.name}")
        df = pd.read_excel(file_path)
        
        wqi_results = []
        for _, row in df.iterrows():
            weighted_qi_sum = 0
            total_weights = 0
            
            for param, std_values in WATER_STANDARDS.items():
                if param in df.columns:
                    qi = calculate_qi(param, row[param], std_values['ideal'], std_values['std'])
                    weighted_qi_sum += qi * std_values['w']
                    total_weights += std_values['w']
            
            wqi_val = weighted_qi_sum / total_weights if total_weights > 0 else np.nan
            wqi_results.append(wqi_val)

        df['WQI'] = wqi_results
        df['WQI_Status'] = df['WQI'].apply(get_wqi_status)

        # Output Naming
        station_name = file_path.stem.replace("annual_cleaned_", "")
        output_file = output_dir / f"WQI_Results_{station_name}.xlsx"
        safe_save_excel(df, output_file)

if __name__ == "__main__":
    print("Starting Water Quality Index (WQI) Analysis...")
    run_wqi_pipeline()
    print("Process Completed.")
