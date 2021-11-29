import numpy as np
import pandas as pd

# Reads sample readings file. Outputs led markers and the number of sample frames

def read_sample_readings(file):
    # reads in first line of number of vertices as int
    num_leds = (pd.read_csv(file, sep=",", header=None, nrows=1))[0][0]
    num_sample_frames = (pd.read_csv(file, sep=",", header=None, nrows=1))[1][0]
    file_name = (pd.read_csv(file, sep=",", header=None, nrows=1))[2][0]

    # creates 3d numpy array of nsamps set of num_ledsx3 matrices
    led_markers = np.zeros((num_sample_frames, num_leds - 4, 3))

    # sets each 2d matrix of A body, B body, and unneeded tracker coordinates
    for i in range(num_sample_frames):
        led_markers[i] = np.delete(np.array(pd.read_csv(file, sep=",", header=None,
                             skiprows=lambda x: x not in range(i * num_leds + 1, (i+1) * num_leds + 1))),
                                   (12, 13, 14, 15), axis=0)

    return led_markers, num_sample_frames
