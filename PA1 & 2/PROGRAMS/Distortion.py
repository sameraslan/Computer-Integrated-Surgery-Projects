import numpy as np
import scipy.special
from numpy.linalg import lstsq


#INPUT  :   ONE Frame of coordinate data. 
#OUTPUT :   Scaled version of data from that frame
def scale_to_box(X,x_min,x_max):
    return (X - x_min)/(x_max - x_min)

#INPUT  :   N, degree of polynomial
#           k, index
#           p, the current point (x or y or z for current coordinate)
def Bernstein(N,k,p):
    return scipy.special.binom(N,k) * ((1-p)**(N-k)) * ((p)**(k))

# INPUT :   V = Distortion Data
#           U = Ground Truth Data
#OUTPUT :   6^3 x 3 matrix c, aka the distortion function coefficients. 
def get_distortion_correction_function(V,U,vmin,vmax):
    #Then, need to get a huge matrix F, with all the bernstein poly data from scale_to_box(V).
    F = []
    V = scale_to_box(V,vmin,vmax)
    for v in V:
        F_row = []
        for i in range(6):
            for j in range(6):
                for k in range(6):
                    F_ijk = Bernstein(5,i,v[0]) * Bernstein(5,j,v[1]) * Bernstein(5,k,v[2])
                    F_row.append(F_ijk)
        F.append(F_row)
    #Next, use least squares  (F*c = U) to get c. 
    c = lstsq(F,U,rcond=None)[0]
    return c

#Unistorts a frame using a distortion correction function, and the data, as well as the box corners vmin and vmax
def undistort_frame(c,F,vmin,vmax):
    X = scale_to_box(F,vmin,vmax)
    g_undistorted = []
    for x in X:
        #x  is a coordinate. We need the undistorted version of this coordinate.
        undistortion_sum = np.array([0,0,0])
        c_index = 0
        for i in range(6):
            for j in range(6):
                for k in range(6):
                    undistortion_sum = undistortion_sum + (c[c_index] * (Bernstein(5,i,x[0]) * Bernstein(5,j,x[1]) * Bernstein(5,k,x[2])))
                    c_index = c_index + 1
        g_undistorted.append(undistortion_sum)
    return np.array(g_undistorted)


def undistort(c, G, vmin,vmax):
    g_undistorted = []
    for G_i in G:
        g_undistorted.append(undistort_frame(c,G_i,vmin,vmax))
    g_undistorted = np.array(g_undistorted)
    return g_undistorted
