import numpy as np
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

    def integrand(x):
        return 1.0 / ((1.0 + x) * np.sqrt(omega_m * (1.0 + x)**3 + omega_l))

    result, error = quad(integrand, 0, z)

    return result / h0_gyr
