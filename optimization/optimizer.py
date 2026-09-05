import streamlit as st
import pandas as pd
from gis.loader import load_berlin_districts
from optimization.optimizer import optimize_bess
from streamlit_folium import st_folium
import folium

# Page Configuration
st.set_page_config(
    page_title="Berlin BESS Siting & Optimization Dashboard",
    page_icon="⚡",
    layout="wide"
)

# Dashboard Title & Description
st.title("⚡ Berlin BESS Location & Optimization Dashboard")
st.markdown("Geospatial optimization and capacity sizing framework for grid-scale Battery Energy Storage Systems (BESS) across Berlin districts.")

# Sidebar Parameters for Market & Battery Parameters
st.sidebar.header("Market & Battery Parameters")

price_spread = st.sidebar.slider(
    "Average Price Spread (EUR/MWh)",
    min_value=30.0,
    max_value=150.0,
    value=90.0,
    step=5.0,
    help="Average daily wholesale electricity price spread."
)

annual_cycles = st.sidebar.number_input(
    "Annual Cycles",
    min_value=100,
    max_value=700,
    value=365,
    step=10,
    help="Number of full equivalent charge-discharge cycles per year."
)

# Price Scenario / Stress Testing Multiplier
st.sidebar.subheader("📉 Market Stress Testing")
price_multiplier = st.sidebar.slider(
    "Price Scenario Multiplier",
    min_value=0.5,
    max_value=2.0,
    value=1.0,
    step=0.1,
    help="Simulate bearish (0.5x) or bullish (2.0x) market price conditions."
)

# --- NEW: Battery Degradation & Replacement Cost Parameter ---
st.sidebar.subheader("🔋 Battery Degradation Model")
deg_cost_rate = st.sidebar.slider(
    "Degradation Cost (EUR / MWh-cycle)",
    min_value=0.5,
    max_value=5.0,
    value=1.5,
    step=0.25,
    help="Cost rate accounting for cell wear, capacity fade, and replacement reserve fund per MWh throughput cycle."
)

# Load GIS data for Berlin districts
df_districts = load_berlin_districts()

# Run Optimization with Degradation Parameters
results = optimize_bess(
    df_districts, 
    price_spread=price_spread, 
    annual_cycles=annual_cycles, 
    price_multiplier=price_multiplier,
    deg_cost_per_mwh_cycle=deg_cost_rate
)
df_results = pd.DataFrame(results)

# Display Results Section
st.subheader("📊 Optimization & Net Profitability Results by Neighborhood")
if price_multiplier != 1.0 or deg_cost_rate != 1.5:
    st.info(f"ℹ️ Active Scenario -> Price Multiplier: **{price_multiplier}x** | Degradation Rate: **€{deg_cost_rate}/MWh-cycle**")

st.dataframe(df_results, use_container_width=True)

# Interactive Map Section
st.subheader("🗺️ Interactive District Map & Net Profit Potential in Berlin")

m = folium.Map(location=[52.52, 13.405], zoom_start=11, tiles="CartoDB positron")

for idx, row in df_results.iterrows():
    lat_offset = (idx % 3 - 1) * 0.03
    lon_offset = ((idx // 3) % 3 - 1) * 0.04
    base_lat, base_lon = 52.52 + lat_offset, 13.405 + lon_offset
    
    folium.CircleMarker(
        location=[base_lat, base_lon],
        radius=max(6, float(row['optimal_bess_mw']) / 1.5),
        color="teal",
        fill=True,
        fill_color="teal",
        fill_opacity=0.7,
        popup=f"<b>{row['neighborhood']}</b><br>Power: {row['optimal_bess_mw']} MW<br>Energy: {row['optimal_bess_mwh']} MWh<br>Net Profit: €{row['net_annual_profit_eur']:,}"
    ).add_to(m)

st_folium(m, width=1200, height=500)
