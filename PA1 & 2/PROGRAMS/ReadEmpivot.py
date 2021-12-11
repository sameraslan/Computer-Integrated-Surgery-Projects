import numpy as np
import pandas as pd

#Read a empivot.txt file. Output G array, as well as N_frames integer.

def read_empivot(file):
    empivot = pd.read_csv(file, sep=",", header=None)
    N_Frames = int(empivot[:1][1][0])
    empivot = empivot[1:]
    e = np.array(empivot).astype(np.float)
    l = []
    for i in range(N_Frames):
        start = i*int(len(e)/N_Frames)        
        empi = e[start:start + int(len(e)/N_Frames)]
        l.append(empi)
    G = np.array(l)
    return G,N_Frames

