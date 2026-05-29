import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from libpysal.weights import KNN
from esda.moran import Moran
from splot.esda import moran_scatterplot

def perform_spatial_analysis():
    # --- تنظیمات مسیرها ---
    base_dir = Path(__file__).parent
    input_file = base_dir / "data" / "spatial_station_data.xlsx" # تغییر نام برای نظم بیشتر
    output_dir = base_dir / "output" / "spatial_statistics"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_file.exists():
        print(f"Error: Input file '{input_file.name}' not found in 'data' folder.")
        return

    # --- بارگذاری داده‌ها ---
    try:
        df = pd.read_excel(input_file)
        # استخراج مختصات UTM و متغیر هدف (مثلاً EC یا WQI)
        coords = df[['UTM X (m)', 'UTM N (m)']].values
        variable = df['EC_mean'].values # متغیر مورد نظر برای تحلیل موران
    except KeyError as e:
        print(f"Error: Missing column in Excel: {e}")
        return

    # --- ۱. ایجاد ماتریس وزن‌های مکانی (Spatial Weights) ---
    # استفاده از ۳ همسایه نزدیک (KNN) - مناسب برای تعداد ایستگاه‌های کم
    k_neighbors = 3
    if len(df) <= k_neighbors:
        k_neighbors = len(df) - 1
        
    w = KNN.from_array(coords, k=k_neighbors)
    w.transform = 'R' # استانداردسازی سطری (Row-standardized)

    # --- ۲. محاسبه شاخص موران (Moran's I) ---
    mi = Moran(variable, w)

    # چاپ نتایج در کنسول برای استفاده در متن مقاله
    print("-" * 30)
    print(f"📊 Global Moran's I Results for EC:")
    print(f"Moran's I Statistic: {mi.I:.4f}")
    print(f"Expected I: {mi.EI:.4f}")
    print(f"P-value: {mi.p_sim:.4f}")
    print(f"Z-score: {mi.z_sim:.4f}")
    
    # تفسیر نتیجه
    if mi.p_sim < 0.05:
        if mi.I > mi.EI:
            print("Conclusion: Spatial Clustering Detected (Significant)")
        else:
            print("Conclusion: Spatial Dispersion Detected (Significant)")
    else:
        print("Conclusion: Spatial Distribution is Random (Not Significant)")
    print("-" * 30)

    # --- ۳. بصری‌سازی (Moran Scatterplot) ---
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    moran_scatterplot(mi, ax=ax, p=0.05) # نقاط معنادار را مشخص می‌کند
    
    ax.set_title(f"Moran Scatterplot (I = {mi.I:.3f})", fontsize=14, fontweight='bold')
    ax.set_xlabel('Normalized EC Value', fontsize=12)
    ax.set_ylabel('Spatial Lag of EC', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)

    # ذخیره نمودار
    plt.tight_layout()
    output_plot = output_dir / "moran_scatterplot_EC.png"
    plt.savefig(output_plot)
    print(f"Saved scatterplot to: {output_plot}")

    # --- ۴. ذخیره نتایج در فایل متنی ---
    with open(output_dir / "moran_results_summary.txt", "w") as f:
        f.write(f"Global Moran's I Analysis\n")
        f.write(f"Variable: EC_mean\n")
        f.write(f"Moran's I: {mi.I}\n")
        f.write(f"P-value: {mi.p_sim}\n")
        f.write(f"Z-score: {mi.z_sim}\n")

if __name__ == "__main__":
    perform_spatial_analysis()
