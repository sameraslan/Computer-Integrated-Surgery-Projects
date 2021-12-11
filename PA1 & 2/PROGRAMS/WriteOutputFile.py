import os
import numpy as np
import pandas as pd

#Writes the output file for a given set of input data files (a,b,c, etc.).

#Required inputs:
#   name:       the unique part of the input data name (eg. debug-a, debug-c, unknown-j, etc.)
#   N_c:        number of em markers on the calibration object
#   N_frames:   number of frames (of calibration data)
#   P1:         estimated position of the calibration dimple from em data
#   P2:         estimated position of the calibration dimple from the optical data
#   C:          estimated positions of the em markers on the calibration object for each frame of data
#Expected outputs:
#   A txt file called pa1-{name}-output1.txt in the OUTPUT directory.

def write_output_file(name, N_c, N_frames, P1, P2, C):
    P1 = np.around(P1,2)
    P2 = np.around(P2,2)
    C = np.around(C,2)
    
    filename = "./OUTPUT/pa1-" + name + "-output1.txt"
    f = open(filename, "w+")
    f.write(str(N_c) + ", " + str(N_frames) + ", " + "pa1-" + name + "-output1.txt" + '\n')
    f.write(str(P1[0]) + ", " + str(P1[1]) + ", " + str(P1[2]) + '\n')
    f.write(str(P2[0]) + ", " + str(P2[1]) + ", " + str(P2[2]) + '\n')
    for c in C:
        for i in range(N_c):
            f.write(str(c[i][0]) + ", " + str(c[i][1]) + ", " + str(c[i][2]) + '\n')
    
    f.close()
