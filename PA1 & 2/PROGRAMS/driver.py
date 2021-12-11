import sys
import numpy as np
import pandas as pd
import math
from Frames import frame_times_vector
from ReadCalbody import read_calbody
from ReadCalreadings import read_calreadings
from ReadEmpivot import read_empivot
from ReadOptpivot import read_optpivot
from CalculateC_Exp import calculate_c_exp
from Adjusted_Coordinates import adjust_coordinates
from PivotCalibration import pivot_calibration
from RigidFrameEstimate import rigid_frame_estimate
from WriteOutputFile import write_output_file
from Frames import Frame
from Frames import compose_frames

#driver of all the code.

#Required Inputs: 
#   argv:   unique part of the file name (eg. debug-a, debug-c, unknown-i)

#Expected Outputs:
#   C_exp, P_dimple_em, P_dimple_opt, etc all listed in a txt file in the OUTPUT directory.

def main(argv):
    #Starting with Q4. This chunk of code will read calbody and calreadings into np arrays, so we can work with them easily.
    #The arrays are named according to the project description's conventions
    calbody_name = './DATA/pa1-' + argv[0] + '-calbody.txt'
    d,a,c = read_calbody(calbody_name)
    calreading_name = './DATA/pa1-' + argv[0] + '-calreadings.txt'
    D,A,C,N_frames = read_calreadings(calreading_name)

    #This small chunk of code will acquire the list of k Frames F_di and F_ai. (k is the number of frames)
    F_d = rigid_frame_estimate(d,D,N_frames)
    F_a = rigid_frame_estimate(a,A,N_frames)

    #This method call will calculate C_exp based on all of our previously acquired frames and data.
    C_exp = calculate_c_exp(N_frames, F_d, F_a, c)

    
    #This chunk of code will read empivot and optpivot files and place relevant values into np arrays so we can work with them easily.
    #The arrays are named according to the project description's conventions.
    #Importantly, we have a new array for D. This is because the number of frames in D or data in the optpivot.txt file may differ from previously.
    empivot_name = './DATA/pa1-' + argv[0] + '-empivot.txt'
    G, N_frames_em = read_empivot(empivot_name)
    g = adjust_coordinates(G[0])
    optpivot_name = './DATA/pa1-' + argv[0] + '-optpivot.txt'
    D,H,N_frames_opt = read_optpivot(optpivot_name)
    h = adjust_coordinates(H[0])
    
    # This chunk of code will acquire frame estimates for F_g[k], F_h[k], as well as F_d[k] (again) and F_dh[k].
    # Important to note: F_dh[k] is the composition of F_d[k] ^-1 and F_h[k]. This is because we go from the em tracker to the optical tracker.
    F_g = rigid_frame_estimate(g,G,N_frames_em)
    F_h = rigid_frame_estimate(h,H,N_frames_opt)
    F_d = rigid_frame_estimate(d,D,N_frames_opt)
    F_dh = []
    for i in range(N_frames_opt):
        F_dh.append(compose_frames((F_d[i]).getInverse(),F_h[i]))
    
    #This small chunk of code will call the pivot calibration function to ultimately find P_dimple when we use 1) empivot, and 2) optpivot respectively.
    P_dimple_em = pivot_calibration(F_g)[3:]
    print(pivot_calibration(F_g)[0:3])
    P_dimple_opt = pivot_calibration(F_dh)[3:]

    #Finally, we'll call a method to wrap up C_exp, P_dimple_em, and P_dimple_opt into a .txt file.
    write_output_file(argv[0], len(C_exp[0]), N_frames, P_dimple_em, P_dimple_opt, C_exp)

if __name__ == "__main__":
    main(sys.argv[1:])

