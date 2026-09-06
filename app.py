import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium
from gis.loader import load_berlin_districts
from optimization.optimizer import optimize_bess
from optimization.forecaster import predict_market_multiplier

st.set_page_config(
    page_title="Berlin BESS Siting & Optimization Dashboard", layout="wide"
)

st.title("Berlin BESS Siting & Optimization Dashboard")
st.markdown("""
Geospatial optimization and capacity sizing framework for grid-scale Battery Energy Storage Systems (BESS) across Berlin districts.
""")

# Sidebar parameters for user tuning
st.sidebar.header("Optimization Parameters")
price_spread = st.sidebar.slider(
    "Base Price Spread (€/MWh)", min_value=30.0, max_value=150.0, value=90.0, step=5.0
)
annual_cycles = st.sidebar.slider(
    "Annual Cycles", min_value=100, max_value=700, value=365, step=25
)
deg_cost = st.sidebar.slider(
    "Degradation Cost (€/MWh·cycle)",
    min_value=0.5,
    max_value=5.0,
    value=1.5,
    step=0.25,
)

st.sidebar.subheader("ML Forecaster Inputs")
renewable_f = st.sidebar.slider(
    "Renewable Penetration Factor", 0.0, 1.0, 0.5, 0.1
)
demand_f = st.sidebar.slider("Grid Demand Index", 0.0, 1.0, 0.5, 0.1)
volatility_f = st.sidebar.slider("Market Volatility Index", 0.0, 1.0, 0.5, 0.1)

# Predict multiplier using ML model
price_multiplier = predict_market_multiplier(renewable_f, demand_f, volatility_f)
st.sidebar.metric(
    label="Predicted Price Spread Multiplier", value=price_multiplier
)

# Load data and run optimization
gdf_districts = load_berlin_districts()
optimization_results = optimize_bess(
    gdf_districts,
    price_spread=price_spread,
    annual_cycles=annual_cycles,
    price_multiplier=price_multiplier,
    deg_cost_per_mwh_cycle=deg_cost,
)
df_results = pd.DataFrame(optimization_results)

# Display metrics overview
col1, col2, col3 = st.columns(3)
col1.metric("Total Optimal BESS Power", f"{df_results['optimal_bess_mw'].sum():,.2f} MW")
col2.metric("Total Optimal BESS Energy", f"{df_results['optimal_bess_mwh'].sum():,.2f} MWh")
col3.metric("Total Net Annual Profit", f"€{df_results['net_annual_profit_eur'].sum():,.0f}")

# Layout: Map and Table side by side
st.subheader("Geospatial & Siting Results")
m = folium.Map(location=[52.52, 13.405], zoom_start=11, tiles="OpenStreetMap")

for idx, row in gdf_districts.iterrows():
    match_res = next((item for item in optimization_results if item['neighborhood'] == row['neighborhood']), {})
    net_prof = match_res.get('net_annual_profit_eur', 0)
    opt_mw = match_res.get('optimal_bess_mw', 0)
    
    color = "red" if row['congestion_risk'] == 'High' else ("orange" if row['congestion_risk'] == 'Medium' else "green")
    
    popup_text = f"""
    <b>Neighborhood:</b> {row['neighborhood']}<br>
    <b>District:</b> {row['district']}<br>
    <b>Congestion Risk:</b> {row['congestion_risk']}<br>
    <b>Optimal Power:</b> {opt_mw} MW<br>
    <b>Net Profit:</b> €{net_prof:,}
    """
    
    # Add geometry to folium map
    folium.GeoJson(
        row['geometry'],
        style_function=lambda x, col=color: {
            'fillColor': col,
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6
        },
        popup=folium.Popup(popup_text, max_width=300)
    ).add_to(m)

c1, c2 = st.columns([1.2, 1])
with c1:
    st_folium(m, width=650, height=500)

with c2:
    st.markdown("### District Optimization Breakdown")
    st.dataframe(df_results[['neighborhood', 'optimal_bess_mw', 'optimal_bess_mwh', 'net_annual_profit_eur', 'congestion_risk']], height=480)
