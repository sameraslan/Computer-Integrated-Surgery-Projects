import numpy as np
import pandas as pd

# Read a calbody.txt file. Output d,a,c arrays.

def read_calbody(file):
    calbody = pd.read_csv(file, sep=",", header=None).iloc[:, 0:3]
    N_d = int(calbody[:1][0][0])
    N_a = int(calbody[:1][1][0])
    N_c = int(calbody[:1][2][0])
    calbody = calbody[1:]
    d = np.array(calbody[:N_d])
    a = np.array(calbody[N_d:N_d+N_a])
    c = np.array(calbody[N_d+N_a:N_d+N_a+N_c])
    return d, a, c