cat << 'EOF' > app.py
import streamlit as st
import pandas as pd
from gis.loader import load_berlin_districts
from optimization.optimizer import optimize_bess
from optimization.forecaster import predict_market_multiplier

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

# Adding mock latitude and longitude columns for native Streamlit map rendering over Berlin coordinates
map_data = []
for idx, row in df_results.iterrows():
    lat_offset = (idx % 3 - 1) * 0.03
    lon_offset = ((idx // 3) % 3 - 1) * 0.04
    base_lat, base_lon = 52.52 + lat_offset, 13.405 + lon_offset
    map_data.append({
        'lat': base_lat,
        'lon': base_lon,
        'neighborhood': row['neighborhood'],
        'net_annual_profit_eur': row['net_annual_profit_eur']
    })

df_map = pd.DataFrame(map_data)
st.map(df_map, latitude='lat', longitude='lon', size='net_annual_profit_eur', zoom=10)
EOF
