import math
from shapely.geometry import Polygon
import geopandas as gpd

def project_shadow(building, height, sun_azimuth, sun_altitude):
    """
    Project a shadow polygon for a building based on sun position.

    Args:
        building (Polygon): Shapely polygon representing the building footprint.
        height (float): Height of the building in meters.
        sun_azimuth (float): Azimuth angle of the sun in degrees.
        sun_altitude (float): Altitude angle of the sun in degrees.

    Returns:
        Polygon: Shapely polygon representing the shadow.
    """
    shadow_points = []
    # Adjust azimuth reference to match counterclockwise model
    azimuth_rad = math.radians((450 - sun_azimuth) % 360)
    altitude_rad = math.radians(sun_altitude)

    # Calculate shadow length
    shadow_length = height / math.tan(altitude_rad)

    # Project each vertex of the building
    for x, y in building.exterior.coords:
        shadow_x = x - shadow_length * math.cos(azimuth_rad)
        shadow_y = y - shadow_length * math.sin(azimuth_rad)
        shadow_points.append((shadow_x, shadow_y))
        print(f"Building vertex: ({x}, {y}) -> Shadow vertex: ({shadow_x}, {shadow_y})")

    # Combine shadow vertices and building vertices to form the shadow polygon
    return Polygon(shadow_points + list(building.exterior.coords))


def load_buildings(filepath):
    """
    Load building data from a GeoJSON file.

    Args:
        filepath (str): Path to the GeoJSON file.

    Returns:
        GeoDataFrame: Loaded geospatial data.
    """
    return gpd.read_file(filepath, engine="pyogrio")

def calculate_sun_position(sun_azimuth, sun_altitude, distance=50):
    """
    Calculate the 3D position of the sun based on azimuth and altitude.

    Args:
        sun_azimuth (float): Azimuth angle of the sun in degrees.
        sun_altitude (float): Altitude angle of the sun in degrees.
        distance (float): Distance of the sun from the origin in 3D space.

    Returns:
        tuple: (x, y, z) coordinates of the sun.
    """
    azimuth_rad = math.radians((450 - sun_azimuth) % 360)  # Adjust azimuth to match 3D plot convention
    altitude_rad = math.radians(sun_altitude)
    x = distance * math.cos(altitude_rad) * math.cos(azimuth_rad)
    y = distance * math.cos(altitude_rad) * math.sin(azimuth_rad)
    z = distance * math.sin(altitude_rad)
    return x, y, z