import json

def load_teeth_data(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data

def get_tooth_data(tooth_id, data):
    return data.get(tooth_id)

# Usage
data_path = './geometry/teeth_data.json'  # Adjust path as necessary
teeth_data = load_teeth_data(data_path)
tooth1_data = get_tooth_data('11', teeth_data)
print(tooth1_data)


# use the position vector and the rotation matrix to calculate the new force and torque vector of the tooth
