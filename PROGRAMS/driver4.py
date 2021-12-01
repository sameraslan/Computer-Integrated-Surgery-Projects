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
    file_choices = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J']
    file_choices = ['A']

    # For files A-J except I
    for file_choice in file_choices:

        # initialize file name to remove later warning due to ifs below
        sample_reading_debug = ''

        # Files A-F
        if 64 < ord(file_choice) < 71:
            sample_reading_debug = './DATA/PA3-' + file_choice + '-Debug-SampleReadingsTest.txt'
        # Files G-J
        elif 70 < ord(file_choice) < 75:
            sample_reading_debug = './DATA/PA3-' + file_choice + '-Unknown-SampleReadingsTest.txt'
        else:
            print("Incorrect command line argument (must be capital A-H or J)")
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
        file_output_name = 'PA3-' + file_choice + '-Output.txt'
        f = open(file_output_name, "w+")
        f.write(str(num_sampleframes) + " " + file_output_name + '\n')

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

            # 5. Assume F_reg = I for problem 4 as initial guess; sk (sample points) = F_reg * dk
            #    F_reg is essentially initial transformation T0
            identity_R = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
            F_reg = Frame(identity_R, np.array([0, 0, 0]))
            sk = frame_times_vector(F_reg, dk)

            # 6. ck = point on surface mesh closest to sk
            ck = find_closest_point_mesh_linear(sk, vertex_coords, triangle_indices)

            # Find magnitude of difference between dk and ck
            mag_dk_ck = np.around(magnitude_distance(dk, ck), 3)

            # Round to (nearest even if .005) two decimals places
            #ck = np.around(ck, 2)
            #dk = np.around(dk, 2)


            points_remaining = len(dk)

            maximum_iterations = 100
            threshold = .0001

            # Vectorized threshold and true array
            threshold_F = threshold * np.ones((1, 12))

            nu_naut = 100

            # Instead of while not converged do, we use a set number of iterations and check for convergence internally
            for iteration in range(maximum_iterations):
                # this is the closest point on the mesh
                z = 1

                sk = frame_times_vector(F_reg, dk)
                keep_index = 1

                # Re-initialize A and B
                A = []
                B = []
                e = []

                # for each sample frame
                for sample in range(num_sampleframes):
                    ck = find_closest_point_mesh_linear(sk, vertex_coords, triangle_indices)

                    distance = magnitude_distance(ck, sk)

                    if distance < nu_naut:
                        A.append(dk)
                        B.append(ck)

                        e.append(distance)
                        keep_index += 1

                # Terminate iteration if len(A) == 0 since nu_naut may be too small
                if len(A) == 0:
                    break

                R_reg_after, p_reg_after = rigid_transform_3D(np.array(A), np.array(B))
                F_reg_after = Frame(R_reg_after, p_reg_after)

                # Get absolute value difference between new and old frame
                abs_frame_offset = abs_subtract_frames(F_reg_after, F_reg)

                # Vectorize and concatenate offset so comparison is easier
                offset_R = np.ndarray.flatten(abs_frame_offset.getR())
                offset_p = np.ndarray.flatten(abs_frame_offset.getp())
                abs_frame_offset = np.concatenate((offset_R, offset_p))

                # Check if this has converged or not; if less than threshold then converged and break
                # the < check returns a 1x12 array of booleans checking if each element is < threshold
                if np.alltrue(abs_frame_offset < threshold_F):
                    sk = frame_times_vector(F_reg_after, dk)
                    break

                F_reg = F_reg_after

                if (len(A) / points_remaining >= .9):
                    nu_naut = 3 * np.mean(e)
                    points_remaining = len(A)

            mag_sk_ck = np.around(magnitude_distance(sk, ck), 3)

            # 7. Write to output file
            f.write('%8.2f %8.2f %8.2f\t\t%8.2f %8.2f %8.2f\t%8.5s\n' % (sk[0], sk[1], sk[2], ck[0], ck[1], ck[2], str(mag_sk_ck)))

if __name__ == "__main__":
    main(sys.argv[1:])