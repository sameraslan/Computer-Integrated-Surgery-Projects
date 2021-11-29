import numpy as np


# Finds Euclidian distance between two vectors
def magnitude_distance(a, b):
    return np.linalg.norm(a-b)