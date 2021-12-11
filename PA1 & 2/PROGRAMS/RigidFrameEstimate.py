from Frames import Frame
import numpy as np

#Rigid 3D 3D transformation method, as described in class. 
#   Required Inputs:
#       A:      Nx3 array of coordinates
#       B:      Nx3 array of coordinates
#   Expected Outputs:
#       R:      3x3 rotation matrix, calculated by SVD as the optimal rotation between A coords and B coords
#       p:      3x1 translation vector, calculated as the optimal translation between A and B coords

def rigid_transform_3D(A, B):

    # find mean column wise
    mean_A = np.mean(A.T, axis=1).reshape(-1, 1)
    mean_B = np.mean(B.T, axis=1).reshape(-1, 1)

    # subtract mean to get adjusted coordinates
    Ai = A.T - mean_A
    Bi = B.T - mean_B

    #I chose to name this matrix A because I've done a similar algorithm in Computer Vision where the input into an SVD algorithm is called 'A'. I think this matrix is analagous to that.
    A = Ai @ Bi.T
    A = A.astype(float)

    # find rotation
    U, S, Vt = np.linalg.svd(A)
    R = Vt.T @ U.T

    # special reflection case for when the determinant of R is -1
    if np.linalg.det(R) < 0:
        Vt[2, :] *= -1
        R = Vt.T @ U.T

    p = -R @ mean_A + mean_B
    p = np.array([p[0][0], p[1][0], p[2][0]])

    return R, p


# create a new Frame or list of Frames with the input coordinates needed for the transformation.
#
def rigid_frame_estimate(v,M,n_frames):
    F = []
    for i in range(n_frames):
        R,p = rigid_transform_3D(v,M[i])
        F.append(Frame(R,p))
    return F    