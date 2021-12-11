import numpy as np
from numpy.linalg import lstsq
from Frames import Frame

# Pivot calibration method described in class using numpy.linalg's built in least squares solver.
# 
# Required Inputs:
#   F:      Frame object F = (R,p)
# Expected Outputs:
#   6x1 vector x defined as x = [p_tx, p_ty, p_tz, p_dimplex, p_dimpley, p_dimplez] 

def pivot_calibration(F):
    #Here, we need to convert all the F_g[k] we passed into the method into a list of k (Num frames) rotations and translations.
    #We will then use those for our least squares solution. 
    A = []
    b = []
    for F_i in F:
        R_i = np.array(F_i.getR())
        p_i = np.array(F_i.getp())
        A.append(R_i[0])
        A.append(R_i[1])
        A.append(R_i[2])
        b.append(p_i)
    A = np.array(A)
    b = np.array(b).reshape(1,3*len(b))[0]*-1
    #Now to make a matrix I which is the negative of the identity matrix as we saw in class is concatenated to the rotation matrix.
    I = []
    for i in range(int(len(A)/3)):
        id = np.identity(3)*-1
        I.append(id[0])
        I.append(id[1])
        I.append(id[2])
    I = np.array(I)
    A = np.concatenate((A,I),axis=1)

    #Finally, We have an equation of the form Ax = b, which we can use np.linalg.lstsq to solve.
    #The answer will be a 6-vector, composed of 2 3-vectors, which are t_g and p_dimple respectively.

    x = lstsq(A,b,rcond=None)[0]
    x = np.array(x).reshape(6,)
    return x
    

    
