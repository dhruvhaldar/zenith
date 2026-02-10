"""
Zenith Utils: Physical and Astronomical Constants
"""

# Physical Constants
c = 2.99792458e8        # Speed of light in vacuum [m/s]
G = 6.67430e-11         # Gravitational constant [m^3 kg^-1 s^-2]
h = 6.62607015e-34      # Planck constant [J s]
k_B = 1.380649e-23      # Boltzmann constant [J/K]
sigma_sb = 5.670374e-8  # Stefan-Boltzmann constant [W m^-2 K^-4]

# Astronomical Constants
AU = 1.495978707e11     # Astronomical Unit [m]
parsec = 3.085677581e16 # Parsec [m]
light_year = 9.4607e15  # Light year [m]
solar_mass = 1.98847e30 # Solar mass [kg]
solar_radius = 6.957e8  # Solar radius [m]
earth_mass = 5.972e24   # Earth mass [kg]
earth_radius = 6.371e6  # Earth radius [m]
jupiter_radius = 7.1492e7 # Jupiter equatorial radius [m]
sun_lum = 3.828e26      # Solar luminosity [W]

def mpc_to_m(mpc):
    """Convert Megaparsecs to meters."""
    return mpc * 1e6 * parsec

def m_to_mpc(m):
    """Convert meters to Megaparsecs."""
    return m / (1e6 * parsec)

def rad_to_deg(rad):
    """Convert radians to degrees."""
    import math
    return rad * (180.0 / math.pi)

def deg_to_rad(deg):
    """Convert degrees to radians."""
    import math
    return deg * (math.pi / 180.0)
