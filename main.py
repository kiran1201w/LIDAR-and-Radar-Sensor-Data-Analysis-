import numpy as np
import pandas as pd
import open3d as o3d  # For LIDAR point cloud visualization
import matplotlib.pyplot as plt

# -------------------------------
# Step 1: Load and Process LIDAR Data
# -------------------------------
def load_lidar_data(file_path):
    """Load LIDAR point cloud data from a .pcd or .csv file."""
    try:
        # Assuming data format: x, y, z (3D point cloud)
        point_cloud = pd.read_csv(file_path, header=None, names=["x", "y", "z"])
        print("LIDAR data loaded successfully!")
        return point_cloud
    except Exception as e:
        print(f"Error loading LIDAR data: {e}")
        return None

# Visualize LIDAR point cloud
def visualize_lidar_data(point_cloud_df):
    """Visualize LIDAR point cloud data using Open3D."""
    pcd = o3d.geometry.PointCloud()
    points = point_cloud_df.to_numpy()
    pcd.points = o3d.utility.Vector3dVector(points)
    o3d.visualization.draw_geometries([pcd])

# -------------------------------
# Step 2: Load and Process Radar Data
# -------------------------------
def load_radar_data(file_path):
    """Load radar sensor data from CSV."""
    try:
        # Assuming radar data format: object_id, distance, velocity, angle
        radar_data = pd.read_csv(file_path)
        print("Radar data loaded successfully!")
        return radar_data
    except Exception as e:
        print(f"Error loading radar data: {e}")
        return None

# Visualize radar sensor data
def visualize_radar_data(radar_df):
    """Visualize radar data using a 2D scatter plot."""
    plt.figure(figsize=(10, 6))
    plt.scatter(radar_df['angle'], radar_df['distance'], c=radar_df['velocity'], cmap='viridis')
    plt.colorbar(label='Velocity (m/s)')
    plt.xlabel('Angle (degrees)')
    plt.ylabel('Distance (m)')
    plt.title('Radar Data Visualization')
    plt.grid()
    plt.show()

# -------------------------------
# Step 3: Combine and Analyze Data
# -------------------------------
def combine_and_analyze_data(lidar_df, radar_df):
    """Analyze combined LIDAR and radar data."""
    print("Combining LIDAR and radar data...")
    # Example analysis: Match radar detections with LIDAR points (simplified)
    combined_data = pd.merge(lidar_df, radar_df, left_index=True, right_index=True, how='inner')
    
    print(f"Combined Data Head:\n{combined_data.head()}")

    # Example metric: Average velocity for objects detected within a specific range
    close_objects = combined_data[combined_data['distance'] < 50]
    avg_velocity = close_objects['velocity'].mean()
    print(f"Average velocity of objects within 50 meters: {avg_velocity:.2f} m/s")

    return combined_data

# -------------------------------
# Main Execution
# -------------------------------
if __name__ == "__main__":
    # File paths (replace with actual file paths)
    lidar_file_path = "lidar_data.csv"  # Example LIDAR file
    radar_file_path = "radar_data.csv"  # Example radar file

    # Step 1: Load and visualize LIDAR data
    lidar_data = load_lidar_data(lidar_file_path)
    if lidar_data is not None:
        visualize_lidar_data(lidar_data)

    # Step 2: Load and visualize radar data
    radar_data = load_radar_data(radar_file_path)
    if radar_data is not None:
        visualize_radar_data(radar_data)

    # Step 3: Combine and analyze both datasets
    if lidar_data is not None and radar_data is not None:
        combined_results = combine_and_analyze_data(lidar_data, radar_data)
