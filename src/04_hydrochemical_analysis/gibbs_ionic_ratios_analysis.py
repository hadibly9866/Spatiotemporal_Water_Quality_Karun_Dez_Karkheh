import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

def analyze_hydrochemistry():
    # --- تنظیمات مسیرها (Path Setup) ---
    base_dir = Path(__file__).parent
    input_file = base_dir / "data" / "Gibbs_IonicRatios_Ready.xlsx"
    output_dir = base_dir / "output" / "hydrochemistry"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_file.exists():
        print(f"Error: Input file '{input_file.name}' not found in 'data' folder.")
        return

    # --- بارگذاری داده‌ها ---
    try:
        df = pd.read_excel(input_file)
        # اطمینان از وجود ستون ایستگاه برای رنگ‌بندی
        if 'Station' not in df.columns:
            df['Station'] = 'Unknown' 
    except Exception as e:
        print(f"Error loading Excel: {e}")
        return

    # --- ۱. محاسبات نسبت‌های یونی و گیبس ---
    # Gibbs Ratios
    df['Gibbs_Cations'] = (df['Na'] + df['K']) / (df['Na'] + df['K'] + df['Ca'])
    df['Gibbs_Anions'] = df['Cl'] / (df['Cl'] + df['HCO3'])
    
    # Key Ionic Ratios
    df['Na_Cl_Ratio'] = df['Na'] / df['Cl']
    df['Ca_SO4_Ratio'] = df['Ca'] / df['SO4']
    df['Mg_Ca_Ratio'] = df['Mg'] / df['Ca']

    # --- ۲. تنظیمات گرافیکی ---
    plt.rcParams["font.family"] = "serif"
    stations = df['Station'].unique()
    colors = plt.cm.get_cmap('tab10', len(stations))
    markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'h']

    # --- ۳. ترسیم نمودارهای گیبس (Gibbs Diagrams) ---
    plots_config = [
        {'x': 'Gibbs_Cations', 'title': 'Gibbs Diagram (Cations)', 'xlabel': '(Na + K) / (Na + K + Ca)', 'filename': 'Gibbs_Cations.png'},
        {'x': 'Gibbs_Anions', 'title': 'Gibbs Diagram (Anions)', 'xlabel': 'Cl / (Cl + HCO3)', 'filename': 'Gibbs_Anions.png'}
    ]

    for config in plots_config:
        fig, ax = plt.subplots(figsize=(8, 10), dpi=300)
        
        # رسم داده‌ها به تفکیک ایستگاه
        for i, station in enumerate(stations):
            station_data = df[df['Station'] == station]
            ax.scatter(station_data[config['x']], station_data['TDS'], 
                       label=station, color=colors(i), marker=markers[i % len(markers)], 
                       edgecolors='k', s=70, alpha=0.8)

        # تنظیمات محورها و مقیاس لگاریتمی برای TDS
        ax.set_yscale('log')
        ax.set_title(config['title'], fontsize=14, fontweight='bold')
        ax.set_xlabel(config['xlabel'], fontsize=12)
        ax.set_ylabel('TDS (mg/L)', fontsize=12)
        ax.grid(True, which="both", ls="-", alpha=0.3)
        
        # افزودن راهنمای نمودار در بیرون کادر
        ax.legend(title="Stations", bbox_to_anchor=(1.05, 1), loc='upper left')

        # ذخیره‌سازی
        plt.tight_layout()
        plt.savefig(output_dir / config['filename'], bbox_inches='tight')
        print(f"Saved: {config['filename']}")
        plt.close()

    # --- ۴. ذخیره نتایج محاسباتی در اکسل جدید ---
    output_excel = output_dir / "Hydrochemical_Analysis_Results.xlsx"
    try:
        df.to_excel(output_excel, index=False)
        print(f"✅ Success! Results saved to: {output_excel}")
    except Exception as e:
        print(f"Error saving Excel: {e}")

if __name__ == "__main__":
    analyze_hydrochemistry()
