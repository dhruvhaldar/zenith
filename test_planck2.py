import numpy as np
from zenith.astrophysics import planck_law

wavelengths = 500e-9
temp = np.array([5000.0, 6000.0])
try:
    print(planck_law(wavelengths, temp))
except Exception as e:
    print("ERROR:", repr(e))
