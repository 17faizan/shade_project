import geopandas as gpd
from shapely.geometry import Polygon
from shapely.affinity import translate

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
