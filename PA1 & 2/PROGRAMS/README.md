# CIS-PA2
INSTRUCTIONS FOR USE:
    1) Navigate to the folder that contains the PROGRAMS directory.
    2) your input argument to the command should be the unique part of the file name you want to run. For example:
        python PROGRAMS/driver2.py debug-a
        python PROGRAMS/driver2.py unknown-i
        python PROGRAMS/driver2.py debug-c
    You can't run the program with more than one file at once.
    IMPORTANT*** The folder that contains all of the input data has to be called DATA in order for my relative path to work. This folder should be at the same level as the PROGRAMS and OUTPUT forlder in the directory structure. 

PROGRAMS:
    driver2.py:
        The executable file. Very little mathematical logic. This file just calls methods that read data and do calculations, and calls the file that writes the output txt.
    
    Frames.py:
        Our Frame library. This library lets you create frames with R, and p as inputs, get a Frames R and/or p values, invert a frame, compose two frames, and multiply a frame by a vector.
    
    CalculateC_exp.py:
        Our file which calculates C_exp. Simply the result of F_d ^-1  * F_a  * c_i = C_i_exp. This method allows for multiple frames of data to be passed in at once, and will return a C_i_exp for each frame i. 
    
    Adjusted_Coordinates.py:
        This file essentially accomplishes Q 5a. You pass in an array of coordinates, this file takes the average of all of these coordinates, and returns the difference between each coordinate and the calculated average. 

    PivotCalibration.py:
        This file takes in a array of Frames (F[k]) and does a pivot calibration using a least squares method. It returns the vector that contains p_tip and p_dimple.

    RigidFrameEstimate.py:
        This file has two methods: rigid_frame_estimate just creates an array of frames using the results of rigid_transform_3d takes two arrays of vectors and computes an estimate for the transformation F = (R,p) between them. It uses svd, and returns (R,p) of the estimate.

    Distortion.py:
        This file has two methods. get_distortion_correction_fucntion is just called once per run. It is the initial calculation of the distortion function c that is used to undistort data throughout. The undistort method takes in a distortion dataset and uses c to undistort it. 

