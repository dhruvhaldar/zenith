import pytest
from zenith.cosmology import recession_velocity, lookback_time

def test_hubble_law():
    """Verifies recession velocity calculation v = H0 * d"""
    # For d = 10 Mpc and H0 = 70 km/s/Mpc
    v = recession_velocity(d_mpc=10, H0=70)
    assert abs(v - 700.0) < 1e-5

def test_lookback_time_small_z():
    """Verifies lookback time for small z (t ~ z/H0)"""
    # For small z=0.1, t ~ 0.1 / H0
    # H0 = 70 km/s/Mpc ~ 0.0715 Gyr^-1
    # 1/H0 ~ 13.9 Gyr
    # t ~ 0.1 * 13.9 ~ 1.39 Gyr

    t = lookback_time(z=0.1, H0=70.0, omega_m=0.3, omega_l=0.7)
    assert 1.3 < t < 1.5

def test_lookback_time_large_z():
    """Verifies lookback time for z=1.0"""
    # For z=1.0, lookback time is around 7-8 Gyr for standard cosmology
    t = lookback_time(z=1.0, H0=70.0, omega_m=0.3, omega_l=0.7)
    assert 7.0 < t < 9.0
