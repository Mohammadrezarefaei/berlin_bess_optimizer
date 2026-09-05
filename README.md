Markdown
# Berlin BESS Siting & Optimization Dashboard

A geospatial optimization and capacity sizing framework for grid-scale Battery Energy Storage Systems (BESS) across Berlin districts. This project combines spatial data analysis, linear programming optimization, and an interactive web dashboard to evaluate grid congestion risks and maximize arbitrage profitability.

---

## 🚀 Key Features

* **Geospatial District Analysis (`GeoPandas` & `Shapely`):** Models Berlin neighborhood boundaries, spatial distributions, and local grid congestion risks.
* **Linear Optimization Engine (`PuLP`):** Solves linear programming models to determine optimal power ($MW$) and energy ($MWh$) sizing for BESS units while maximizing annual arbitrage revenue.
* **Interactive Dashboard (`Streamlit` & `Folium`):** Provides a dynamic web interface featuring real-time parameter tuning (price spreads and annual cycles), optimization result tables, and an interactive map of Berlin.

---

## 🛠️ Installation & Setup

1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/berlin_bess_optimizer.git](https://github.com/your-username/berlin_bess_optimizer.git)
   cd berlin_bess_optimizer
Install the required dependencies:

Bash
pip install -r requirements.txt
🖥️ Running the Dashboard
Launch the Streamlit web application locally:

Bash
python3 -m streamlit run app.py
Open the provided local URL in your browser to interact with the dashboard, adjust market parameters via the sidebar, and analyze optimal BESS allocations across Berlin.

📦 Tech Stack
Python 3.12

Streamlit & Streamlit-Folium (Dashboard & Mapping)

GeoPandas & Shapely (Spatial Data Processing)

PuLP (Linear Optimization)

Pandas & NumPy (Data Manipulation)

📂 Project Structure
Plaintext
berlin_bess_optimizer/
│
├── data/                    # Shapefiles and market data directory
├── gis/                     # Spatial data loading and processing modules
│   └── loader.py            # Generates Berlin district boundaries and grid parameters
├── optimization/            # Mathematical optimization modules
│   └── optimizer.py         # PuLP linear programming model for BESS sizing and profit
├── app.py                   # Main Streamlit dashboard application
└── requirements.txt         # Required Python packages
