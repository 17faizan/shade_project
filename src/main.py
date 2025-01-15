import geopandas as gpd
import random
from fetch_data import create_sample_data, save_to_file, fetch_building_data_with_heights
from calculate_shade import project_shadow, load_buildings, calculate_sun_position
from visualize import visualize_with_sun_3d  
import time
from tqdm import tqdm
"""
def main():
    
    Main function to run the shade simulation pipeline.
"""
    
'''
    # Step 1: Generate sample building dat
    print("Generating sample building data...")
    gdf = create_sample_data()
    save_to_file(gdf, "data/buildings.geojson")
    print("Sample building data saved.")

    # Step 2: Load building data
    print("Loading building data...")
    buildings = load_buildings("data/buildings.geojson")
    print("Building data loaded.")

    # Step 3: Assign random heights to each building
    print("Assigning building heights...")
    heights = [random.randint(5, 20) for _ in range(len(buildings))]
    buildings["height"] = heights  # Add heights as a column
    print(f"Building heights: {heights}")
   


    # Step 4: Calculate shadows for each building
    print("Calculating shadows...")
    shadows = []
    for _, row in buildings.iterrows():
        building = row["geometry"]
        height = row["height"]
        shadow = project_shadow(building, height=height, sun_azimuth=135, sun_altitude=45)
        shadows.append(shadow)
    print("Shadows calculated.")

    # Step 5: Define sun position
    sun_position = (5, 10, 50)  # Example (x, y, z)
   
    # Debugging buildings and heights
    print("Buildings:", buildings)
    print("Building Heights:", heights)
    # Debugging shadows
    for i, shadow in enumerate(shadows):
        print(f"Shadow {i + 1}: {shadow}")

    # Step 6: Visualize buildings, shadows, and sun position
    print("Visualizing buildings, shadows, and sun position in 3D...")
    # Calculate the sun position dynamically
    sun_azimuth = 135  # Example value in degrees
    sun_altitude = 45  # Example value in degrees
    sun_position = calculate_sun_position(sun_azimuth, sun_altitude)

    # Pass the dynamically calculated sun_position
    visualize_with_sun_3d(buildings["geometry"], heights, shadows, sun_position)
    print("Visualization complete.")

if __name__ == "__main__":
    main()
 '''

from fetch_data import fetch_building_data_with_heights, save_to_file
from calculate_shade import project_shadow
from visualize import visualize_with_sun_3d

from fetch_data import fetch_building_data_with_heights
from calculate_shade import project_shadow
from visualize import visualize_with_sun_3d

def main():
    # Step 1: Fetch real-world building data
    place_name = "Hartford, Connecticut, USA"
    print(f"Fetching building data for {place_name}...")
    buildings_gdf = fetch_building_data_with_heights(place_name)
    if buildings_gdf is None:
        print("Failed to fetch building data. Exiting.")
        return

    print(f"Number of buildings fetched: {len(buildings_gdf)}")
    print(buildings_gdf.head())  # Inspect the first few rows
    print(f"Number of valid geometries: {buildings_gdf.is_valid.sum()} / {len(buildings_gdf)}")

    # Step 2: Calculate shadows for each building
    print("Calculating shadows...")
    shadows = []
    heights = []
    for _, row in buildings_gdf.iterrows():
        building = row["geometry"]
        height = row["height"]
        shadow = project_shadow(building, height=height, sun_azimuth=135, sun_altitude=45)
        shadows.append(shadow)
        heights.append(height)
    print(f"Number of buildings processed for shadows: {len(buildings_gdf['geometry'])}")
    print(f"Number of shadows generated: {len(shadows)}")

    # Step 3: Visualize buildings, shadows, and sun position
    print(f"Preparing to visualize {len(buildings_gdf['geometry'])} buildings and {len(shadows)} shadows.")
    visualize_with_sun_3d(buildings_gdf["geometry"], heights, shadows, sun_position=(10, -10, 50))
    print("Visualization complete.")

    


if __name__ == "__main__":
    main()