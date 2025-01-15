import osmnx as ox

place_name = "Glastonbury, Connecticut USA"
tags = {"building": True}

try:
    print("Attempting to fetch features...")
    # Use features_from_place instead of geometries_from_place
    gdf = ox.features_from_place(place_name, tags)
    print("Features fetched successfully.")  # Only prints if the function succeeds
    print(gdf.head())  # Display the first few rows of the GeoDataFrame
except Exception as e:
    print(f"Error occurred: {e}")
