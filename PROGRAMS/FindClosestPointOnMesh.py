import math

import numpy as np
import pandas as pd
from numpy.linalg import lstsq
from numpy.linalg import inv
from FindClosestPointTriangle import find_closest_point
from Magnitude import magnitude_distance

# Finds closest point on mesh
# Simple bounding box search


def find_closest_point_mesh(a, points, indices):
    lower = np.array([0, 0, 0]).T
    upper = np.array([0, 0, 0]).T
    c = [0, 0, 0]

    bound = float("Inf")  # Initialize inf

    num_triangles = len(indices)
    corners = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    for i in range(1, num_triangles):
        # Bound if statement for x, y, z abstracted w for loop
        bound_check = 0
        for j in range(3):
            if lower[j] - bound < a[j] < upper[j] + bound:
                bound_check += 1

        if bound_check == 3:
            corners[0] = points[indices[i][0]]
            corners[1] = points[indices[i][1]]
            corners[2] = points[indices[i][2]]

            #  3x3 matrix of Triangle corners for given triangle i
            corners = np.array(corners)

            h = find_closest_point(a, corners)  # returns 1x3 closest point to a given triangle's corners

            if magnitude_distance(h, a) < bound:  # if absolute value of distance less than bound
                c = h  # set closest point to c
                bound = magnitude_distance(h, a)

    return c
