import geopandas as gpd
import pandas as pd
import shapely.geometry as sg

def load_berlin_districts():
    """
    Loads or generates Berlin districts geospatial data with congestion and spatial weights
    for BESS optimization.
    """
    # Sample data representing Berlin districts/neighborhoods with spatial & grid parameters
    data = {
        'neighborhood': [
            'Mitte', 'Charlottenburg', 'Kreuzberg', 'Prenzlauer Berg', 
            'Friedrichshain', 'Tempelhof', 'Spandau', 'Pankow', 'Neukölln'
        ],
        'district': [
            'Mitte', 'Charlottenburg-Wilmersdorf', 'Friedrichshain-Kreuzberg', 'Pankow', 
            'Friedrichshain-Kreuzberg', 'Tempelhof-Schöneberg', 'Spandau', 'Pankow', 'Neukölln'
        ],
        'congestion_weight': [1.35, 1.25, 1.40, 1.15, 1.30, 1.20, 1.10, 1.12, 1.28],
        'congestion_risk': ['High', 'Medium', 'High', 'Low', 'High', 'Medium', 'Low', 'Low', 'Medium']
    }
    
    # Creating a dummy GeoDataFrame with bounding geometries for Berlin
    df = pd.DataFrame(data)
    
    # Generate approximate polygon geometries for demonstration / spatial handling
    base_lon, base_lat = 13.405, 52.52
    geometries = []
    for i in range(len(df)):
        lon_offset = (i % 3 - 1) * 0.04
        lat_offset = ((i // 3) % 3 - 1) * 0.03
        poly = sg.Polygon([
            (base_lon + lon_offset, base_lat + lat_offset),
            (base_lon + lon_offset + 0.03, base_lat + lat_offset),
            (base_lon + lon_offset + 0.03, base_lat + lat_offset + 0.025),
            (base_lon + lon_offset, base_lat + lat_offset + 0.025)
        ])
        geometries.append(poly)
        
    gdf = gpd.GeoDataFrame(df, geometry=geometries, crs="EPSG:4326")
    return gdf
