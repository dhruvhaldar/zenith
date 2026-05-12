import numpy as np
from zenith.astrophysics import planck_law

wavelengths = np.array([500e-9, 600e-9])
temp = 5000.0
try:
    print(planck_law(wavelengths, temp))
except Exception as e:
    print("ERROR:", repr(e))
