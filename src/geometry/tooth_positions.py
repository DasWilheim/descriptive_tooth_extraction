import math

class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

def tand_locatie(kwadrant, tand):
    tandvectors = [
        [Vector3(0.0395, 0.249, 0), Vector3(0.226, 0.0623, 0)],
        [Vector3(0.0332, -0.00759, 0.00336), Vector3(0.0336, -0.0101, 0.011), Vector3(0.0344, -0.0133, 0.0189), Vector3(0.0321, -0.0225, 0.0193), Vector3(0.0321, -0.0295, 0.0232), Vector3(0.0311, -0.0371, 0.0241), Vector3(0.0308, -0.0481, 0.0253), Vector3(0.0299, -0.0583, 0.0258)],
        [Vector3(0.0332, -0.00759, -0.00336), Vector3(0.0336, -0.0101, -0.011), Vector3(0.0344, -0.0133, -0.0189), Vector3(0.0321, -0.0225, -0.0193), Vector3(0.0321, -0.0295, -0.0232), Vector3(0.0311, -0.0371, -0.0241), Vector3(0.0308, -0.0481, -0.0253), Vector3(0.0299, -0.0583, -0.0258)],
        [Vector3(-0.0131, 0.0261, -0.00207), Vector3(-0.0136, 0.0263, -0.00779), Vector3(-0.0164, 0.0264, -0.0135), Vector3(-0.0225, 0.0225, -0.0155), Vector3(-0.0291, 0.0237, -0.0189), Vector3(-0.0383, 0.0226, -0.0214), Vector3(-0.0494, 0.0225, -0.0211), Vector3(-0.0602, 0.0229, -0.0228)],
        [Vector3(-0.0131, 0.0261, 0.00207), Vector3(-0.0136, 0.0263, 0.00779), Vector3(-0.0164, 0.0264, 0.0135), Vector3(-0.0225, 0.0225, 0.0155), Vector3(-0.0291, 0.0237, 0.0189), Vector3(-0.0383, 0.0226, 0.0214), Vector3(-0.0494, 0.0225, 0.0211), Vector3(-0.0602, 0.0229, 0.0228)]
    ]
    # base_correction = Vector3(-0.002, -0.0025, 0) if kwadrant in [1, 2] else Vector3(-0.005, -0.002, 0)
    center_correction = Vector3(0, 0.018, 0)

    base_vector = tandvectors[0][0 if kwadrant in [1, 2] else 1]
    tooth_vector = tandvectors[kwadrant][tand - 1]
    location = base_vector + tooth_vector + center_correction
    return location

# Test the function by printing locations for each tooth in each quadrant
for quadrant in range(1, 5):
    print(f"Quadrant {quadrant}:")
    for tooth in range(1, 9):
        loc = tand_locatie(quadrant, tooth)
        print(f"Tooth {tooth}: {loc}")
