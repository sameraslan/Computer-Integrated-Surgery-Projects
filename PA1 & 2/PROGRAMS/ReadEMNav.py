import numpy as np
import pandas as pd

def read_emnav(filename):
    emnav = pd.read_csv(filename, sep=",", header=None)
    N_G = int(emnav[:1][0][0])
    N_frames = int(emnav[:1][1][0])
    emnav = emnav[1:]
    G = []
    for i in range(N_frames):
        start = i*N_G
        g = np.array(emnav[start:start+N_G])
        G.append(g) 
    G = np.array(G)
    for f in G:
        for v in f:
            v[2] = float(v[2])
    #print(G)
    return G,N_frames