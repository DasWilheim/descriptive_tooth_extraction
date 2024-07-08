import numpy as np
import json
import os
from scipy.integrate import simps
from numpy import gradient

def load_data_from_json(relative_path):
    # Construct an absolute path from a relative path
    script_dir = os.path.dirname(__file__)  # Directory of the current script
    project_root = os.path.abspath(os.path.join(script_dir, '../../'))  # Go up two levels to reach the project root

    file_path = os.path.join(project_root, relative_path)  # Construct the full file path

    with open(file_path, 'r') as file:
        data = json.load(file)

        raw_forces = [data['translated_forces_x'], data['translated_forces_y'], data['translated_forces_z']]
        raw_torques = [data['translated_torques_x'], data['translated_torques_y'], data['translated_torques_z']]
        sensor_data = np.array(raw_forces + raw_torques).T
    return sensor_data

def compute_metrics(data, dt):
    # Initialize the metrics dictionary
    metrics = {}

    # Calculate Peak Plus
    metrics['PEAK+'] = np.max(data, axis=0)

    # Calculate Peak Minus
    metrics['PEAK-'] = -np.min(data, axis=0)

    # Calculate Peak to Peak
    metrics['PP'] = metrics['PEAK+'] + metrics['PEAK-']

    # Calculate Integrated Absolute Value
    # Using simps to integrate over all data points for each force/torque dimension
    metrics['INTABS'] = simps(np.abs(data), dx=dt, axis=0)

    # Calculate DER (derivative)
    # First calculate derivative, then square it, integrate (sum), and take the square root
    dx_dt = gradient(data, axis=0, edge_order=2)
    metrics['DER'] = np.sqrt(simps(dx_dt**2, dx=dt, axis=0))

    # Calculate Mean Absolute Nonzero Force (MANF)
    threshold = 0.1  # Define a threshold for 'nonzero' force
    nonzero_data = data[np.any(np.abs(data) > threshold, axis=1)]
    metrics['MANF'] = np.mean(np.abs(nonzero_data), axis=0)

    # PCA related calculations for Force Volume
    if data.shape[1] == 3:  # Ensure data has three components
        cov_matrix = np.cov(data, rowvar=False)
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
        sorted_indices = np.argsort(eigenvalues)[::-1]
        std_deviations = np.sqrt(eigenvalues[sorted_indices])
        metrics['FV'] = (4/3) * np.pi * np.prod(std_deviations)

    return metrics

# Example usage
file_path = 'data/filtered/noorlag/translated_sensordata_2024-04-18T16;25;02-38.json'
sensor_data = load_data_from_json(file_path)
dt = 1/990  # Sampling interval, e.g., 990 Hz sampling rate

# Assuming sensor data has three force and three torque columns
force_data = sensor_data[:, :3]  # First three columns for forces
torque_data = sensor_data[:, 3:]  # Next three columns for torques

force_metrics = compute_metrics(force_data, dt)
torque_metrics = compute_metrics(torque_data, dt)

# Optionally, print or save the computed metrics
print("Force Metrics:", force_metrics)
print("Torque Metrics:", torque_metrics)

