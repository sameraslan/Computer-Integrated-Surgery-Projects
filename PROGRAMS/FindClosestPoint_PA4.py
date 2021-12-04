import numpy as np
import pandas as pd
from numpy.linalg import lstsq
from numpy.linalg import inv

# Finds closest point on triangle by solving least squares using numpy.linalg's lstsq method
# Given point a and triangle coordinates p, q, r find closest point
# After following the course slides to implement this algorithm, we noticed that there was
# an edge case that was not accounted for. We still could not figure out the issue after rigorously debugging.
# Thus, we looked for other guidance online in order to ensure that we could still generate correct output for
# PA4

def find_closest_point(a, triangle_vertices):
    p, q, r = triangle_vertices[0], triangle_vertices[1], triangle_vertices[2]

    # Reference for the algorithm below: https://www.geometrictools.com/Documentation/DistancePoint3Triangle3.pdf
    first_edge = q - p
    second_edge = r - p
    v0 = p - a

    # Calculating dot products (a, b, c, d, e)
    dot_1 = np.dot(first_edge, first_edge)
    dot_2 = np.dot(first_edge, second_edge)
    dot_3 = np.dot(second_edge, second_edge)
    dot_4 = np.dot(first_edge, v0)
    dot_5 = np.dot(second_edge, v0)

    # Calculating determiner, s, and t as per the paper
    determiner = dot_1 * dot_3 - dot_2 * dot_2
    s = dot_2 * dot_5 - dot_3 * dot_4
    t = dot_2 * dot_4 - dot_1 * dot_5

    # Case 1
    if (s + t < determiner):
        if (s < 0):
            if (t < 0):
                # In region 4 according to graph
                if (dot_4 < 0):
                    s = max(0, min(1, -dot_4 / dot_1))
                    t = 0
                else:
                    s = 0
                    t = max(0, min(1, -dot_5 / dot_3))
            else:
                # In region 3 according to graph
                s = 0
                t = max(0, min(1, -dot_5 / dot_3))
        elif t < 0:
            # In region 5 according to graph
            s = max(0, min(1, -dot_4 / dot_1))
            t = 0
        else:
            # In region 0 according to graph
            inv_det = 1 / determiner
            s = s * inv_det
            t = t * inv_det
    # Case 2
    else:
        if s < 0:
            # In region 2 according to graph
            tmp0 = dot_2 + dot_4
            tmp1 = dot_3 + dot_5

            if tmp1 > tmp0:
                denom = dot_1 - 2 * dot_2 + dot_3
                numer = tmp1 - tmp0
                s = max(0, min(1, numer / denom))
                t = 1 - s
            else:
                t = max(0, min(1, -dot_5 / dot_3))
                s = 0
        elif t < 0:
            # In region 6 according to graph
            if dot_1 + dot_4 > dot_2 + dot_5:
                denom = dot_1 - 2 * dot_2 + dot_3
                numer = dot_3 + dot_5 - dot_2 - dot_4
                s = max(0, min(1, numer / denom))
                t = 1 - s
            else:
                s = max(0, min(1, -dot_5 / dot_3))
                t = 0
        else:
            # In region 1 according to graph
            denom = dot_1 - 2 * dot_2 + dot_3
            numer = dot_3 + dot_5 - dot_2 - dot_4
            s = max(0, min(1, numer / denom))
            t = 1 - s

    # Determine our closest point after determining correct p, s, t, first edge, and second edge above based on region
    closest_point = p + s * first_edge + t * second_edge

    return closest_point
