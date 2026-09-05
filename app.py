cat << 'EOF' > app.py
import streamlit as st
import pandas as pd
from gis.loader import load_berlin_districts
from optimization.optimizer import optimize_bess
from optimization.forecaster import predict_market_multiplier
from streamlit_folium import st_folium
import folium

st.set_page_config(
    page_title="Berlin BESS Siting & Optimization Dashboard",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Berlin BESS Location & Optimization Dashboard")
st.markdown("Geospatial optimization and capacity sizing framework for grid-scale Battery Energy Storage Systems (BESS) across Berlin districts.")

st.sidebar.header("Market & Battery Parameters")

price_spread = st.sidebar.slider(
    "Average Price Spread (EUR/MWh)",
    min_value=30.0,
    max_value=150.0,
    value=90.0,
    step=5.0
)

annual_cycles = st.sidebar.number_input(
    "Annual Cycles",
    min_value=100,
    max_value=700,
    value=365,
    step=10
)

st.sidebar.subheader("🤖 ML Market Forecasting")
use_ml_forecast = st.sidebar.checkbox("Enable ML Price Prediction", value=False)

if use_ml_forecast:
    ren_factor = st.sidebar.slider("Renewable Penetration Index", 0.0, 1.0, 0.6, 0.1)
    demand_factor = st.sidebar.slider("Grid Demand Index", 0.0, 1.0, 0.5, 0.1)
    vol_factor = st.sidebar.slider("Market Volatility Index", 0.0, 1.0, 0.7, 0.1)
    
    price_multiplier = predict_market_multiplier(ren_factor, demand_factor, vol_factor)
    st.sidebar.success(f"🎯 ML Predicted Multiplier: **{price_multiplier}x**")
else:
    price_multiplier = st.sidebar.slider(
        "Price Scenario Multiplier",
        min_value=0.5,
        max_value=2.0,
        value=1.0,
        step=0.1
    )

st.sidebar.subheader("🔋 Battery Degradation Model")
deg_cost_rate = st.sidebar.slider(
    "Degradation Cost (EUR / MWh-cycle)",
    min_value=0.5,
    max_value=5.0,
    value=1.5,
    step=0.25
)

df_districts = load_berlin_districts()

results = optimize_bess(
    df_districts, 
    price_spread=price_spread, 
    annual_cycles=annual_cycles, 
    price_multiplier=price_multiplier,
    deg_cost_per_mwh_cycle=deg_cost_rate
)
df_results = pd.DataFrame(results)

st.subheader("📊 Optimization & Net Profitability Results by Neighborhood")
st.info(f"ℹ️ Active Multiplier: **{price_multiplier}x** {'(ML Forecasted)' if use_ml_forecast else '(Manual)'} | Degradation Rate: **€{deg_cost_rate}/MWh-cycle**")

st.dataframe(df_results, use_container_width=True)

st.download_button(
    label="📥 Download Optimization Report (CSV)",
    data=df_results.to_csv(index=False).encode('utf-8'),
    file_name="berlin_bess_optimization_report.csv",
    mime="text/csv"
)

st.subheader("🗺️ Interactive District Map & Net Profit Potential in Berlin")

# Using standard OpenStreetMap via explicit tiles URL endpoint to prevent API key prompts
m = folium.Map(
    location=[52.52, 13.405], 
    zoom_start=11, 
    tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    attr="© OpenStreetMap contributors"
)

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
EOF
