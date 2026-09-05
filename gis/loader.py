import geopandas as gpd
from shapely.geometry import Polygon
import pandas as pd

def get_berlin_bess_grid_data():
    """
    تولید دیتافریم مکانی (GeoDataFrame) برای محله‌های کلیدی برلین 
    همراه با اطلاعات بار شبکه و پتانسیل BESS
    """
    data = {
        "neighborhood": ["Charlottenburg", "Mitte", "Kreuzberg", "Prenzlauer Berg", "Spandau"],
        "district": ["Charlottenburg-Wilmersdorf", "Mitte", "Friedrichshain-Kreuzberg", "Pankow", "Spandau"],
        "geometry": [
            Polygon([[13.28, 52.51], [13.33, 52.51], [13.33, 52.55], [13.28, 52.55]]),
            Polygon([[13.38, 52.51], [13.42, 52.51], [13.42, 52.54], [13.38, 52.54]]),
            Polygon([[13.39, 52.48], [13.43, 52.48], [13.43, 52.51], [13.39, 52.51]]),
            Polygon([[13.40, 52.54], [13.45, 52.54], [13.45, 52.57], [13.40, 52.57]]),
            Polygon([[13.19, 52.53], [13.25, 52.53], [13.25, 52.57], [13.19, 52.57]])
        ],
        "grid_congestion_risk": ["High", "Medium", "Low", "Medium", "High"],
        "avg_load_mw": [45.5, 60.2, 30.1, 28.4, 50.0],
        "bess_potential_mw": [20.0, 15.0, 10.0, 12.0, 25.0]
    }
    
    gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")
    return gdf

if __name__ == "__main__":
    df = get_berlin_bess_grid_data()
    print(df.head())
    