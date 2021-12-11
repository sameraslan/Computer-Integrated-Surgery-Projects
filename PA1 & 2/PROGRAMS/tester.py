import numpy as np
from Frames import Frame
from Adjusted_Coordinates import adjust_coordinates
from ReadCTFids import read_ctfids
from ReadEMFids import read_emfids
from ReadEmpivot import read_empivot
from numpy.linalg import lstsq, det
from Frames import frame_times_vector
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


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

def rigid_frame_estimate(v,M,n_frames):
    F = []
    for i in range(n_frames):
        R,p = rigid_transform_3D(v,M[i])
        F.append(Frame(R,p))
    return F    

p_tip = [-87.63746333, -45.71432872, -15.16765985]
ctfids_name = 'C:/Users/Colli/Documents/CIS/CIS-PA1/PA1/DATA/pa2-debug-a-ct-fiducials.txt'
emfids_name = 'C:/Users/Colli/Documents/CIS/CIS-PA1/PA1/DATA/pa2-debug-a-em-fiducialss.txt'
b = read_ctfids(ctfids_name)
G, N_frames_G = read_emfids(emfids_name)
g = adjust_coordinates(G[0])
#print(g)
F_g = rigid_frame_estimate(g,G,N_frames_G)
  
B = []
for F in F_g:
    B_i = frame_times_vector(F,p_tip)
    #print(B_i)
    #print(F.getR() @ p_tip + F.getp())
    B.append(B_i)
B = np.array(B)


<<<<<<< HEAD:PA1/PROGRAMS/tester.py
=======
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
    #print(A)
    #print(np.array(b))
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
    #print(A)
    #print(b)
    #Finally, We have an equation of the form Ax = b, which we can use np.linalg.lstsq to solve.
    #The answer will be a 6-vector, composed of 2 3-vectors, which are t_g and p_dimple respectively.

    x = lstsq(A,b,rcond=None)[0]
    x = np.array(x).reshape(6,)
    return x

empivot_name = 'C:/Users/Colli/Documents/CIS/CIS-PA1 & 2/PA1 & 2/DATA/pa2-debug-a-empivot.txt'
G, N_frames_em = read_empivot(empivot_name) 
g = adjust_coordinates(G[0])
F_g = rigid_frame_estimate(g,G,N_frames_em)
>>>>>>> 8b93ff585ad399046921481ec970bd4437b02443:PA1 & 2/PROGRAMS/tester.py

print("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")

print(B[:,2])
print(b/10)

fig = plt.figure(figsize=(20,20))

<<<<<<< HEAD:PA1/PROGRAMS/tester.py
ax = fig.add_subplot(111, projection='3d')
=======
ctfids_name = 'C:/Users/Colli/Documents/CIS/CIS-PA1 & 2/PA1 & 2/DATA/pa2-debug-a-ct-fiducials.txt'
emfids_name = 'C:/Users/Colli/Documents/CIS/CIS-PA1 & 2/PA1 & 2/DATA/pa2-debug-a-em-fiducialss.txt'
b = read_ctfids(ctfids_name)
Q,nframes = read_emfids(emfids_name)
print("Q")
print(Q)
g = adjust_coordinates(Q[0])
print(g)
F_q = (rigid_frame_estimate(g,Q,6))
for F in F_q:
    print(F.getR())
    print(det(F.getR()))
    print(F.getp())
    print()

G1 = F_q[0].getR() @ p_tip + F_q[0].getp()
G2 = F_q[1].getR() @ p_tip + F_q[1].getp()
G3 = F_q[2].getR() @ p_tip + F_q[2].getp()
G4 = F_q[3].getR() @ p_tip + F_q[3].getp()
G5 = F_q[4].getR() @ p_tip + F_q[4].getp()
G6 = F_q[5].getR() @ p_tip + F_q[5].getp()

G = np.array([G1,G2,G3,G4,G5,G6])
print(G)

empivot_name = 'C:/Users/Colli/Documents/CIS/CIS-PA1 & 2/PA1 & 2/DATA/pa2-debug-a-empivot.txt'
G, N_frames_em = read_empivot(empivot_name) 
g = adjust_coordinates(G[0])
F_g = rigid_frame_estimate(g,G,N_frames_em)
>>>>>>> 8b93ff585ad399046921481ec970bd4437b02443:PA1 & 2/PROGRAMS/tester.py

x = B[:,0]
y = B[:,1]
z = B[:,2]
plt.scatter(x,y,z)
plt.show()


plt.show()

R,p = rigid_transform_3D(B,b)
F_reg = Frame(R,p)
print(F_reg.getR())
print(F_reg.getp())

print(F_reg.getR() @ B[0] + F_reg.getp())
print(b[0])