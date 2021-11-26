import numpy as np
import pandas as pd
from numpy.linalg import lstsq
from numpy.linalg import inv

# Finds closest point on triangle by solving least squares using numpy.linalg's lstsq method
# Given point a and triangle coordinates p, q, r find closest point

def find_closest_point(a, triangle_vertices):
    closest_point = np.array([0, 0, 0])  # instantiate and set later

    # Check if point inside triangle
    p, q, r = triangle_vertices[0], triangle_vertices[1], triangle_vertices[2]

    A = np.column_stack(((q - p).T, (r - p).T))  # 3x2 A
    b = (a - p).T  # 3x1 b

    x = inv(A.T @ A) @ A.T @ b
    x1 = lstsq(A, b, rcond=None)  # equivalent to above explicit solving

    lamb = x[0]  # lambda value solved for
    mu = x[1]  # mu value solved for

    c = p + lamb*(q-p) + mu*(r-p)  # possibly found point c (3x1) on triangle

    # find closest point on edge of traingle
    if lamb < 0:
        lamb_project = np.dot((c - r), (p - r)) / np.dot((p - r), (p - r))  # project_on_segment(c, r, p)
        lamb_seg = max(0, min(lamb_project, 1))
        closest_point = np.cross((r + lamb_seg), (p - r))

    elif mu < 0:
        lamb_project = np.dot((c - p), (q - p)) / np.dot((q - p), (q - p))  # project_on_segment(c, p, q)
        lamb_seg = max(0, min(lamb_project, 1))
        closest_point = np.cross((p + lamb_seg), (q - p))

    elif lamb + mu > 1:
        lamb_project = np.dot((c - q), (r - q)) / np.dot((r - q), (r - q))  # project_on_segment(c, q, r)
        lamb_seg = max(0, min(lamb_project, 1))
        closest_point = np.cross((q + lamb_seg), (r - q))

    # closest point is in center of triangle
    else:
        closest_point = c  # closest point c lies within the triangle

    return closest_point
