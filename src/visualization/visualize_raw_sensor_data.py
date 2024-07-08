import json
import matplotlib.pyplot as plt
import numpy as np
import os

def load_data_from_json(relative_path):
    # Construct an absolute path from a relative path
    script_dir = os.path.dirname(__file__)  # Directory of the current script
    project_root = os.path.abspath(os.path.join(script_dir, '../../'))  # Go up four levels to reach the project root

    file_path = os.path.join(project_root, relative_path)  # Construct the full file path
    
    
    with open(file_path, 'r') as file:
        data = json.load(file)


        print(len(data['raw_forces_x']))

        print(data['end_timestamp'] - data['start_timestamp'])

        print("The frequency", len(data['raw_forces_x']) / (data['end_timestamp'] - data['start_timestamp']) )


        raw_forces = [data['raw_forces_x'], data['raw_forces_y'], data['raw_forces_z']]
        raw_torques = [data['raw_torques_x'], data['raw_torques_y'], data['raw_torques_z']]
        sensor_data = np.array(raw_forces + raw_torques).T
    return sensor_data

def plot_data(sensor_data, distribution=False, graph=False):
    force_labels = ['Force X', 'Force Y', 'Force Z']
    torque_labels = ['Torque X', 'Torque Y', 'Torque Z']

    if distribution:
        # Distribution of Forces
        plt.figure(figsize=(12, 6))
        plt.subplot(2, 1, 1)
        for i in range(3):
            plt.hist(sensor_data[:, i], bins=50, alpha=0.7, label=force_labels[i])
        plt.title('Distribution of Force Readings')
        plt.xlabel('Force (N)')
        plt.ylabel('Frequency')
        plt.legend()

        # Distribution of Torques
        plt.subplot(2, 1, 2)
        for i in range(3, 6):
            plt.hist(sensor_data[:, i], bins=50, alpha=0.7, label=torque_labels[i - 3])
        plt.title('Distribution of Torque Readings')
        plt.xlabel('Torque (Nm)')
        plt.ylabel('Frequency')
        plt.legend()

        plt.tight_layout()
        plt.show()

    if graph:
        # Time-series Plot for Forces
        plt.figure(figsize=(12, 6))
        plt.subplot(2, 1, 1)
        for i in range(3):
            plt.plot(sensor_data[:, i], label=force_labels[i])
        plt.title('Force Readings over Time')
        plt.xlabel('Time')
        plt.ylabel('Force (N)')
        plt.legend()

        # Time-series Plot for Torques
        plt.subplot(2, 1, 2)
        for i in range(3, 6):
            plt.plot(sensor_data[:, i], label=torque_labels[i - 3])
        plt.title('Torque Readings over Time')
        plt.xlabel('Time')
        plt.ylabel('Torque (Nm)')
        plt.legend()

        plt.tight_layout()
        plt.show()

# Example usage
# Update this relative path to the actual data file you want to use.
relative_path = 'data/raw/data_beuling_2/extraction_data_2024-05-21T17;41;46-33.json'
sensor_data = load_data_from_json(relative_path)
plot_data(sensor_data, distribution=True, graph=True)
