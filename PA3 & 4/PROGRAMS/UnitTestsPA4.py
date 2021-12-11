import numpy as np
from Frame import Frame
from Frame import compose_frames
from Frame import frame_times_vector
from FindClosestPoint_PA4 import find_closest_point
import math

# Testing find_closest_point PA4 function
def test_find_closest_point(a, triangle_vertices, correct_c):
    if find_closest_point(a, triangle_vertices) != correct_c:
        return 0
    return 1

# Next, we test to make sure the frame creation is working
def test_frame_init(R, p):
    res = []
    # First is expected to work.
    try:
        f1 = Frame(R[0], p[0])
        res.append(1)
    except Exception as e:
        res.append(0)

    # second is expected to fail because of both r and p
    try:
        f1 = Frame(R[1], p[1])
        res.append(1)
    except Exception as e:
        res.append(0)

    # third is expected to succeed
    try:
        f1 = Frame(R[2], p[2])
        res.append(1)
    except Exception as e:
        res.append(0)

    # fourth is expected to fail because of r
    try:
        f1 = Frame(R[3], p[3])
        res.append(1)
    except Exception as e:
        res.append(0)

    # fifth is expected to fail because of p
    try:
        f1 = Frame(R[4], p[4])
        res.append(1)
    except Exception as e:
        res.append(0)

    expected = [1, 0, 1, 0, 0]

    return (res == expected)

# Testing to make sure that we get the rotational matrix correctly
def test_getR(R, t):
    frames = []
    for i in range(5):
        if i == 0 or i == 2:
            print(R[i])
            print(t[i])
            frames.append(Frame(R[i], t[i]))
            if (frames[i].getR().all() != R[i].all()):
                return 0
    return 1

# Testing to make sure that we get the translation component correctly
def test_getp(R, t):
    frames = []
    for i in range(5):
        frames.append(Frame(R[i], t[i]))
        if (frames[i].getp() != t[i]):
            return 0
    return 1

# Test that we get the inverse frame correctly
def test_invert_frame(F, F2, F3, F4):
    if F.getInverse().getR().all() != F3.getR().all():
        return 0
    if F.getInverse().getp().all() != F3.getp().all():
        return 0
    if F2.getInverse().getR().all() != F4.getR().all():
        return 0
    if F2.getInverse().getp().all() != F4.getp().all():
        return 0
    if F3.getInverse().getR().all() != F.getR().all():
        return 0
    if F3.getInverse().getp().all() != F.getp().all():
        return 0
    return 1

# Testing correct frame composition
def test_compose_frames(F1, F2, F3):
    return (compose_frames(F1, F2).getR().all() == F3.getR().all() and compose_frames(F1,
                                                                                      F2).getp().all() == F3.getp().all())

# Testing correct frame times vector result
def test_frame_times_vector(F1, F2, v1, v2, v3, v4, v5, v6):
    if frame_times_vector(F1, v1).all() != v3.all():
        return 0
    if frame_times_vector(F1, v2).all() != v4.all():
        return 0
    if frame_times_vector(F2, v1).all() != v5.all():
        return 0
    if frame_times_vector(F2, v2).all() != v6.all():
        return 0
    return 1

def main():
    rotations = np.array([
        # Good rotation

        np.array([[1, 0, 0],
                  [0, 1, 0],
                  [0, 0, 1]
                  ]),
        # Bad rotation

        np.array(
            [[0, 1, 1],
             [0, 1],
             [1]
             ]),
        # Good rotation
        np.array([
            [.5, .5, 0],
            [.5, .5, 0],
            [1, 1, .5]
        ]),
        # Bad rotation
        np.array([
            [1],
            [1],
            [1]
        ]),
        # Good rotation
        np.array([
            [0, 1, 0],
            [1, 0, 0]
        ])
    ])

    translations = np.array([
        # Good translation

        np.array([0, 0, 0]),

        # bad translation

        np.array([100, 200]),

        # Good translation

        np.array([1.6, 2.2, 4.3]),

        # Good translation

        np.array([1, -3, -5]),

        # bad translation

        np.array([0])
    ])

    # Good Frames for frame method tests
    F1 = Frame(np.array([
        [.866, .98, .25],
        [-.433, .5, .75],
        [-.1, -.866, .433]]),
        np.array([12.1, 23.983, 11.932]))
    F2 = Frame(np.array([
        [math.cos(31), 0, -math.sin(31)],
        [0, 1, 0],
        [math.sin(31), 0, math.cos(31)]]),
        np.array([62.1, 0, 42.82]))
    # True inverses, calculated by hand (and by hand I mean Wolfram Alpha)
    F1inv = Frame(np.array([
        [0.89607244, -0.66309361, 0.63118267],
        [0.11639526, 0.41386751, -0.78406339],
        [0.43973565, 0.67459562, 0.88711172]]),
        np.array([-2.47077415, -1.97872276, -32.0846451]))
    F2inv = Frame(np.array([
        [0.91474236, 0, -0.40403765],
        [0, 1, 0],
        [0.40403765, 0, 0.91474236]]),
        np.array([-39.50460845, 0, -64.26000554]))

    # Good vectors for frame method tests
    v1 = np.array([10, 10, 1])
    v2 = np.array([1, 12, -6])
    # True Frame vector compositions, calculated by hand
    F1v1 = np.array([30.81, 25.403, 2.705])
    F1v2 = np.array([23.226, 25.05, -1.158])
    F2v1 = np.array([71.65146122, 10, 39.6943659])
    F2v2 = np.array([60.59051649, 12, 36.92750821])

    # tests for initializing frames and getting frame params
    frame_init = test_frame_init(rotations, translations)
    # getR = test_getR(rotations,translations)
    # getp = test_getp(rotations,translations)

    # if(getR == 0 or getp == 0 or frame_init == 0):
    # print ("Test failed: frame initialization.")
    # else :
    # print("Frame initialization tests passed. :D")

    # test for inverting frames
    invert_frame = test_invert_frame(F1, F2, F1inv, F2inv)

    if (invert_frame == 0):
        print("Frame inverting test Failed")
    else:
        print("Frame invert tests passed!:)")

    # tests for composing frames
    true_F1F2 = Frame(np.array([
        [0.69115747, 0.98, 0.57858219], [-0.69911167, 0.5, 0.51110847], [-0.26642254, -0.866, 0.35567968]
    ]), np.array([76.5836, 29.2087, 24.26306]))
    compose_frame = test_compose_frames(F1, F2, true_F1F2)

    if (compose_frame == 0):
        print("Compose frames failed!")
    else:
        print("compose frames tests passed! :)")

    # test frame times vector
    frame_vector = test_frame_times_vector(F1, F2, v1, v2, F1v1, F1v2, F2v1, F2v2)

    if (frame_vector == 0):
        print("frame times vector failed!")
    else:
        print("frame times vector passed! :)")


    # test find_closest_point_PA4
    closest_point1 = test_find_closest_point([0.5, 0.2, 0.5], [[0, 0, 0], [0, 1, 0], [1, 1, 0]], [0.5, 0.2, 0])
    closest_point2 = test_find_closest_point([0, 0, 10], [[0, 0, 0], [0, 1, 0], [1, 1, 0]], [0, 0, 0])

    if (closest_point1 == 0):
        print("closest point failed!")
    else:
        print("closest point passed! :)")

    if (closest_point2 == 0):
        print("closest point2 failed!")
    else:
        print("closest point2 passed! :)")

if __name__ == "__main__":
    main()