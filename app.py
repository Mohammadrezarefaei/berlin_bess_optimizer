cat << 'EOF' > app.py
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

st.subheader("📊 Optimization Results")
st.dataframe(df_results, use_container_width=True)

st.download_button("📥 Download CSV", df_results.to_csv(index=False).encode('utf-8'), "report.csv", "text/csv")

st.subheader("🗺️ Geospatial Optimization & Profit Distribution (Berlin Districts)")

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

# Interactive Plotly Scatter Mapbox / Scatter geo implementation with instant hover tooltips
fig = px.scatter(
    df_map,
    x='Longitude',
    y='Latitude',
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
    size_max=35,
    title="Berlin Districts BESS Siting & Profit Potential"
)

fig.update_layout(
    xaxis_title="Longitude",
    yaxis_title="Latitude",
    template="plotly_dark",
    height=550
)

st.plotly_chart(fig, use_container_width=True)
EOF
