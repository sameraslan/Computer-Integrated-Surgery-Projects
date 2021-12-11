import numpy as np

# Get the new postions p_i of a set of coordinates defined as p_i = (original coordinate_i - average_of_each_coordinate)

#Required Inputs:
#   G:  The array of coordinates

#Expected Outputs:
#   g:  The new adjusted array of coordinates

def adjust_coordinates(G):
    total_G = [0,0,0]
    for i in G:
        total_G = total_G + i
    G_0 = total_G / len(G)
    g = []
    for i in G:
        g_i = i - G_0
        g.append(g_i)
    g = np.array(g)
    return g