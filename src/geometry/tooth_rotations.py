import numpy as np

def deg_to_rad(degrees):
    return np.deg2rad(degrees)

def rotation_matrix_z(angle):
    """Calculate the rotation matrix for a rotation around the z-axis."""
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
    ])

def rotation_matrix_x(angle):
    """Calculate the rotation matrix for a rotation around the x-axis."""
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [1, 0, 0],
        [0, c, -s],
        [0, s, c]
    ])

# Define the angles for each quadrant
angles = [
    [0., -19.4, -53., -57.5, -66.3, -79.7, -79.7, -95.6],
    [0., 19.4, 53., 57.5, 66.3, 79.7, 79.7, 95.6],
    [0, -19.7, -39.2, -67., -78., -78., -78., -90.],
    [0, 19.7, 39.15, 67., 78., 78., 78., 90.]
]

rotation_matrices = {}

# Calculate rotation matrices for each quadrant and tooth
for quadrant in range(1, 5):
    rotation_matrices[f'Quadrant {quadrant}'] = {}
    for tooth, angle in enumerate(angles[quadrant - 1], start=1):
        rad = deg_to_rad(angle)
        if quadrant in [1, 2]:
            rotation_matrices[f'Quadrant {quadrant}'][f'Tooth {tooth}'] = rotation_matrix_z(rad)
        else:
            rotation_matrices[f'Quadrant {quadrant}'][f'Tooth {tooth}'] = rotation_matrix_x(rad)

# Optionally, print the rotation matrices for each tooth
for quadrant, teeth in rotation_matrices.items():
    print(f"{quadrant}:")
    for tooth, matrix in teeth.items():
        print(f"{tooth}: \n{matrix}\n")

