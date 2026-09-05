Markdown# Berlin BESS Siting & Optimization Dashboard

A geospatial optimization and capacity sizing framework for grid-scale Battery Energy Storage Systems (BESS) across Berlin districts. This project combines spatial data analysis, linear programming optimization, and an interactive web dashboard to evaluate grid congestion risks and maximize arbitrage profitability.

🌐 **Live Demo:** [View Streamlit Dashboard](https://scaling-zebra-wrvj49vjxwrq2gx77-8501.app.github.dev/)

---

## 🚀 Key Features

* **Geospatial District Analysis (`GeoPandas` & `Shapely`):** Models Berlin neighborhood boundaries, spatial distributions, and local grid congestion risks.
* **Linear Optimization Engine (`PuLP`):** Solves linear programming models to determine optimal power ($MW$) and energy ($MWh$) sizing for BESS units while maximizing annual arbitrage revenue.
* **Interactive Dashboard (`Streamlit` & `Folium`):** Provides a dynamic web interface featuring real-time parameter tuning (price spreads and annual cycles), optimization result tables, and an interactive map of Berlin.

---

## 📊 Dashboard Preview

| Optimization Results & Table | Interactive Folium Map |
| :---: | :---: |
| ![Dashboard Table](assets/dashboard_table.png) | ![Dashboard Map](assets/dashboard_map.png) |

Navigate into the directory:Bashcd berlin_bess_optimizer
Install the required dependencies:Bashpip install -r requirements.txt
🖥️ Running the DashboardLaunch the Streamlit web application locally:Bashpython3 -m streamlit run app.py
Open the provided local URL in your browser to interact with the dashboard, adjust market parameters via the sidebar, and analyze optimal BESS allocations across Berlin.📦 Tech Stack & Features ComparisonComponentTechnologyPrimary FunctionGIS & SpatialGeoPandas, ShapelyBerlin district boundaries & spatial modelingOptimizationPuLP (Linear Programming)Siting, sizing ($MW$/$MWh$), & arbitrage maximizationDashboardStreamlit, Streamlit-FoliumWeb UI, interactive maps, & parameter slidersData ProcessingPandas, NumPyMarket spread calculations & results aggregation

## 📂 Project Structure

```text
berlin_bess_optimizer/
│
├── data/                    # Shapefiles and market data directory
├── gis/                     # Spatial data loading and processing modules
│   └── loader.py            # Generates Berlin district boundaries and grid parameters
├── optimization/            # Mathematical optimization modules
│   └── optimizer.py         # PuLP linear programming model for BESS sizing and profit
├── app.py                   # Main Streamlit dashboard application
└── requirements.txt         # Required Python packages
