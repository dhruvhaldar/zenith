import numpy as np
import timeit

def bench1():
    time_hours = np.linspace(-3, 3, 1000)
    R_star = 6.957e8
    R_planet = 11.2 * 6.371e6
    v_orb = 2 * np.pi * 1.5e11 / (365.25 * 86400)

    inv_2R = 1.0 / (2 * R_planet)
    c1 = (R_star + R_planet) * inv_2R
    c2 = v_orb * inv_2R * 3600.0

    # Old
    flux = np.abs(time_hours)
    flux *= -c2
    flux += c1
    np.clip(flux, 0.0, 1.0, out=flux)

def bench2():
    time_hours = np.linspace(-3, 3, 1000)
    R_star = 6.957e8
    R_planet = 11.2 * 6.371e6
    v_orb = 2 * np.pi * 1.5e11 / (365.25 * 86400)

    inv_2R = 1.0 / (2 * R_planet)
    c1 = (R_star + R_planet) * inv_2R
    c2 = v_orb * inv_2R * 3600.0

    # New
    flux = np.abs(time_hours)
    flux *= -c2
    flux += c1
    np.clip(flux, 0.0, 1.0, out=flux)

print(timeit.timeit("bench1()", globals=globals(), number=10000))
