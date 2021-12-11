import os
import numpy as np

#Writes the output file for a given set of input data files (a,b,c, etc.).

#Required inputs:
#   name:       the unique part of the input data name (eg. debug-a, debug-c, unknown-j, etc.)
#   N_c:        number of frames of em-nav data
#   g_i:        estimated positions of p_tip in ct frame
#Expected outputs:
#   A txt file called pa1-{name}-output1.txt in the OUTPUT directory.

def write_output_file2(name, N_frames, g):
    g = np.around(g,2)
    filename = "./OUTPUT/pa2-" + name + "-output2.txt"
    f = open(filename, "w+")
    f.write(str(N_frames) + ", " + "pa2-" + name + "-output2.txt" + '\n')
    for g_i in g:
        f.write(str(g_i[0]) + ", " + str(g_i[1]) + ", " + str(g_i[2]) + '\n')
    
    f.close()