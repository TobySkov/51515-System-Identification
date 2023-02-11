import numpy as np

def rpm_to_rad_per_s(rpm: np.ndarray):
    assert isinstance(rpm, np.ndarray)

    rad_per_s = np.zeros(len(rpm))

    for i, number in enumerate(rpm):
        rad_per_s[i] = ((2*np.pi)/60.0)*number

    return rad_per_s



