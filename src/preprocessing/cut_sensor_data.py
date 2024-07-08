import numpy as np
import matplotlib.pyplot as plt
import json
import os
import glob
from scipy.signal import lfilter

candidate = "noorlag"
translated_directory = r'C:\Users\wille\OneDrive\Documenten\Tu Delft\Msc, Robotics\Afstuderen\AMC\Coding\thesis\descriptive_tooth_extraction\data\filtered\{}'.format(candidate)
cutted_directory = r'C:\Users\wille\OneDrive\Documenten\Tu Delft\Msc, Robotics\Afstuderen\AMC\Coding\thesis\descriptive_tooth_extraction\data\cutted\{}'.format(candidate)

# Ensure the filtered directory exists
os.makedirs(cutted_directory, exist_ok=True)

def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        sensor_data = np.array([
            data['translated_forces_x'],
            data['translated_forces_y'],
            data['translated_forces_z'],
            data['translated_torques_x'],
            data['translated_torques_y'],
            data['translated_torques_z']
        ]).T
    return data, sensor_data


def detect_procedure_limits(sensor_data, threshold=0.005, look_back=10, look_forward=10):
    # Calculate the gradient of sensor data
    gradients = np.abs(np.gradient(sensor_data, axis=0))

    # Detect start: check if any gradient exceeds the threshold from the start
    start_indices = np.where((gradients > 0.01).any(axis=1))[0]
    if start_indices.size > 0:
        start_index = max(start_indices[0] - look_back, 0)
    else:
        start_index = None

    # Detect end: reverse the sensor data to detect from the end
    reversed_gradients = np.abs(np.gradient(sensor_data[::-1], axis=0))
    end_indices = np.where((reversed_gradients > threshold).any(axis=1))[0]
    if end_indices.size > 0:
        end_index = len(sensor_data) - end_indices[0] - look_forward
    else:
        end_index = None

    return start_index, end_index


def plot_data_with_limits(sensor_data, start_index, end_index):
    # Labeling for plot
    force_labels = ['Force X', 'Force Y', 'Force Z']
    torque_labels = ['Torque X', 'Torque Y', 'Torque Z']

    # Plotting the data
    plt.figure(figsize=(14, 7))
    for i in range(3):
        plt.subplot(2, 1, 1)
        plt.plot(sensor_data[:, i], label=force_labels[i])
        if start_index is not None:
            plt.axvline(x=start_index, color='r', linestyle='--', label='Procedure Start' if i == 0 else "")
        if end_index is not None:
            plt.axvline(x=end_index, color='g', linestyle='--', label='Procedure End' if i == 0 else "")
        plt.title('Force Readings over Time')
        plt.xlabel('Time')
        plt.ylabel('Force (N)')
        plt.legend()

    for i in range(3, 6):
        plt.subplot(2, 1, 2)
        plt.plot(sensor_data[:, i], label=torque_labels[i - 3])
        if start_index is not None:
            plt.axvline(x=start_index, color='r', linestyle='--')
        if end_index is not None:
            plt.axvline(x=end_index, color='g', linestyle='--')
        plt.title('Torque Readings over Time')
        plt.xlabel('Time')
        plt.ylabel('Torque (Nm)')
        plt.legend()

    plt.tight_layout()
    plt.show()

# Usage

for file_path in glob.glob(os.path.join(translated_directory, '*.json')):
    original_data, sensor_data = load_data(file_path)

    # Detect start and end indices
    start_index, end_index = detect_procedure_limits(sensor_data)

    # Ensure indices are Python int type for JSON serialization
    if start_index is not None:
        original_data['procedure_start'] = int(start_index)
    if end_index is not None:
        original_data['procedure_end'] = int(end_index)

    # Slice the original data to the start and end index
    sensor_data_cutted = sensor_data[start_index:end_index]

    # Update the original data dictionary with cut data
    original_data.update({
        "translated_forces_x": sensor_data_cutted[:, 0].tolist(),
        "translated_forces_y": sensor_data_cutted[:, 1].tolist(),
        "translated_forces_z": sensor_data_cutted[:, 2].tolist(),
        "translated_torques_x": sensor_data_cutted[:, 3].tolist(),
        "translated_torques_y": sensor_data_cutted[:, 4].tolist(),
        "translated_torques_z": sensor_data_cutted[:, 5].tolist()
    })

    output_filename = os.path.basename(file_path)
    output_path = os.path.join(cutted_directory, output_filename)

    # Save the filtered data
    with open(output_path, 'w') as file:
        json.dump(original_data, file, indent=4)

    print(f"Filtered data saved to: {output_path}")