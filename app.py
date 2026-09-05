cat << 'EOF' > app.py
import streamlit as st
import pandas as pd
import pydeck as pdk
from gis.loader import load_berlin_districts
from optimization.optimizer import optimize_bess
from optimization.forecaster import predict_market_multiplier

st.set_page_config(page_title="Berlin BESS Dashboard", layout="wide")
st.title("⚡ Berlin BESS Location & Optimization Dashboard")

price_spread = st.sidebar.slider("Price Spread (EUR/MWh)", 30.0, 150.0, 90.0, 5.0)
annual_cycles = st.sidebar.number_input("Annual Cycles", 100, 700, 365, 10)

use_ml_forecast = st.sidebar.checkbox("Enable ML Price Prediction", value=False)
if use_ml_forecast:
    price_multiplier = predict_market_multiplier(0.6, 0.5, 0.7)
    st.sidebar.success(f"🎯 ML Multiplier: {price_multiplier}x")
else:
    price_multiplier = st.sidebar.slider("Price Multiplier", 0.5, 2.0, 1.0, 0.1)

deg_cost_rate = st.sidebar.slider("Degradation Cost (EUR/MWh)", 0.5, 5.0, 1.5, 0.25)

df_districts = load_berlin_districts()
results = optimize_bess(df_districts, price_spread, annual_cycles, price_multiplier, deg_cost_rate)
df_results = pd.DataFrame(results)

st.subheader("📊 Optimization Results")
st.dataframe(df_results, use_container_width=True)

st.download_button("📥 Download CSV", df_results.to_csv(index=False).encode('utf-8'), "report.csv", "text/csv")

st.subheader("🗺️ Interactive District Map (Hover for Details)")

map_data = []
for idx, row in df_results.iterrows():
    lat_offset = (idx % 3 - 1) * 0.03
    lon_offset = ((idx // 3) % 3 - 1) * 0.04
    map_data.append({
        'lat': 52.52 + lat_offset,
        'lon': 13.405 + lon_offset,
        'neighborhood': row['neighborhood'],
        'optimal_bess_mw': row['optimal_bess_mw'],
        'net_annual_profit_eur': row['net_annual_profit_eur']
    })

df_map = pd.DataFrame(map_data)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_map,
    get_position=["lon", "lat"],
    get_radius="optimal_bess_mw * 300",
    get_fill_color=[0, 128, 128, 180],
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(latitude=52.52, longitude=13.405, zoom=10, pitch=0)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"html": "<b>Neighborhood:</b> {neighborhood}<br/><b>Net Profit:</b> €{net_annual_profit_eur:,}"}
)

st.pydeck_chart(r)
EOF
