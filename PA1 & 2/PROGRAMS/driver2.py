import sys
import numpy as np
from pandas.core import frame
from Frames import Frame
from Frames import frame_times_vector
from ReadCalbody import read_calbody
from ReadCalreadings import read_calreadings
from ReadEmpivot import read_empivot
from ReadCTFids import read_ctfids
from ReadEMFids import read_emfids
from ReadEMNav import read_emnav
from CalculateC_Exp import calculate_c_exp
from Adjusted_Coordinates import adjust_coordinates
from PivotCalibration import pivot_calibration
from RigidFrameEstimate import rigid_frame_estimate
from RigidFrameEstimate import rigid_transform_3D
from WriteOutputFilePA2 import write_output_file2
from Distortion import get_distortion_correction_function
from Distortion import undistort
#driver of all the code.

#Required Inputs: 
#   argv:   unique part of the file name (eg. debug-a, debug-c, unknown-i)

#Expected Outputs:
#   C_exp, P_dimple_em, P_dimple_opt, etc all listed in a txt file in the OUTPUT directory.

def main(argv):
    #Starting with Q4. This chunk of code will read calbody and calreadings into np arrays, so we can work with them easily.
    #The arrays are named according to the project description's conventions
    calbody_name = './DATA/pa2-' + argv[0] + '-calbody.txt'
    d,a,c = read_calbody(calbody_name)
    calreading_name = './DATA/pa2-' + argv[0] + '-calreadings.txt'
    D,A,C,N_frames = read_calreadings(calreading_name)

    #This small chunk of code will acquire the list of k Frames F_di and F_ai. (k is the number of frames)
    F_d = rigid_frame_estimate(d,D,N_frames)
    F_a = rigid_frame_estimate(a,A,N_frames)

    #This method call will calculate C_exp based on all of our previously acquired frames and data. Then I just reshape them to be stacked, instead of separated by frames.
    C_exp = calculate_c_exp(N_frames, F_d, F_a, c)
    C = C.reshape(1,len(C)*len(C[0]),3)[0]
    C_exp = C_exp.reshape(1,len(C_exp)*len(C_exp[0]),3)[0]
    vmin = np.min(C, axis=0)
    vmax = np.max(C, axis=0)

    #0. use C (distortion data) and C_exp (Ground truth) to get a distortion correction function c (c = 6^3 x 3 matrix)
    dist_correct_func = get_distortion_correction_function(C, C_exp, vmin, vmax)

    
    #1. use distortion_correction_function to fix G from empivot.txt, then redo pivot calibration, like in PA1 & 2, to get p_tip.
    empivot_name = './DATA/pa2-' + argv[0] + '-empivot.txt'
    G_empivot, N_frames_em = read_empivot(empivot_name) 
    G_empivot = undistort(dist_correct_func,G_empivot,vmin,vmax)
    g_empivot = adjust_coordinates(G_empivot[0])
    F_g_empivot = rigid_frame_estimate(g_empivot,G_empivot,N_frames_em)
    p_tip = pivot_calibration(F_g_empivot)[0:3]
    
    #2. read ct-fiducials to get b_i, which is data with respect to the ct-frame. Read em-fiducials and undistort to get F_g_i. Now do F_g_i * p_tip = B_i
    ctfids_name = './DATA/pa2-' + argv[0] + '-ct-fiducials.txt'
    emfids_name = './DATA/pa2-' + argv[0] + '-em-fiducialss.txt'
    b_ctfids = read_ctfids(ctfids_name)
    G_emfids, N_frames_G_emfids = read_emfids(emfids_name)
    G_emfids = undistort(dist_correct_func,G_emfids,vmin,vmax)
    g_emfids = adjust_coordinates(G_emfids[0])
    F_g_emfids = rigid_frame_estimate(g_emfids,G_emfids,N_frames_G_emfids)

    #Now do F_g_i * p_tip = B_i
    B_emfids = []
    for F_emfid in F_g_emfids:
        B_i_emfids = frame_times_vector(F_emfid,p_tip)
        B_emfids.append(B_i_emfids)
    B_emfids = np.array(B_emfids)

    #3. Now, we will use our values from B_emfids, as well as our values from b_ctfids to do a point cloud transformation to get F_reg such that F_reg * B_emfids = b_ctfids
    R_reg,p_reg = rigid_transform_3D(B_emfids,b_ctfids)
    F_reg = Frame(R_reg,p_reg)

    
    #4. Finally, repeat the whole process with em-nav.txt to get all the values for B_i again with this data. Now do F_reg * B_i = b_i to get coords in ct frame.
    em_nav_name = './DATA/pa2-' + argv[0] + '-EM-nav.txt'
    G_emnav, N_frames_G_emnav = read_emnav(em_nav_name)
    G_emnav = undistort(dist_correct_func,G_emnav,vmin,vmax)
    g_emnav = adjust_coordinates(G_emnav[0])
    F_g_emnav = rigid_frame_estimate(g_emnav,G_emnav,N_frames_G_emnav)  
    
    #Here we get the values for B_i
    B_emnav = []
    for F_emnav in F_g_emnav:
        B_i_emnav = frame_times_vector(F_emnav,p_tip)
        B_emnav.append(B_i_emnav)
    B_emnav = np.array(B_emnav)
    
    #Now we use our F_reg frame and apply it to the B_i we acquired to get the locations of the test points in ct coordinates.
    b_ctcoords = []
    for B_i_emcoords in B_emnav:
        print(B_i_emcoords)
        print(F_reg.getR())
        b_i_ctcoords = frame_times_vector(F_reg, B_i_emcoords)
        b_ctcoords.append(b_i_ctcoords)
    b_ctcoords = np.array(b_ctcoords)
    
    
    #5. output b into a txt file
    write_output_file2(argv[0], N_frames_G_emnav, b_ctcoords)


if __name__ == "__main__":
    main(sys.argv[1:])