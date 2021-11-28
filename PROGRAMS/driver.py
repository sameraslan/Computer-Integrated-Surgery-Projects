import sys
import numpy as np
import pandas as pd
import math
from ReadSurfaceMesh import read_surfacemesh
from ReadBody import read_body
from ReadSampleReadings import read_sample_readings
from FindClosestPointTriangle import find_closest_point
from FindClosestPointOnMesh import find_closest_point_mesh
from GetSpecifiedSampleReading import get_specified_sample

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
    sample_reading_debug_A = './DATA/PA3-A-Debug-SampleReadingsTest.txt'

    # Below lines read the 3D surface mesh
    # Gets vertex coordinates and each triangle's respective vertices index
    vertex_coords, triangle_indices = read_surfacemesh(surfacemesh_name)

    led_marker_coords, tip_coords = read_body(bodyA_name)

    # Get data itself for sample_readings (returns 12x3 of A, B marker readings)
    sample_reading_debug_A, num_sampleframes = read_sample_readings(sample_reading_debug_A)

    # Get sample reading at k=1 frame and for A body
    #print(get_specified_sample(sample_reading_debug_A, 14, "B", num_sample_frames))

    # print(find_closest_point_mesh(vertex_coords[triangle_indices[0][0]], triangle_indices, vertex_coords))


if __name__ == "__main__":
    main(sys.argv[1:])