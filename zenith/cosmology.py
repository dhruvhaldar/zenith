import math
import numpy as np
from functools import lru_cache
from scipy.integrate import quad
from zenith.utils import c, mpc_to_m, parsec

def recession_velocity(d_mpc, H0=70.0):
    """
    Calculate recession velocity using Hubble's Law.

    Parameters:
        d_mpc (float): Distance in Megaparsecs.
        H0 (float): Hubble constant in km/s/Mpc.

    Returns:
        float: Recession velocity in km/s.
    """
    return H0 * d_mpc

def redshift_from_velocity(v_km_s):
    """
    Calculate redshift from velocity (non-relativistic approximation).

    Parameters:
        v_km_s (float): Velocity in km/s.

    Returns:
        float: Redshift z.
    """
    c_km_s = c / 1000.0
    return v_km_s / c_km_s

# ⚡ Bolt: Cache expensive numerical integration results
# Lookback time calculation uses scipy.integrate.quad, which is computationally expensive.
# Caching avoids redundant integrations for frequently used redshift values and default parameters.
@lru_cache(maxsize=128)
def lookback_time(z, H0=70.0, omega_m=0.3, omega_l=0.7):
    """
    Calculate lookback time for a given redshift in a flat LambdaCDM model.

    Parameters:
        z (float): Redshift.
        H0 (float): Hubble constant in km/s/Mpc.
        omega_m (float): Matter density parameter.
        omega_l (float): Dark energy density parameter.

    Returns:
        float: Lookback time in Gyr (billion years).
    """
    # H0 in 1/Gyr
    # 1 Mpc = 3.086e19 km
    # H0 = 70 km/s/Mpc = 70 / 3.086e19 s^-1 = 2.268e-18 s^-1
    # 1 Gyr = 3.154e16 s
    # H0_Gyr = H0 * (1e9 * 365.25 * 24 * 3600) / (3.086e19)
    # Actually, simpler: 1/H0 in Gyr = 977.8 / h (where h = H0/100).
    # t_H = 1/H0 = 9.778 h^-1 Gyr.

    # Let's convert H0 to Gyr^-1
    # H0 [km/s/Mpc]
    # 1 Mpc = 3.0857e22 m
    # 1 km = 1e3 m
    # H0 [s^-1] = H0 * 1e3 / 3.0857e22
    h0_s = H0 * 1000.0 / (1e6 * parsec)
    h0_gyr = h0_s * (1e9 * 365.25 * 24 * 3600.0)

    # ⚡ Bolt: Use exact analytic solution with inverse hyperbolic functions
    # to eliminate computationally expensive numerical integration (quad).
    # age t(z) = (2 / (3 H0 sqrt(Omega_L))) * asinh( sqrt(Omega_L / Omega_M) * (1+z)^(-3/2) )
    if omega_m > 0 and omega_l > 0:
        t_age_0 = (2.0 / (3.0 * math.sqrt(omega_l))) * math.asinh(math.sqrt(omega_l / omega_m))
        t_age_z = (2.0 / (3.0 * math.sqrt(omega_l))) * math.asinh(math.sqrt(omega_l / omega_m) * ((1.0+z)**-1.5))
        result = t_age_0 - t_age_z
        return result / h0_gyr
    else:
        # Fallback to numerical integration for edge-case cosmologies (e.g., Matter-only or de Sitter universes)
        def integrand(x):
            x1 = 1.0 + x
            return 1.0 / (x1 * math.sqrt(omega_m * (x1 * x1 * x1) + omega_l))
        result, _ = quad(integrand, 0, z)
        return result / h0_gyr
