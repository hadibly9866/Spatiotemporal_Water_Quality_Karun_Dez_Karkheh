# Paper-to-Code Mapping

This document maps the specific sections of the manuscript to the corresponding Python scripts in this repository.

| Manuscript Section | Analysis / Task | Corresponding Script |
|:--- |:--- |:--- |
| **Methods: Data Preprocessing** | Station & Satellite Data Merging | `src/01_data_preprocessing/data_preprocessing.py` |
| **Methods: WQI Calculation** | Weighted Arithmetic Index | `src/02_water_quality_index/water_quality_index.py` |
| **Results: Temporal Trends** | Mann-Kendall & Sen's Slope | `src/03_temporal_trend_analysis/mann_kendall_trend_analysis.py` |
| **Results: EC-WQI Trends** | Comparative Trend Visualization | `src/03_temporal_trend_analysis/ec_wqi_temporal_trends.py` |
| **Results: Gibbs Diagram** | Hydrochemical Facies Analysis | `src/04_hydrochemical_analysis/gibbs_ionic_ratios_analysis.py` |
| **Results: Spatial Clusters** | Global & Local Moran's I | `src/05_spatial_analysis/spatial_autocorrelation_moran.py` |
| **Results: GWR Modeling** | Spatially Varying Coefficients | `src/05_spatial_analysis/geographically_weighted_regression.py` |
| **Results: Integrated Maps** | Hotspot & GWR Synthesis | `src/05_spatial_analysis/integrated_gwr_hotspot_map.py` |

## Non-Coding Steps
- **Piper & Stiff Diagrams:** Analyzed using external hydrochemical software (RockWare/AquaChem).
- **Cartography:** Final map layouts were refined in ArcGIS/QGIS.
