import numpy as np
import json
import os

# Conversion from degrees to radians
def deg_to_rad(degrees):
    return np.deg2rad(degrees)



# rotation form base frame to frame 2 (frame for quadrant 1 and 2)
def rotation_1_to_2():
    return np.array([
        [0, 0, 1],
        [0, -1, 0],
        [1, 0, 0]
    ])

# Rotation matrices for rotations around z, x, and y axes
def rotation_matrix_z(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
    ])

def rotation_matrix_x(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [1, 0, 0],
        [0, c, -s],
        [0, s, c]
    ])

def rotation_matrix_y(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [c, 0, s],
        [0, 1, 0],
        [-s, 0, c]
    ])

# Angle data for each quadrant
angles = [
    [-3.89, -21.56, -50.7, -66.14, -73.35, -79.61, -90, -96.38],
    [3.64, 21.33, 47.38, 68.18, 73, 79.32, 86.18, 94.57],
    [3.72, -14.56, -41.67, -68.11, -72.38, -81.05, -87.66, -91.3],  #crooked 31 thats why it starts at 3.72
    [2.22, 7.11, 33.61, 62.67, 69.07, 77.39, 81.31, 92.55]
]

# Class for handling 3D vectors
class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def to_dict(self):
        return {"x": self.x, "y": self.y, "z": self.z}

# Compute tooth locations based on quadrant and tooth index
def tand_locatie(kwadrant, tand):
    tandvectors = [
        [
            Vector3(0.06311, -0.00415, 0.23629), 
            Vector3(0.06311, -0.01142, 0.2349), 
            Vector3(0.06311, -0.01734, 0.23075), 
            Vector3(0.06311, -0.02029, 0.22367), 
            Vector3(0.06311, -0.0229, 0.21683), 
            Vector3(0.06311, -0.02448, 0.2079), 
            Vector3(0.06311, -0.02575, 0.19759), 
            Vector3(0.06311, -0.02553, 0.18799)
        ],
        [
            Vector3(0.06311, 0.00483, 0.23623), 
            Vector3(0.06311, 0.01231, 0.23484), 
            Vector3(0.06311, 0.01753, 0.23132), 
            Vector3(0.06311, 0.01997, 0.22477), 
            Vector3(0.06311, 0.02315, 0.21791), 
            Vector3(0.06311, 0.02462, 0.20863), 
            Vector3(0.06311, 0.02653, 0.19819), 
            Vector3(0.06311, 0.02632, 0.18836)
        ],
        [
            Vector3(0.20887, 0.00299, 0.08229), 
            Vector3(0.20785, 0.00868, 0.08229), 
            Vector3(0.20505, 0.01414, 0.08229), 
            Vector3(0.19977, 0.01773, 0.08229), 
            Vector3(0.19292, 0.02031, 0.08229), 
            Vector3(0.18383, 0.02286, 0.08229), 
            Vector3(0.17332, 0.02488, 0.08379), 
            Vector3(0.16328, 0.02458, 0.08449)
        ],
        [
            Vector3(0.20886, -0.00246, 0.08229), 
            Vector3(0.20785, -0.00788, 0.08229), 
            Vector3(0.20555, -0.01341, 0.08229), 
            Vector3(0.20023, -0.01769, 0.08229), 
            Vector3(0.19307, -0.02056, 0.08229), 
            Vector3(0.18412, -0.02329, 0.08229), 
            Vector3(0.17332, -0.02471, 0.08379), 
            Vector3(0.16318, -0.02434, 0.08449)
        ]
    ]

    tooth_vector = tandvectors[kwadrant - 1][tand - 1]

    location =  tooth_vector 
    return location

# Creating dictionary to store data
teeth_data = {}
for quadrant in range(1, 5):
    teeth_data[f'Quadrant {quadrant}'] = {}
    for tooth in range(1, 9):
        rad = deg_to_rad(angles[quadrant - 1][tooth - 1])
        if quadrant in [1, 2]:
            rotation_matrix = rotation_1_to_2() @ rotation_matrix_x(rad)
        else:
            rotation_matrix = rotation_matrix_z(rad)
        
        location = tand_locatie(quadrant, tooth).to_dict()

        teeth_data[f'Quadrant {quadrant}'][f'{tooth}'] = {
            "coordinates": location,
            "rotation": rotation_matrix.tolist()
        }

# Save to JSON file

file_path = os.path.join(os.path.dirname(__file__), 'teeth_data.json')

with open(file_path, 'w') as file:
    json.dump(teeth_data, file, indent=4)

