import numpy as np
import pandas as pd

# Reads surfacemesh file. Output the vertex coordinates for all of the triangles as np array
# and the indices of the vertices for each triangle

def read_surfacemesh(file):
    # reads in first line of number of vertices as int
    num_vertices = (pd.read_csv(file, sep=" ", header=None, nrows=1))[0][0]

    # reads in vertices into (numVertices) the vertex coordinates for all of the triangles as np array
    vertices = np.array(pd.read_csv(file, sep=" ", header=None, skiprows=lambda x: x not in range(1, num_vertices + 1)))

    # reads in number of triangles as int
    num_triangles = (pd.read_csv(file, sep=" ", header=None, skiprows=lambda x: x not in [num_vertices + 1]))[0][0]

    # reads in triangles into 3135 (numTriangles) x 6 dataframe
    triangle_vertices = pd.read_csv(file, sep=" ", header=None,
                                    skiprows=lambda x: x not in range(num_vertices + 2, num_triangles + num_vertices + 2))

    # modifies vertices to get only first 3 columns which is the vertex coordinates of the triangles as np array
    # the indices of the vertices for each triangle
    triangle_vertex_coords = np.array(triangle_vertices[[0, 1, 2]])

    return vertices, triangle_vertex_coords
