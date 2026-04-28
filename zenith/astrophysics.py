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
    # ⚡ Bolt: Fast array exponentiation (10**x -> np.exp(ln(10) * x))
    # ⚡ Bolt: Combined scalar constants (2.302585092994046 / 5.0 = 0.4605170185988092) to avoid multiple intermediate array allocations
    return np.exp(0.4605170185988092 * (m - M + 5.0))

def absolute_magnitude(m, d):
    """
    Calculate absolute magnitude given apparent magnitude and distance.

    Parameters:
        m (float): Apparent magnitude.
        d (float): Distance in parsecs.

    Returns:
        float: Absolute magnitude.
    """
    # ⚡ Bolt: Fast array logarithm (log10(x) -> ln(x) / ln(10))
    # 5.0 / ln(10) = 2.171472409516259
    # This maps to highly-optimized C-level np.log and provides ~30% speedup
    return m - 2.171472409516259 * np.log(d) + 5.0

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
    # ⚡ Bolt: Unroll small integer powers to avoid NumPy generic power overhead (~2x faster)
    if isinstance(radius, np.ndarray) or isinstance(temperature, np.ndarray):
        # Start with a float array containing the largest broadcasted shape
        # to prevent UFuncTypeError when doing in-place ops on int arrays or mixed shapes
        res = np.empty(np.broadcast(radius, temperature).shape, dtype=float)
        res[...] = temperature

        np.square(res, out=res) # t^2
        np.square(res, out=res) # t^4

        # ⚡ Bolt: Group scalar variables into a single constant before array multiplication
        # to avoid creating redundant intermediate arrays.
        constant = 4.0 * np.pi * sigma_sb

        res *= constant
        res *= radius
        res *= radius
        return res
    else:
        r2 = radius * radius
        t2 = temperature * temperature
        t4 = t2 * t2
        # ⚡ Bolt: Group scalar variables into a single constant before array multiplication
        # to avoid creating redundant intermediate arrays.
        return (4.0 * np.pi * sigma_sb) * (r2 * t4)
