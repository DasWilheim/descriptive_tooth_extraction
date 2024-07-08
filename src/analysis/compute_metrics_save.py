import numpy as np
import json
import os
import glob
from scipy.integrate import simps
from numpy import gradient

def load_data_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        raw_forces = [data['translated_forces_x'], data['translated_forces_y'], data['translated_forces_z']]
        raw_torques = [data['translated_torques_x'], data['translated_torques_y'], data['translated_torques_z']]
        sensor_data = np.array(raw_forces + raw_torques).T
    return data, sensor_data

def compute_metrics(data, dt):
    # Initialize the metrics dictionary
    metrics = {}

    # Calculate Peak Plus
    metrics['PEAK+'] = np.max(data, axis=0).tolist()

    # Calculate Peak Minus
    metrics['PEAK-'] = (-np.min(data, axis=0)).tolist()

    # Calculate Peak to Peak
    # Directly add the two lists element-wise using list comprehension
    metrics['PP'] = [a + b for a, b in zip(metrics['PEAK+'], metrics['PEAK-'])]

    # Calculate Integrated Absolute Value
    metrics['INTABS'] = simps(np.abs(data), dx=dt, axis=0).tolist()

    # Calculate DER (derivative)
    dx_dt = gradient(data, axis=0, edge_order=2)
    metrics['DER'] = np.sqrt(simps(dx_dt**2, dx=dt, axis=0)).tolist()

    # Calculate Mean Absolute Nonzero Force (MANF)
    threshold = 0.1  # Define a threshold for 'nonzero' force
    nonzero_data = data[np.any(np.abs(data) > threshold, axis=1)]
    metrics['MANF'] = np.mean(np.abs(nonzero_data), axis=0).tolist()

    # PCA related calculations for Force Volume
    if data.shape[1] == 3:  # Ensure data has three components
        cov_matrix = np.cov(data, rowvar=False)
        eigenvalues, _ = np.linalg.eig(cov_matrix)
        sorted_indices = np.argsort(eigenvalues)[::-1]
        std_deviations = np.sqrt(eigenvalues[sorted_indices])
        metrics['FV'] = (4/3) * np.pi * np.prod(std_deviations).tolist()

    return metrics


# Set candidate and directories
candidate = "noorlag"
cutted_directory = f'data/cutted/{candidate}'
metrics_directory = f'data/metrics/{candidate}'

# Ensure the metrics directory exists
os.makedirs(metrics_directory, exist_ok=True)


dt = 1/990  # Sampling interval, e.g., 990 Hz sampling rate


# Process each translated data file
for file_path in glob.glob(os.path.join(cutted_directory, '*.json')):

    _, sensor_data = load_data_from_json(file_path)
    
    # Assuming sensor data has three force and three torque columns
    force_data = sensor_data[:, :3]  # First three columns for forces
    torque_data = sensor_data[:, 3:]  # Next three columns for torques

    force_metrics = compute_metrics(force_data, dt)
    torque_metrics = compute_metrics(torque_data, dt)
    
    # Prepare the metrics data for saving
    metrics_data = {'force_metrics': force_metrics, 'torque_metrics': torque_metrics}
    
    # Add quadrant and tooth information
    data, _ = load_data_from_json(file_path)
    metrics_data['quadrant'] = data["quadrant"]
    metrics_data['tooth'] = data["tooth"]

    # Construct output file path
    output_filename = os.path.basename(file_path)
    output_file_path = os.path.join(metrics_directory, output_filename)
    
    # Save the metrics data
    with open(output_file_path, 'w') as file:
        json.dump(metrics_data, file, indent=4)
    
    print(f"Metrics saved to: {output_file_path}")
