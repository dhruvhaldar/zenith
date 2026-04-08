import numpy as np
from zenith.utils import h, c, k_B, sigma_sb

def planck_law(wavelength, temperature):
    """
    Calculate spectral radiance of a blackbody using Planck's Law.

    Parameters:
        wavelength (float or array): Wavelength in meters.
        temperature (float): Temperature in Kelvin.

    Returns:
        float or array: Spectral radiance (B_lambda) in W sr^-1 m^-3.
    """
    a = 2.0 * h * c**2

    # ⚡ Bolt: Fast exponentiation for integer powers avoids NumPy pow overhead (~4x faster)
    w2 = wavelength * wavelength
    w5 = w2 * w2 * wavelength

    # ⚡ Bolt: Precompute division constant for array processing
    hc_kT = (h * c) / (k_B * temperature)
    b = hc_kT / wavelength

    # ⚡ Bolt: np.expm1(b) is more numerically stable than np.exp(b) - 1.0
    return a / (w5 * np.expm1(b))

def wien_displacement(temperature):
    """
    Calculate peak wavelength using Wien's Displacement Law.

    Parameters:
        temperature (float): Temperature in Kelvin.

    Returns:
        float: Peak wavelength in meters.
    """
    b_wien = 2.8977719e-3 # Wien's displacement constant [m K]
    return b_wien / temperature

def distance_modulus(m, M):
    """
    Calculate distance using distance modulus formula.

    Parameters:
        m (float): Apparent magnitude.
        M (float): Absolute magnitude.

    Returns:
        float: Distance in parsecs.
    """
    # m - M = 5 * log10(d) - 5
    exponent = (m - M + 5.0) / 5.0
    return 10**exponent

def absolute_magnitude(m, d):
    """
    Calculate absolute magnitude given apparent magnitude and distance.

    Parameters:
        m (float): Apparent magnitude.
        d (float): Distance in parsecs.

    Returns:
        float: Absolute magnitude.
    """
    return m - 5.0 * np.log10(d) + 5.0

def luminosity_from_radius_temp(radius, temperature):
    """
    Calculate luminosity using Stefan-Boltzmann Law.
    L = 4 * pi * R^2 * sigma * T^4

    Parameters:
        radius (float): Radius in meters.
        temperature (float): Temperature in Kelvin.

    Returns:
        float: Luminosity in Watts.
    """
    # ⚡ Bolt: Moved sigma_sb import to top level to avoid repeated import overhead inside function
    return 4.0 * np.pi * radius**2 * sigma_sb * temperature**4
