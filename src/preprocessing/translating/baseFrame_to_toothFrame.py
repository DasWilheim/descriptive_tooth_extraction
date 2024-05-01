import numpy as np
import json
import glob
import os

# Define paths to the directories and files
candidate = "van_riet"
data_directory = rf'C:\Users\wille\OneDrive\Documenten\Tu Delft\Msc, Robotics\Afstuderen\AMC\Coding\thesis\descriptive_tooth_extraction\data\raw\{candidate}'
tooth_data_path = r'C:\Users\wille\OneDrive\Documenten\Tu Delft\Msc, Robotics\Afstuderen\AMC\Coding\thesis\descriptive_tooth_extraction\src\geometry\teeth_data.json'
output_directory = r'C:\Users\wille\OneDrive\Documenten\Tu Delft\Msc, Robotics\Afstuderen\AMC\Coding\thesis\descriptive_tooth_extraction\data\translated'

# Create a specific directory for the candidate if it doesn't exist
candidate_output_directory = os.path.join(output_directory, candidate)
os.makedirs(candidate_output_directory, exist_ok=True)

# Load tooth data once since it is reused
with open(tooth_data_path, 'r') as file:
    tooth_data = json.load(file)

# Process each sensor data file that starts with 'extraction_data'
for sensor_data_path in glob.glob(os.path.join(data_directory, 'extraction_data*.json')):
    with open(sensor_data_path, 'r') as file:
        sensor_data = json.load(file)

    # Extract the values from the data object    
    quadrant = sensor_data["quadrant"]
    tooth = sensor_data["tooth"]
    element_fractured = sensor_data["element_fractured"]
    end_timestamp = sensor_data["end_timestamp"]
    epoxy_failed = sensor_data["epoxy_failed"]
    forceps_slipped = sensor_data["forceps_slipped"]
    format_version = sensor_data["format_version"]
    jaw_type = sensor_data["jaw_type"]
    nonrepresentative = sensor_data["nonrepresentative"]
    person_type = sensor_data["person_type"]
    post_extraction_notes = sensor_data["post_extraction_notes"]
    start_timestamp = sensor_data["start_timestamp"]

    # Form the key for accessing tooth data
    quadrant_key = f"Quadrant {quadrant}"
    tooth_key = str(tooth)

    # Extract the relevant tooth data
    coordinates = np.array([tooth_data[quadrant_key][tooth_key]["coordinates"]["x"],
                            tooth_data[quadrant_key][tooth_key]["coordinates"]["y"],
                            tooth_data[quadrant_key][tooth_key]["coordinates"]["z"]])

    rotation = np.array(tooth_data[quadrant_key][tooth_key]["rotation"])

    # Define sensor force and torque arrays
    forces = np.array([sensor_data["raw_forces_x"],
                       sensor_data["raw_forces_y"],
                       sensor_data["raw_forces_z"]])

    torques = np.array([sensor_data["raw_torques_x"],
                        sensor_data["raw_torques_y"],
                        sensor_data["raw_torques_z"]])

    # Initialize lists to store translated forces and torques
    translated_forces = []
    translated_torques = []

    # Compute translated forces and torques
    for i in range(len(forces[0])):
        force_vector = forces[:, i]
        torque_vector = torques[:, i]

        # Translate forces (just rotation)
        translated_force = rotation.dot(force_vector)
        translated_forces.append(translated_force.tolist())

        # Translate torques (rotation and translation correction)
        translated_torque = rotation.dot(torque_vector) - np.cross(coordinates, translated_force)
        translated_torques.append(translated_torque.tolist())

    # Prepare to save the results
    output_data = {
        "quadrant": quadrant,
        "tooth": tooth,
        "element_fractured": element_fractured,
        "start_timestamp": start_timestamp,
        "end_timestamp": end_timestamp,
        "epoxy_failed": epoxy_failed,
        "forceps_slipped": forceps_slipped,
        "format_version": format_version,
        "jaw_type": jaw_type,
        "nonrepresentative": nonrepresentative,
        "person_type": person_type,
        "post_extraction_notes": post_extraction_notes,
        "translated_forces_x": [f[0] for f in translated_forces],
        "translated_forces_y": [f[1] for f in translated_forces],
        "translated_forces_z": [f[2] for f in translated_forces],
        "translated_torques_x": [t[0] for t in translated_torques],
        "translated_torques_y": [t[1] for t in translated_torques],
        "translated_torques_z": [t[2] for t in translated_torques]
    }

    # Save to a new JSON file in the candidate's directory
    output_filename = os.path.basename(sensor_data_path).replace('extraction_data', 'translated_sensordata')
    output_path = os.path.join(candidate_output_directory, output_filename)
    with open(output_path, 'w') as file:
        json.dump(output_data, file, indent=4)

    print(f"Data translated and saved to: {output_path}")
