import os
import pandas as pd
import numpy as np

# 1. Path Configuration
# Set directories relative to the script location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 2. Station Configuration
# Map station names to their corresponding CSV files in the data folder
stations = {
    'Ahvaz': 'Ahvaz.csv',
    'Dezful': 'Dezful.csv',
    # Add other stations here as needed
}

def run_analysis():
    print("Starting Mann-Kendall and WQI analysis...")
    
    # 3. Processing
    results_list = []
    
    for station_name, file_name in stations.items():
        file_path = os.path.join(DATA_DIR, file_name)
        
        if not os.path.exists(file_path):
            print(f"Warning: File not found for station {station_name} at {file_path}. Skipping.")
            continue
            
        print(f"Processing station: {station_name}")
        # Add your specific Mann-Kendall / WQI logic here...
        # Example placeholder:
        # data = pd.read_csv(file_path)
        # result = perform_calculations(data)
        # results_list.append(result)

    # 4. Save Results
    output_path = os.path.join(OUTPUT_DIR, 'Mann_Kendall_Results.xlsx')
    
    try:
        # Assuming 'results_list' is populated with DataFrames
        if results_list:
            final_df = pd.concat(results_list)
            final_df.to_excel(output_path, index=False)
            print(f"Success: Results saved to {output_path}")
        else:
            print("Error: No data to save.")
            
    except PermissionError:
        # Handle cases where the file might be open in Excel
        backup_path = os.path.join(OUTPUT_DIR, 'Mann_Kendall_Results_backup.xlsx')
        print(f"Warning: Could not save file (file might be open). Saving as backup: {backup_path}")
        final_df.to_excel(backup_path, index=False)

if __name__ == "__main__":
    run_analysis()
