# CIS-PA3
INSTRUCTIONS FOR USE:
    1) Navigate to the folder that contains the PROGRAMS directory. It should also include the DATA folder (on the same level as PROGRAMS)
    2) your input argument to the command should just be running the driver:
        python ./PROGRAMS/driver.py
    Running the program allows all files to be run in one go. 
    IMPORTANT*** The folder that contains all of the input data has to be called DATA in order for our relative path to work. This folder should be at the same level as the PROGRAMS and OUTPUT folder in the directory structure. 

PROGRAMS:

    driver.py:
        The executable file. Very little mathematical logic. This file just calls methods that read data and do calculations, and writes the output txt file.

    FindClosestPointOnMeshLinear.py:
        Linear search for closest point on the mesh using a variable bound; iterates through all triangles

    FindClosestPointTriangle.py:
        Given some triangle and a point a, find the closest point on the triangle, whether on the edge or inside

    Frames.py:
        Our Frame library. This library lets you create frames with R, and p as inputs, get a Frames R and/or p values, invert a frame, compose two frames, and multiply a frame by a vector.

    GetSpecifiedSampleReading.py:
        Given a frame k, A/B, and specific sample reading, get the sample reading matrix of that part

    Magnitude.py:
        Returns the norm of difference of two vectors

    ReadBody.py:
        Reads in the two rigid bodies A and B

    ReadSampleReadings.py:
        Reads in the sample readings of the led markers into aik and bik

    ReadSurfaceMesh.py:
        Reads in triangle indices and coordinates for mesh surface

    RigidTransform.py:
        This file has two methods: rigid_frame_estimate just creates an array of frames using the results of rigid_transform_3d takes two arrays of vectors and computes an estimate for the transformation F = (R,p) between them. It uses svd, and returns (R,p) of the estimate.