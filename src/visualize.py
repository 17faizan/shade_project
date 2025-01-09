import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

def visualize_with_sun_3d(buildings, heights, shadows, sun_position):
    """
    Visualize buildings, their shadows, and the sun's position in 3D.

    Args:
        buildings (list of Polygon): List of building footprints.
        heights (list of float): Heights of buildings.
        shadows (list of Polygon): List of shadow polygons on the ground.
        sun_position (tuple): 3D coordinates of the sun (x, y, z).
    """
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection='3d')

    # Plot buildings as extruded prisms
    for i, building in enumerate(buildings):
        x, y = building.exterior.xy
        z = np.zeros(len(x))  # Base of the building
        verts = [
            [(x[j], y[j], 0) for j in range(len(x))],  # Base face
            [(x[j], y[j], heights[i]) for j in range(len(x))]  # Top face
        ]
        walls = []
        for j in range(len(x) - 1):
            walls.append([
                (x[j], y[j], 0), (x[j], y[j], heights[i]),
                (x[j + 1], y[j + 1], heights[i]), (x[j + 1], y[j + 1], 0)
            ])
        ax.add_collection3d(Poly3DCollection(verts, facecolors='blue', alpha=0.7, edgecolor='black'))
        for wall in walls:
            ax.add_collection3d(Poly3DCollection([wall], facecolors='blue', alpha=0.7, edgecolor='black'))

    # Plot shadows on the ground
    for shadow in shadows:
        x, y = shadow.exterior.xy
        z = np.zeros(len(x))
        verts = [list(zip(x, y, z))]
        ax.add_collection3d(Poly3DCollection(verts, facecolors='gray', alpha=0.4, edgecolor='black'))

    # Annotate shadow lengths
    for shadow, building in zip(shadows, buildings):
        shadow_x, shadow_y = shadow.exterior.xy[:2]
        building_x, building_y = building.exterior.xy[:2]
        shadow_length = np.linalg.norm(
            [shadow_x[0] - building_x[0], shadow_y[0] - building_y[0]]
        )
        ax.text(
            shadow_x[0], shadow_y[0], 0,
            f"{shadow_length:.2f}m",
            color='red'
        )

    # Add the ground plane for context
    ground_x = np.linspace(-10, 15, 20)
    ground_y = np.linspace(-10, 15, 20)
    ground_x, ground_y = np.meshgrid(ground_x, ground_y)
    ground_z = np.zeros_like(ground_x)
    ax.plot_surface(ground_x, ground_y, ground_z, color='lightgray', alpha=0.2)

    # Add the sun
    sun_x, sun_y, sun_z = sun_position
    ax.scatter(sun_x, sun_y, sun_z, color='yellow', s=200, label="Sun")

    # Add rays from the sun to the tops of buildings
    for i, building in enumerate(buildings):
        for x, y in building.exterior.coords:
            ax.plot(
                [sun_x, x], [sun_y, y], [sun_z, heights[i]],
                color='orange', linestyle='--', linewidth=0.8
            )

    # Adjust perspective for better depth understanding
    ax.view_init(elev=45, azim=135)

    # Set labels and legend
    ax.set_title("Building Shadows with Sun Position (3D)")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_zlabel("Height (meters)")
    ax.legend(loc='upper right')
    plt.show()
