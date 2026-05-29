import pandas as pd
import os

# 1. Path Configuration
# Directories are set relative to the script location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

# Ensure directories exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 2. Station Configuration
# Define station coordinates and their mapping to Excel files
# Ensure these files exist in the 'data' directory
station_info = {
    'Ahvaz': {'lat': 31.33, 'lon': 48.67, 'file': 'Ahvaz.xlsx'},
    'Malathani': {'lat': 31.65, 'lon': 48.83, 'file': 'Malathani.xlsx'},
    'Farsiat': {'lat': 31.15, 'lon': 48.65, 'file': 'Farsiat.xlsx'},
    'Dezful': {'lat': 32.38, 'lon': 48.40, 'file': 'Dezful.xlsx'},
    'Hamidieh': {'lat': 31.48, 'lon': 48.07, 'file': 'Hamidieh.xlsx'},
    'Pa-ye Pol': {'lat': 32.22, 'lon': 48.38, 'file': 'Pa_ye_Pol.xlsx'}
}

def merge_data():
    print("Loading environmental indices (LST and NDVI)...")
    
    # Load annual indices
    lst_df = pd.read_csv(os.path.join(DATA_DIR, 'LST_Annual.csv'))
    ndvi_df = pd.read_csv(os.path.join(DATA_DIR, 'NDVI_Annual.csv'))
    
    # Merge LST and NDVI on Year
    environmental_data = pd.merge(lst_df, ndvi_df, on='Year')
    
    merged_results = []

    print("Processing individual stations...")
    for station_name, info in station_info.items():
        file_path = os.path.join(DATA_DIR, info['file'])
        
        if os.path.exists(file_path):
            # Load EC data for the station
            station_df = pd.read_excel(file_path)
            
            # Merge with environmental data
            station_df = pd.merge(station_df, environmental_data, on='Year')
            
            # Add spatial coordinates
            station_df['Station'] = station_name
            station_df['Latitude'] = info['lat']
            station_df['Longitude'] = info['lon']
            
            merged_results.append(station_df)
            print(f" - Processed: {station_name}")
        else:
            print(f" - Warning: File for {station_name} not found at {file_path}")

    # 3. Concatenate and Save
    if merged_results:
        final_df = pd.concat(merged_results, ignore_index=True)
        output_file = os.path.join(OUTPUT_DIR, 'Merged_Data_2000_2020.csv')
        
        final_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"Success: Data merged and saved to {output_file}")
    else:
        print("Error: No data processed.")

if __name__ == "__main__":
    merge_data()
