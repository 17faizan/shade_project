import geopandas as gpd
from shapely.geometry import Polygon
from shapely.affinity import translate
import osmnx as ox
import time


import pandas as pd
import random

def fetch_building_data_with_heights(place_name, max_features=None, simplify_tolerance=0.001):
    """
    Fetch building geometries for a given place name, assign heights, and simplify geometry.

    Args:
        place_name (str): The name of the place to fetch data for.
        max_features (int, optional): Limit the number of buildings processed.
        simplify_tolerance (float, optional): Tolerance for simplifying geometries.

    Returns:
        GeoDataFrame: Filtered building geometries with heights.
    """
    print(f"Fetching building data for {place_name}...")
    start_time = time.time()
    try:
        tags = {"building": True}
        gdf = ox.features_from_place(place_name, tags)
        print(f"Features fetched successfully in {time.time() - start_time:.2f} seconds.")

        # Filter for Polygon or MultiPolygon geometries
        buildings_gdf = gdf[gdf.geom_type.isin(["Polygon", "MultiPolygon"])]

        # Limit the number of buildings for testing
        if max_features:
            buildings_gdf = buildings_gdf.head(max_features)
            print(f"Subset of {max_features} features selected.")

        # Simplify geometries for performance
        buildings_gdf["geometry"] = buildings_gdf["geometry"].simplify(simplify_tolerance)
        print(f"Geometries simplified with tolerance {simplify_tolerance}.")

        # Assign heights
        if 'height' in buildings_gdf.columns:
            print("Height data found in the dataset.")
            buildings_gdf['height'] = pd.to_numeric(buildings_gdf['height'], errors='coerce').fillna(10)
        else:
            print("No height data available. Assigning default/random heights.")
            buildings_gdf['height'] = buildings_gdf.apply(lambda _: random.randint(5, 20), axis=1)

        # Save to a GeoJSON file
        buildings_gdf.to_file("data/filtered_buildings.geojson", driver="GeoJSON")
        print(f"Filtered building data saved to 'data/filtered_buildings.geojson'.")
        return buildings_gdf

    except Exception as e:
        print(f"Error fetching building data: {e}")
        return None



def translate_buildings(buildings, translations):
    """
    Translate building polygons to new positions.

    Args:
        buildings (list of Polygon): List of building footprints.
        translations (list of tuple): List of (x_offset, y_offset) for each building.

    Returns:
        list of Polygon: Translated building footprints.
    """
    translated_buildings = []
    for building, (x_offset, y_offset) in zip(buildings, translations):
        translated_buildings.append(translate(building, xoff=x_offset, yoff=y_offset))
    return translated_buildings

def create_sample_data():
    """
    Create a GeoDataFrame with simulated building polygons for testing.

    Returns:
        GeoDataFrame: Simulated geospatial data.
    """
    # Simulate some polygons (buildings)
    polygons = [
        Polygon([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]),  # Square building
        Polygon([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]),  # Square building
        Polygon([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]])   # Square building
    ]

    # Define translations for each building
    translations = [(0, 0), (3, 0), (6, 0)]  # Move buildings along the x-axis

    # Translate buildings to their new positions
    translated_polygons = translate_buildings(polygons, translations)

    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame(
        {"building_id": [1, 2, 3]},  # Example IDs
        geometry=translated_polygons,
        crs="EPSG:4326"  # Set CRS to WGS84
    )

    return gdf

def save_to_file(gdf, filename):
    """
    Save GeoDataFrame to a GeoJSON file.

    Args:
        gdf (GeoDataFrame): Geospatial data to save.
        filename (str): Output file name.
    """
    gdf.to_file(filename, driver="GeoJSON")
    print(f"GeoDataFrame saved to {filename}")

def main():
    """
    Main function to create and save geospatial data.
    """
    print("Creating sample geospatial data...")
    gdf = create_sample_data()
    
    print("Saving data to 'buildings.geojson'...")
    save_to_file(gdf, "data/buildings.geojson")

if __name__ == "__main__":
    main()
