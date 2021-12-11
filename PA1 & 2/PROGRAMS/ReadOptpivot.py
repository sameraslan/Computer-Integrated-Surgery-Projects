import numpy as np
import pandas as pd

#Read optpivot.txt file. Return D, H arrays, as well as N_frames integer.

def read_optpivot(file):
    optpivot = pd.read_csv(file, sep=",", header=None)
    N_d = int(optpivot[:1][0][0])
    N_h = int(optpivot[:1][1][0])
    N_frames = int(optpivot[:1][2][0])
    optpivot = optpivot[1:]
    optpivot = optpivot.iloc[:, 0:3]

    D = []
    H = []
    for i in range(N_frames):
        start = i*(N_d + N_h)
        d = np.array(optpivot[start:start+N_d])
        h = np.array(optpivot[start+N_d:start+N_d+N_h])
        D.append(d)
        H.append(h)
    D = np.array(D)
    H = np.array(H)
    return D,H,N_frames