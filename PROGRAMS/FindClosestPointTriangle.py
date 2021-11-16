import numpy as np
import pandas as pd
from numpy.linalg import lstsq

# Finds closest point on triangle by solving least squares using numpy.linalg's lstsq method
# Given point a and triangle coordinates p, q, r find closest point

def find_closest_point(a, triangle_vertices):
    # Check if point inside triangle
    p, q, r = triangle_vertices[0], triangle_vertices[1], triangle_vertices[2]
    A = a - p
    B = lamb * (q - p)
    C = mu * (r - p)

    # Check if point on triangle border

    return vertices, triangle_vertex_coords
