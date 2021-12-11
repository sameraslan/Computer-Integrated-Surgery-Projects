import numpy as np
from Frames import Frame
from Frames import compose_frames
from Frames import frame_times_vector

#Calculates a list of length N_frames of coordinates for the markers on the calibration object. The calculation is defined as C_exp_i = F1_i^-1 * F2_i * c_i.

#Required Inputs:
#   N_frames:       integer number of frames of data included in the data files.
#   F1:             first frame used in the calculation (F_d in the context of the assignment)
#   F2:             second frame used in the calculation (F_a in the assignment)
#   c:              vector used in calculation. (c in the assignment)

#Expected Outputs:
#   C_exp:          list[N_frames] of C_exp calculations.

def calculate_c_exp(N_frames, F1, F2, c):
    C_exp = []
    for i in range(N_frames):
        C_i = []
        for j in range(c.shape[0]):
            C_i.append(frame_times_vector(compose_frames(F1[i].getInverse(),F2[i]), c[j]))
        C_exp.append(C_i)
    C_exp = np.array(C_exp)
    return C_exp