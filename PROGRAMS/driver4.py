import sys
import numpy as np
from ReadSurfaceMesh import read_surfacemesh
from ReadBody import read_body
from ReadSampleReadings import read_sample_readings
from FindClosestPointOnMeshLinear import find_closest_point_mesh_linear
from GetSpecifiedSampleReading import get_specified_sample
from Frame import Frame, compose_frames, frame_times_vector, abs_subtract_frames
from RigidTransform import rigid_transform_3D
from Magnitude import magnitude_distance

# This is the driver for PA3. For every file A-J, it goes through each sample
# frame k and calculates the respective dk and ck, outputting them to files as instructed.

def main(argv):
    surfacemesh_name = './DATA/Problem3MeshFile.sur'
    bodyA_name = './DATA/Problem3-BodyA.txt'
    bodyB_name = './DATA/Problem3-BodyB.txt'
    file_choices = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K']

    # For files A-K except I
    for file_choice in file_choices:

        # initialize file name to remove later warning due to ifs below
        sample_reading_debug = ''

        # Files A-F
        if 64 < ord(file_choice) < 71:
            sample_reading_debug = './DATA/PA4-' + file_choice + '-Debug-SampleReadingsTest.txt'
        # Files G-K
        elif 70 < ord(file_choice) < 76:
            sample_reading_debug = './DATA/PA4-' + file_choice + '-Unknown-SampleReadingsTest.txt'
        else:
            print("Incorrect command line argument (must be capital A-H or J/K)")
            exit(0)

        # 1. Read surface mesh
        # Below lines read the 3D surface mesh
        # Gets vertex coordinates and each triangle's respective vertices index
        vertex_coords, triangle_indices = read_surfacemesh(surfacemesh_name)

        # 2. Read Rigid Bodies A and B
        led_marker_coords_A, tip_coords_A = read_body(bodyA_name)
        led_marker_coords_B, tip_coords_B = read_body(bodyB_name)

        # 3. Read Sample Reading for some debug sample reading
        # Get data itself for sample_readings (returns 12x3 of A, B marker readings)
        sample_reading_debug_A, num_sampleframes = read_sample_readings(sample_reading_debug)

        # 4. For each sample frame k, get values of aik and bik
        #    Using point-cloud-to-point-cloud registration to determine poses Fak and Fbk
        #    rigid bodies with respect to the tracker
        file_output_name = 'PA4-' + file_choice + '-Output.txt'
        f = open(file_output_name, "w+")
        f.write(str(num_sampleframes) + " " + file_output_name + '\n')

        c_all = []
        d_all = []

        for k in range(num_sampleframes):
            # Find frame F_Ak
            aik = get_specified_sample(sample_reading_debug_A, k, "A")
            R_Ak, p_Ak = rigid_transform_3D(led_marker_coords_A, aik)
            F_Ak = Frame(R_Ak, p_Ak)

            # Find frame F_bk
            bik = get_specified_sample(sample_reading_debug_A, k, "B")
            R_Bk, p_Bk = rigid_transform_3D(led_marker_coords_B, bik)
            F_Bk = Frame(R_Bk, p_Bk)

            # Get position of pointer tip with respect to rigid body
            # dk gets (F_Bk)^-1 * F_Ak * A_tip
            dk = frame_times_vector(compose_frames(F_Bk.getInverse(), F_Ak), tip_coords_A)

            # 6. ck = point on surface mesh closest to sk
            ck = find_closest_point_mesh_linear(dk, vertex_coords, triangle_indices)

            c_all.append(ck)
            d_all.append(dk)

        # End of registration

        # Beginning of ICP

        # 1. Set threshold, max iterations, and F_reg initial guess as I
        s_all = []  # to remove later warning
        epsilon_prev = len(d_all)

        # Maximum number of iterations we found was 65, so 80 seems safe if this is run on other test data
        maximum_iterations = 75

        threshold = .00001  # 10^-5 as threshold found to be best without doing too many iterations
        # Vectorized threshold and true array
        threshold_F = threshold * np.ones((1, 12))

        # Assume F_reg = I for problem 4 as initial guess; sk (sample points) = F_reg * dk
        # F_reg is essentially initial transformation T0
        identity_R = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        F_reg = Frame(identity_R, np.array([0, 0, 0]))
        F_reg_after = F_reg

        nu_n = 100

        # 2. For every iteration
        # Instead of while not converged do, we use a set number of iterations and check for convergence internally
        for iteration in range(maximum_iterations):

            # 3. Do frame times vector to get sk given the previously found frame
            # Holds all sks
            s_all = []
            for dk in d_all:
                # For every sk add the frame transformation of dk to this array of sks
                s_all.append(frame_times_vector(F_reg_after, dk))


            # Re-initialize A and B, and hold distance in array if less than nu_naut
            A = []
            B = []
            distance_hold = []

            # 3. For each sample frame append to A and B if distance < nu_n
            # for each sample frame
            for sample in range(num_sampleframes):
                # Apply find closest point and set to ck
                c_all[sample] = find_closest_point_mesh_linear(s_all[sample], vertex_coords, triangle_indices)

                # Gets norm distance between ck, sk
                distance = magnitude_distance(c_all[sample], s_all[sample])

                # Valid match check
                if distance < nu_n:
                    # Subset of Q with valid matches
                    A.append(d_all[sample])

                    # Points on M corresponding to A
                    B.append(c_all[sample])

                    # Append to distance storage for possible tightening of nu_naut later
                    distance_hold.append(distance)

            # Terminate iteration if len(A) == 0 since nu_naut may be
            # too small for the distance
            if len(A) == 0:
                break

            # 4. We flatten A and B and then compare below
            # Flatten A and B
            A = np.concatenate(A).ravel().reshape(-1, 3)
            B = np.concatenate(B).ravel().reshape(-1, 3)

            # Create new F_reg from A and B
            R_reg_after, p_reg_after = rigid_transform_3D(A, B)
            F_reg_after = Frame(R_reg_after, p_reg_after)

            # Get absolute value difference between new and old frame
            abs_frame_offset = abs_subtract_frames(F_reg_after, F_reg)
            F_reg = F_reg_after  # Set next F_reg for comparison to current F_reg

            # Vectorize and concatenate offset so comparison is easier
            offset_R = np.ndarray.flatten(abs_frame_offset.getR())
            offset_p = np.ndarray.flatten(abs_frame_offset.getp())
            abs_frame_offset = np.concatenate((offset_R, offset_p))

            # Essentially doing quaternion in order to make the comparison work
            abs_frame_offset[0] = abs_frame_offset[0] - 1
            abs_frame_offset[4] = abs_frame_offset[0] - 1
            abs_frame_offset[8] = abs_frame_offset[0] - 1
            less_than_check = abs_frame_offset <= threshold_F

            # Check if this has converged or not; if less than threshold then converged and break
            # the < check returns a 1x12 array of booleans checking if each element is < threshold
            if np.alltrue(less_than_check):
                for dk in d_all:
                    # For every sk add the frame transformation of dk to this array of sks
                    s_all.append(frame_times_vector(F_reg_after, dk))
                break

            # If number of distances less than nu_naut is from more than 90% of sample frames
            # This is essentially the epsilon comparison from the lecture notes
            # Gamma <= epsilon_n / epsilon_n-1 <= 1
            # If this is true for less than 90% of sample frames then we don't change mu
            # Allowing us to get unstuck from local minima
            if .9 <= len(A) / epsilon_prev <= 1:
                # nu_n gets 3 * mean of distances that satisfied previous nu_naut check
                nu_n = 3 * np.mean(distance_hold)

                # Length of points that satisfied this previously becomes # of remaining points
                # Prevents ratio above from becoming greater than 1 for more than one iteration
                epsilon_prev = len(A)


        # 7. Write to output file
        for k in range(num_sampleframes):
            mag_sk_ck = float(np.around(magnitude_distance(s_all[k], c_all[k]), 3))
            sk = np.round(s_all[k], 2)
            ck = np.round(c_all[k], 2)
            f.write('%8.2f %8.2f %8.2f\t   %8.2f %8.2f %8.2f\t  %.3f\n' % (sk[0], sk[1], sk[2], ck[0], ck[1], ck[2], mag_sk_ck))

if __name__ == "__main__":
    main(sys.argv[1:])