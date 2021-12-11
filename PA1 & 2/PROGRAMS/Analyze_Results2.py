import sys
import numpy as np
from numpy.lib.function_base import average
from numpy.linalg.linalg import norm
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
from numpy.linalg import norm

calbody_name = 'C:/Users/Colli/Documents/CIS/CIS-PA1 & 2/PA1 & 2/DATA/pa1-unknown-k-calbody.txt'
d, a, c = read_calbody(calbody_name)
calreading_name = 'C:/Users/Colli/Documents/CIS/CIS-PA1 & 2/PA1 & 2/DATA/pa1-unknown-k-calreadings.txt'
D, A, C, N_frames = read_calreadings(calreading_name)

# This small chunk of code will acquire the list of k Frames F_di and F_ai. (k is the number of frames)
F_d = rigid_frame_estimate(d, D, N_frames)
F_a = rigid_frame_estimate(a, A, N_frames)

# This method call will calculate C_exp based on all of our previously acquired frames and data.
C_exp = calculate_c_exp(N_frames, F_d, F_a, c)

results = []
for j in range(len(C_exp)):
    percent_diffs = []
    for i in range(len(C_exp[j])):
        a = C_exp[j][i]
        e = C[j][i]
        percent_difference = np.around(norm(a - e) / norm(e) * 100, 2)
        percent_diffs.append(percent_difference)
    results.append(percent_diffs)

counter = 0
for i in results:
    k = np.around(average(i), 3)
    results[counter] = k
    counter += 1
print(results)
print(average(results))

# Now to make a table of C_exp I guess
a = []
for i in range(len(C_exp)):
    for j in range(len(C_exp[i])):
        a.append(C_exp[i][j])
a = np.array(a)
# print(a)
m = [i % len(C_exp[0]) + 1 for i in range(N_frames * len(C_exp[0]))]
m = np.array(m)
n = [int(i / len(C_exp[0])) + 1 for i in range(N_frames * len(C_exp[0]))]

df = pd.DataFrame({'frame': n, 'marker': m, 'x': a[:, 0], 'y': a[:, 1], 'z': a[:, 2]})
summary = df.iloc[::10, :]
# summary.to_csv('unknown-k.csv',index=False)

empivot_name = 'C:/Users/Colli/Documents/CIS/CIS-PA1 & 2/PA1 & 2/DATA/pa1-unknown-k-empivot.txt'
G, N_frames_em = read_empivot(empivot_name)
g = adjust_coordinates(G[0])
optpivot_name = 'C:/Users/Colli/Documents/CIS/CIS-PA1 & 2/PA1 & 2/DATA/pa1-unknown-k-optpivot.txt'
D, H, N_frames_opt = read_optpivot(optpivot_name)
h = adjust_coordinates(H[0])

# This chunk of code will acquire frame estimates for F_g[k], F_h[k], as well as F_d[k] (again) and F_dh[k].
# Important to note: F_dh[k] is the composition of F_d[k] ^-1 and F_h[k]. This is because we go from the em tracker to the optical tracker.
F_g = rigid_frame_estimate(g, G, N_frames_em)
F_h = rigid_frame_estimate(h, H, N_frames_opt)
F_d = rigid_frame_estimate(d, D, N_frames_opt)
F_dh = []
for i in range(N_frames_opt):
    F_dh.append(compose_frames((F_d[i]).getInverse(), F_h[i]))

    # This small chunk of code will call the pivot calibration function to ultimately find P_dimple when we use 1) empivot, and 2) optpivot respectively.
P_dimple_em = pivot_calibration(F_g)[3:]
P_dimple_opt = pivot_calibration(F_dh)[3:]
print(P_dimple_em)
print(P_dimple_opt)