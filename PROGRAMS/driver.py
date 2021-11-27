import sys
import numpy as np
import pandas as pd
import math
from ReadSurfaceMesh import read_surfacemesh
from FindClosestPointTriangle import find_closest_point
from FindClosestPointOnMesh import find_closest_point_mesh

# driver for PA3.

# Required Inputs:
#   argv:   unique part of the file name (eg. debug-a, debug-c, unknown-i)

# Expected Outputs:
#   number of sample frames, xyz coordinates of d_k, xyz coordinates of c_k, magnitude difference,
#   etc all listed in a txt file in the OUTPUT directory.


def main(argv):
    surfacemesh_name = './DATA/Problem3MeshFile.sur'
    bodyA_name = './DATA/Problem3-BodyA.txt'
    bodyB_name = './DATA/Problem3-BodyA.txt'

    # Gets vertex coordinates and each triangle's respective vertices index
    vertex_coords, triangle_indices = read_surfacemesh(surfacemesh_name)
    print(find_closest_point_mesh(vertex_coords[triangle_indices[0][0]], triangle_indices, vertex_coords))


if __name__ == "__main__":
    main(sys.argv[1:])