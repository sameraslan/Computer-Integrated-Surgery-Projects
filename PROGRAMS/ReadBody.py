import numpy as np
import pandas as pd

# Reads surfacemesh file. Output the vertex coordinates for all of the triangles as np array
# and the indices of the vertices for each triangle

def read_body(file):
    # reads in first line of number of vertices as int
    num_markers = (pd.read_csv(file, sep=" ", header=None, nrows=1))[0][0]
    file_name = (pd.read_csv(file, sep=" ", header=None, nrows=1))[1][0]

    # reads in led marker coordinates using num_markers
    led_marker_coords = np.array(pd.read_csv(file, delim_whitespace=True, header=None, skiprows=lambda x: x not in range(1, num_markers + 1)))

    # reads in tip coordinates
    tip_coords = np.array(pd.read_csv(file, delim_whitespace=True, header=None,
                                    skiprows=lambda x: x in range(0, num_markers + 1)))

    return led_marker_coords, tip_coords[0]
