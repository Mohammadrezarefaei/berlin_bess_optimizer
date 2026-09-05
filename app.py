import streamlit as st
import folium
from streamlit_folium import st_folium
from gis.loader import get_berlin_bess_grid_data
from optimization.optimizer import optimize_berlin_bess

# Page configuration
st.set_page_config(page_title="Berlin BESS Optimizer", layout="wide")

st.title("⚡ Berlin BESS Location & Optimization Dashboard")
st.markdown("Geospatial optimization and capacity sizing framework for grid-scale Battery Energy Storage Systems across Berlin districts.")

# Load data and run optimization
gdf = get_berlin_bess_grid_data()

# Sidebar for market and battery parameters
st.sidebar.header("Market & Battery Parameters")
price_spread = st.sidebar.slider("Average Price Spread (EUR/MWh)", min_value=40.0, max_value=150.0, value=80.0, step=5.0)
cycles = st.sidebar.number_input("Annual Cycles", min_value=100, max_value=700, value=365)

# Re-run optimization with updated sidebar parameters
df_results = optimize_berlin_bess(gdf, price_spread_eur_per_mwh=price_spread, annual_cycles=cycles)

# Display results table in the dashboard
st.subheader("📊 Optimization & Profitability Results by Neighborhood")
st.dataframe(df_results, use_container_width=True)

# Interactive Berlin map section using Folium
st.subheader("🗺️ Interactive District Map & BESS Potential in Berlin")

# Center coordinates for Berlin
m = folium.Map(location=[52.52, 13.40], zoom_start=11)

# Add circles to the map for each neighborhood based on optimal BESS size
for idx, row in gdf.iterrows():
    res_row = df_results[df_results["neighborhood"] == row["neighborhood"]].iloc[0]
    
    popup_text = f"""
    <b>Neighborhood:</b> {row['neighborhood']}<br>
    <b>District:</b> {row['district']}<br>
    <b>Congestion Risk:</b> {row['grid_congestion_risk']}<br>
    <b>Optimal BESS:</b> {res_row['optimal_bess_mw']} MW / {res_row['optimal_bess_mwh']} MWh<br>
    <b>Est. Profit:</b> €{res_row['estimated_annual_profit_eur']:,.2f}
    """
    
    centroid = row['geometry'].centroid
    folium.CircleMarker(
        location=[centroid.y, centroid.x],
        radius=float(res_row['optimal_bess_mw']) * 0.8,
        popup=popup_text,
        tooltip=row['neighborhood'],
        color="crimson",
        fill=True,
        fill_color="crimson"
    ).add_to(m)

# Render the map in Streamlit
st_folium(m, width=1200, height=500)