import numpy as np
import pandas as pd

# Returns resulting led_markers given specified body

def get_specified_sample(led_readings, k, body_desired):
    if body_desired == "A":
        return led_readings[k][:6]
    elif body_desired == "B":
        return led_readings[k][6:12]
    else:
        raise ModuleNotFoundError
