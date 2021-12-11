import numpy as np
import pandas as pd
def read_emfids(filename):
    emfids = pd.read_csv(filename, sep=",", header=None).iloc[:, 0:4]
    N_G = int(emfids[:1][0][0])
    N_frames = int(emfids[:1][1][0])
    emfids = emfids[1:]
    G = []
    for i in range(N_frames):
        start = i*N_G
        g = np.array(emfids[start:start+N_G])
        G.append(g) 
    G = np.array(G)
    #print(float(G[0][0][2]))
    for f in G:
        for v in f:
            v[2] = float(v[2])
    #print(G)
    return G,N_frames