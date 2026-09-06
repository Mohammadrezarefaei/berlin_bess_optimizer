cat <<  > app.py
import streamlit as st
import pandas as pd
import plotly.express as px
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

total_profit = df_results['net_annual_profit_eur'].sum()
total_mw = df_results['optimal_bess_mw'].sum()
total_mwh = df_results['optimal_bess_mwh'].sum()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Net Annual Profit", f"€{total_profit:,.0f}")
col2.metric("⚡ Total Optimal Power", f"{total_mw:,.1f} MW")
col3.metric("🔋 Total Storage Capacity", f"{total_mwh:,.1f} MWh")

st.divider()

st.subheader("📊 Optimization Results")
st.dataframe(df_results, use_container_width=True)

st.download_button("📥 Download Optimization Report (CSV)", df_results.to_csv(index=False).encode('utf-8'), "berlin_bess_report.csv", "text/csv")

st.subheader("🗺️ Interactive Geospatial Map of Berlin Districts")

map_data = []
for idx, row in df_results.iterrows():
    lat_offset = (idx % 3 - 1) * 0.03
    lon_offset = ((idx // 3) % 3 - 1) * 0.04
    map_data.append({
        'Latitude': 52.52 + lat_offset,
        'Longitude': 13.405 + lon_offset,
        'Neighborhood': row['neighborhood'],
        'District': row['district'],
        'Optimal_MW': row['optimal_bess_mw'],
        'Optimal_MWh': row['optimal_bess_mwh'],
        'Net_Profit_EUR': row['net_annual_profit_eur'],
        'Congestion_Risk': row['congestion_risk']
    })

df_map = pd.DataFrame(map_data)

# Using Plotly Scatter Mapbox with OpenStreetMap (No API key required)
fig = px.scatter_mapbox(
    df_map,
    lat='Latitude',
    lon='Longitude',
    size='Optimal_MW',
    color='Net_Profit_EUR',
    hover_name='Neighborhood',
    hover_data={
        'Latitude': False,
        'Longitude': False,
        'District': True,
        'Optimal_MW': True,
        'Optimal_MWh': True,
        'Net_Profit_EUR': True,
        'Congestion_Risk': True
    },
    color_continuous_scale='Teal',
    size_max=30,
    zoom=10.5,
    center={'lat': 52.52, 'lon': 13.405},
    mapbox_style="open-street-map"
)

fig.update_layout(
    margin={'r':0, 't':0, 'l':0, 'b':0},
    height=550
)

st.plotly_chart(fig, use_container_width=True)
EOF
