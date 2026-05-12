import numpy as np
from zenith.astrophysics import absolute_magnitude

m_arr = np.array([10.0, 11.0, 12.0])
d_scalar = 10.0

try:
    print(absolute_magnitude(m_arr, d_scalar))
except Exception as e:
    print("ERROR:", repr(e))
