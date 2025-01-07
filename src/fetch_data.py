import geopandas as gpd
from shapely.geometry import Polygon

def create_sample_data():
    """
    Create a GeoDataFrame with simulated building polygons for testing.

    Returns:
        GeoDataFrame: Simulated geospatial data.
    """
    # Simulate some polygons (buildings)
    polygons = [
        Polygon([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]),  # Square building
        Polygon([[1, 1], [1, 2], [2, 2], [2, 1], [1, 1]]),  # Square building
        Polygon([[2, 0], [2, 3], [3, 3], [3, 0], [2, 0]])   # Rectangle building
    ]

    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame(
        {"building_id": [1, 2, 3]},  # Example IDs
        geometry=polygons,
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
