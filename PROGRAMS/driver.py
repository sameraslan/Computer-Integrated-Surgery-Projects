import sys
import numpy as np
from ReadSurfaceMesh import read_surfacemesh
from ReadBody import read_body
from ReadSampleReadings import read_sample_readings
from FindClosestPointOnMesh import find_closest_point_mesh
from GetSpecifiedSampleReading import get_specified_sample
from Frame import Frame, compose_frames, frame_times_vector
from RigidTransform import rigid_transform_3D
from Magnitude import magnitude_distance

# driver for PA3.


def main(argv):
    surfacemesh_name = './DATA/Problem3MeshFile.sur'
    bodyA_name = './DATA/Problem3-BodyA.txt'
    bodyB_name = './DATA/Problem3-BodyB.txt'
    sample_reading_debug_A = './DATA/PA3-A-Debug-SampleReadingsTest.txt'

    # 1. Read surface mesh
    # Below lines read the 3D surface mesh
    # Gets vertex coordinates and each triangle's respective vertices index
    vertex_coords, triangle_indices = read_surfacemesh(surfacemesh_name)

    # 2. Read Rigid Bodies A and B
    led_marker_coords_A, tip_coords_A = read_body(bodyA_name)
    led_marker_coords_B, tip_coords_B = read_body(bodyB_name)

    # 3. Read Sample Reading for some debug sample reading
    # Get data itself for sample_readings (returns 12x3 of A, B marker readings)
    sample_reading_debug_A, num_sampleframes = read_sample_readings(sample_reading_debug_A)

    # 4. For each sample frame k, get values of aik and bik
    #    Using point-cloud-to-point-cloud registration to determine poses Fak and Fbk
    #    rigid bodies with respect to the tracker
    file_choice = 'A'
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

        # 5. Assume F_reg = I for problem 3; sk (sample points) = F_reg * dk
        F_reg = Frame(np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), np.array([0, 0, 0]))
        sk = frame_times_vector(F_reg, dk)

        # 6. ck = point on surface mesh closest to sk
        ck = find_closest_point_mesh(sk, vertex_coords, triangle_indices)

        # Find magnitude of difference between dk and ck
        mag_dk_ck = magnitude_distance(dk, ck)
        ck = np.around(ck, 2)
        dk = np.around(dk, 2)

        # 7. Write to output file
        f.write("\t" + str(dk[0]) + "\t" + str(dk[1]) + "\t" + str(dk[2]) + "\t" + "\t" +
                str(ck[0]) + "\t" + str(ck[1]) + "\t" + str(ck[2]) + "\t" + str(mag_dk_ck) + '\n')

if __name__ == "__main__":
    main(sys.argv[1:])