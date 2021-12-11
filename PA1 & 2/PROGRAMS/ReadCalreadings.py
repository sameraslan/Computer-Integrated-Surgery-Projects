import numpy as np
import pandas as pd

#Read a calreadings.txt file. Output D,A,C arrays as well as N_frames integer.

def read_calreadings(file):
    calreadings = pd.read_csv(file, sep=",", header=None).iloc[:, 0:4]
    N_D = int(calreadings[:1][0][0])
    N_A = int(calreadings[:1][1][0])
    N_C = int(calreadings[:1][2][0])
    N_frames = int(calreadings[:1][3][0])
    calreadings = calreadings.iloc[:, 0:3]
    calreadings = calreadings[1:]
    D = []
    A = []
    C = []

    N_tot = N_D + N_A + N_C
    for i in range(N_frames):
        start = i*N_tot
        d = np.array(calreadings[start:start+N_D])
        a = np.array(calreadings[start+N_D:start+N_D+N_A])
        c = np.array(calreadings[start + N_D+N_A: start + N_D+N_A+N_C])
        D.append(d)
        A.append(a)
        C.append(c)
    D = np.array(D)
    A = np.array(A)
    C = np.array(C)
    return D,A,C,N_frames