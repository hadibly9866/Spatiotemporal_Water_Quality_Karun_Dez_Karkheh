import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

def calculate_sens_slope(data):
    """Calculates Sen's Slope for a given time series."""
    n = len(data)
    slopes = []
    for i in range(n):
        for j in range(i + 1, n):
            slopes.append((data[j] - data[i]) / (j - i))
    return np.median(slopes)

def plot_water_quality_trends():
    # Setup Paths
    base_dir = Path(__file__).parent
    input_file = base_dir / "data" / "Ec_6_Station.xlsx" # Adjusted filename
    output_dir = base_dir / "output" / "trend_plots"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_file.exists():
        print(f"Error: Input file {input_file} not found.")
        return

    # Load Data
    df = pd.read_excel(input_file)
    stations = ['Ahvaz', 'Bamdezh', 'Gotvand', 'Harmaleh', 'Payepol', 'Pol_e_Shalo']
    years = np.arange(2000, 2024)

    # Visualization Setup
    plt.rcParams["font.family"] = "serif" # Standard for academic papers
    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(15, 18), dpi=300)
    axes = axes.flatten()

    for i, station in enumerate(stations):
        if station not in df.columns:
            continue
            
        data = df[station].values
        ax = axes[i]

        # 1. Plot Original Data
        ax.plot(years, data, marker='o', linestyle='-', color='teal', label=f'{station} EC/WQI')

        # 2. Calculate and Plot Trend Line
        z = np.polyfit(years, data, 1)
        p = np.poly1d(z)
        ax.plot(years, p(years), "r--", alpha=0.8, label='Linear Trend')

        # 3. Calculate Sen's Slope
        slope = calculate_sens_slope(data)
        
        # 4. Moving Average (3-Year)
        moving_avg = pd.Series(data).rolling(window=3, min_periods=1).mean()
        ax.plot(years, moving_avg, color='orange', linewidth=2, label='3-Year Moving Avg')

        # Formatting
        ax.set_title(f"Station: {station}", fontsize=14, fontweight='bold')
        ax.set_xlabel("Year", fontsize=12)
        ax.set_ylabel("Value", fontsize=12)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend(loc='upper left', fontsize=10)
        
        # Annotate Sen's Slope
        ax.text(0.05, 0.95, f"Sen's Slope: {slope:.2f}", transform=ax.transAxes, 
                fontsize=11, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))

    plt.tight_layout()
    plot_path = output_dir / "combined_trends_analysis.png"
    plt.savefig(plot_path)
    print(f"Trend visualization saved to: {plot_path}")
    plt.show()

if __name__ == "__main__":
    plot_water_quality_trends()
