import numpy as np
import pandas as pd

#Read a calreadings.txt file. Output D,A,C arrays as well as N_frames integer.

def read_surfacemesh(file):
    # reads in first line of number of vertices as int
    num_vertices = (pd.read_csv(file, sep=" ", header=None, nrows=1))[0][0]

    # reads in vertices into (numVertices)
    vertices = pd.read_csv(file, sep=" ", header=None, skiprows=lambda x: x not in range(1, num_vertices + 1))

    # reads in number of triangles as int
    num_triangles = (pd.read_csv(file, sep=" ", header=None, skiprows=lambda x: x not in [num_vertices + 1]))[0][0]

    # reads in triangles into 3135 (numTriangles) x 6 dataframe
    vertices = pd.read_csv(file, sep=" ", header=None,
                           skiprows=lambda x: x not in range(num_vertices + 2, num_triangles + num_vertices + 2))

    # modifies vertices to get only first 3 columns which is the vertex coordinates of the triangles as pandas dataframe
    triangle_vertex_coords = vertices[[0, 1, 2]]

    print(triangle_vertex_coords)

    # N_D = int(calreadings[:1][0][0])
    # N_A = int(calreadings[:1][1][0])
    # N_C = int(calreadings[:1][2][0])
    # N_frames = int(calreadings[:1][3][0])
    # calreadings = calreadings.iloc[:, 0:3]
    # calreadings = calreadings[1:]
    # D = []
    # A = []
    # C = []
    #
    # N_tot = N_D + N_A + N_C
    # for i in range(N_frames):
    #     start = i*N_tot
    #     d = np.array(calreadings[start:start+N_D])
    #     a = np.array(calreadings[start+N_D:start+N_D+N_A])
    #     c = np.array(calreadings[start + N_D+N_A: start + N_D+N_A+N_C])
    #     D.append(d)
    #     A.append(a)
    #     C.append(c)
    # D = np.array(D)
    # A = np.array(A)
    # C = np.array(C)
    return num_vertices
