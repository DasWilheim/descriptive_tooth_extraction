# make a low pass butterworth filter with a cutoff frequency of 1 Hz to filter out high frequency noise 
# from the sensor data from the measurement located in data/translated/${candadite}/filename.json
import numpy as np
import json
import os
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

def load_data_from_json(relative_path):
    # Construct an absolute path from a relative path
    script_dir = os.path.dirname(__file__)  # Directory of the current script
    project_root = os.path.abspath(os.path.join(script_dir, '../../'))  # Go up four levels to reach the project root

    file_path = os.path.join(project_root, relative_path)  # Construct the full file path
    
    
    with open(file_path, 'r') as file:
        data = json.load(file)

        print(data['tooth'])

        raw_forces = [data['translated_forces_x'], data['translated_forces_y'], data['translated_forces_z']]
        raw_torques = [data['translated_torques_x'], data['translated_torques_y'], data['translated_torques_z']]
        sensor_data = np.array(raw_forces + raw_torques).T
    return sensor_data


def butter_lowpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

