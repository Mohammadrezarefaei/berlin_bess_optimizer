import os
from PIL import Image
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="BESS Dispatch & Market Optimization", layout="wide"
)

st.title("BESS Operation & Reserve Allocation Dashboard")

# نمایش تصاویر و نقشه‌های موجود در پوشه assets
st.subheader("GIS & Spatial Analysis")
map_path = "assets/dashboard_map.png"
if os.path.exists(map_path):
    st.image(
        Image.open(map_path),
        caption="GIS Spatial & Site Map",
        use_container_width=True,
    )

st.subheader("Optimization & Financial Tables")
table_path = "assets/dashboard_table.png"
if os.path.exists(table_path):
    st.image(
        Image.open(table_path),
        caption="Model Results & Table",
        use_container_width=True,
    )

# نمودارهای تحلیل بازار و باتری
hours = np.arange(24)
np.random.seed(42)

price = 50 + 25 * np.sin(hours / 3 * np.pi) + np.random.normal(0, 5, 24)
net_power = np.where(
    (hours >= 0) & (hours <= 2),
    0.9,
    np.where((hours >= 18) & (hours <= 21), -0.8, 0.0),
)
fcr_headroom = np.where(
    (hours >= 0) & (hours <= 2), 0.3, np.where((hours >= 19), 0.3, 0.0)
)

df = pd.DataFrame(
    {
        "Hour": hours,
        "Market Price": price,
        "Net Power Flow (Discharge - Charge)": net_power,
        "Fcr Reserve Headroom": fcr_headroom,
    }
)

st.subheader("Market Price (€/MWh)")
st.line_chart(df.set_index("Hour")["Market Price"])

st.subheader("Net Power Flow (MW)")
st.line_chart(df.set_index("Hour")["Net Power Flow (Discharge - Charge)"])

st.subheader("Fcr Reserve Headroom (MW)")
st.line_chart(df.set_index("Hour")["Fcr Reserve Headroom"])
