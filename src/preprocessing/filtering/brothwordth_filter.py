import numpy as np
import json
import glob
import os
from scipy.signal import butter, lfilter

# Set the directory paths and candidate
candidate = "van_riet"
translated_directory = r'C:\Users\wille\OneDrive\Documenten\Tu Delft\Msc, Robotics\Afstuderen\AMC\Coding\thesis\descriptive_tooth_extraction\data\translated\{}'.format(candidate)
filtered_directory = r'C:\Users\wille\OneDrive\Documenten\Tu Delft\Msc, Robotics\Afstuderen\AMC\Coding\thesis\descriptive_tooth_extraction\data\filtered\{}'.format(candidate)

# Ensure the filtered directory exists
os.makedirs(filtered_directory, exist_ok=True)

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

def butter_lowpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

# Filter specifications
fs = 700  # Sampling frequency
cutoff = 1  # Cutoff frequency in Hz
order = 5  # Order of the filter

# Prepare the filter coefficients
b, a = butter_lowpass(cutoff, fs, order=order)

# Process each translated data file
for file_path in glob.glob(os.path.join(translated_directory, '*.json')):
    original_data, sensor_data = load_data(file_path)
    sensor_data_filtered = lfilter(b, a, sensor_data, axis=0)

    # Update the original data dictionary with filtered data
    original_data.update({
        "translated_forces_x": sensor_data_filtered[:, 0].tolist(),
        "translated_forces_y": sensor_data_filtered[:, 1].tolist(),
        "translated_forces_z": sensor_data_filtered[:, 2].tolist(),
        "translated_torques_x": sensor_data_filtered[:, 3].tolist(),
        "translated_torques_y": sensor_data_filtered[:, 4].tolist(),
        "translated_torques_z": sensor_data_filtered[:, 5].tolist()
    })

    # Construct the output file path
    output_filename = os.path.basename(file_path)
    output_path = os.path.join(filtered_directory, output_filename)

    # Save the filtered data
    with open(output_path, 'w') as file:
        json.dump(original_data, file, indent=4)

    print(f"Filtered data saved to: {output_path}")
