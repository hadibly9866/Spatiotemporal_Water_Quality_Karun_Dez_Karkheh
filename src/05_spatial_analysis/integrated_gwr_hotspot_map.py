import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path
import contextily as cx # برای افزودن نقشه پایه (OpenStreetMap)

def generate_final_integrated_map():
    # --- پیکربندی مسیرها ---
    base_dir = Path(__file__).parent
    data_dir = base_dir / "data"
    output_dir = base_dir / "output" / "final_visualizations"
    output_dir.mkdir(parents=True, exist_ok=True)

    # --- بارگذاری داده‌های خروجی مراحل قبل ---
    # فرض بر این است که نتایج GWR و Hotspot را در یک فایل یا فایل‌های مجزا ذخیره کرده‌اید
    gwr_results_path = data_dir / "gwr_model_outputs.csv"
    hotspot_results_path = data_dir / "spatial_hotspot_results.csv"
    
    if not gwr_results_path.exists() or not hotspot_results_path.exists():
        print("Error: Required result files from Step 19 or GWR analysis not found.")
        return

    # بارگذاری و ترکیب داده‌ها
    gwr_df = pd.read_csv(gwr_results_path)
    hotspot_df = pd.read_csv(hotspot_results_path)
    
    # ادغام بر اساس نام ایستگاه (Station Name)
    combined_df = pd.merge(gwr_df, hotspot_df, on='Station')

    # تبدیل به داده مکانی (GeoDataFrame) - فرض بر مختصات UTM یا WGS84
    gdf = gpd.GeoDataFrame(
        combined_df, 
        geometry=gpd.points_from_xy(combined_df['Longitude'], combined_df['Latitude']),
        crs="EPSG:4326"
    )

    # --- ترسیم نقشه ترکیبی نهایی ---
    fig, ax = plt.subplots(1, 1, figsize=(12, 10), dpi=300)

    # ۱. نمایش قدرت مدل GWR (Local R2) با طیف رنگی
    # نقاطی که مدل در آنجا بهتر عمل کرده بزرگتر یا پررنگ‌تر دیده می‌شوند
    plot = gdf.plot(column='Local_R2', 
                    ax=ax, 
                    cmap='YlOrRd', 
                    legend=True, 
                    markersize=100,
                    legend_kwds={'label': "Local $R^2$ (Model Performance)"},
                    edgecolor='black',
                    alpha=0.8)

    # ۲. مشخص کردن نقاط Hotspot با علائم خاص (مثلاً ستاره یا ضربدر)
    # فرض بر این است که ستون Cluster_Type مقادیر 'Hotspot' یا 'Coldspot' دارد
    hotspots = gdf[gdf['Cluster_Type'] == 'Hotspot']
    hotspots.plot(ax=ax, marker='*', color='blue', markersize=150, label='Hotspot (High EC/WQI)')

    # افزودن نقشه پایه (اختیاری - نیاز به اینترنت دارد)
    try:
        cx.add_basemap(ax, crs=gdf.crs.to_string(), source=cx.providers.OpenStreetMap.Mapnik, alpha=0.5)
    except:
        print("Note: Basemap could not be loaded, plotting without background.")

    # --- شخصی‌سازی نهایی ---
    ax.set_title("Integrated Spatial Map: GWR Performance & Hotspot Locations", fontsize=15, fontweight='bold')
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    plt.legend(loc='lower right')

    # ذخیره فایل برای مقاله
    final_map_file = output_dir / "Figure_Final_Integrated_Spatial_Analysis.png"
    plt.savefig(final_map_file, bbox_inches='tight')
    print(f"✅ Final integrated map saved to: {final_map_file}")
    plt.show()

if __name__ == "__main__":
    generate_final_integrated_map()
