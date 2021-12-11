import numpy as np
import pandas as pd
import csv

def read_ctfids(filename):
    ct_fids = open(filename)
    next(ct_fids)
    g = []
    for line in ct_fids.readlines():
        x = float(line.split(",")[0])
        y = float(line.split(",")[1])
        z = float(line.split(",")[2])
        a = [x,y,z]
        g.append(a)
    g = np.array(g)
    return g   
    