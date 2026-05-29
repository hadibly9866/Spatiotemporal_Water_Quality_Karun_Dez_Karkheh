import pandas as pd
import numpy as np
import os
from mgwr.gwr import GWR
from mgwr.sel_bw import Sel_BW
from sklearn.metrics import mean_squared_error

# 1. Path Configuration
# Set the project base directory and data/output paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Define input file path
input_file = os.path.join(DATA_DIR, 'Merged_Data_2000_2020.csv')

print(f"Loading data from: {input_file}")

# 2. Data Loading and Preprocessing
data = pd.read_csv(input_file)

# Drop missing values in critical columns
required_cols = ['EC', 'LST', 'NDVI', 'Longitude', 'Latitude']
data = data.dropna(subset=required_cols)

# Define variables
y = data['EC'].values.reshape((-1, 1))
X = data[['LST', 'NDVI']].values
coords = list(zip(data['Longitude'], data['Latitude']))

# Standardization of independent variables (Optional, recommended for GWR)
X = (X - X.mean(axis=0)) / X.std(axis=0)
y = (y - y.mean()) / y.std()

# 3. Bandwidth Selection and GWR Execution
print("Selecting optimal bandwidth...")
selector = Sel_BW(coords, y, X, kernel='bisquare', fixed=False)
bw = selector.search(criterion='AICc')
print(f"Optimal Bandwidth: {bw}")

model = GWR(coords, y, X, bw, kernel='bisquare', fixed=False)
results = model.fit()

# 4. Extracting Local Results
data['Local_R2'] = results.localR2
data['Residuals'] = results.resid_response
data['Intercept'] = results.params[:, 0]
data['Coeff_LST'] = results.params[:, 1]
data['Coeff_NDVI'] = results.params[:, 2]

# 5. Statistical Analysis by Station
def calculate_rmse(group):
    """Calculate RMSE for each station group."""
    return np.sqrt(mean_squared_error(group['EC'], group['EC'] - group['Residuals']))

station_summary = data.groupby('Station').agg({
    'Local_R2': 'mean',
    'Intercept': 'mean',
    'Coeff_LST': 'mean',
    'Coeff_NDVI': 'mean',
    'Latitude': 'first',
    'Longitude': 'first'
}).reset_index()

# Calculate and add RMSE to the summary
rmse_per_station = data.groupby('Station').apply(calculate_rmse)
station_summary['RMSE'] = station_summary['Station'].map(rmse_per_station)

# 6. Saving Results
summary_output = os.path.join(OUTPUT_DIR, 'GWR_Station_Summary.csv')
full_results_output = os.path.join(OUTPUT_DIR, 'GWR_Full_Results.csv')

station_summary.to_csv(summary_output, index=False)
data.to_csv(full_results_output, index=False)

# Optional: Save Excel versions
station_summary.to_excel(summary_output.replace('.csv', '.xlsx'), index=False)
data.to_excel(full_results_output.replace('.csv', '.xlsx'), index=False)

print(f"Analysis complete. Results successfully saved in: {OUTPUT_DIR}")
