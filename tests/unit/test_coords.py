import pytest
import datetime
from zenith.astrometry import calculate_lst, ra_dec_to_alt_az

def test_lst():
    # Test LST for a known case (Greenwich, J2000 epoch)
    # J2000 epoch is 2000-01-01 12:00:00 UTC
    dt = datetime.datetime(2000, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
    lon = 0.0 # Greenwich
    lst = calculate_lst(lon, dt)
    # GMST at J2000.0 is roughly 18.697 hours = 280.46 degrees
    assert abs(lst - 280.46) < 1.0

def test_ra_dec_to_alt_az():
    # Test coordinate transformation
    # Example: Star at Zenith
    # If HA = 0 and Dec = Lat, then Alt = 90

    # Let's mock time such that LST = RA
    # Then HA = 0
    # Let's say RA = 100, LST = 100

    # We need to find a time that gives LST = 100 for lon = 0
    # This is tricky without inversion.

    # Instead, let's just calculate LST first
    dt = datetime.datetime(2025, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
    lon = 0.0
    lat = 45.0
    lst = calculate_lst(lon, dt)

    # Choose a star with RA = LST (so HA = 0)
    ra = lst
    dec = 45.0 # Equal to latitude

    alt, az = ra_dec_to_alt_az(ra, dec, lat, lon, dt)

    # Should be at Zenith (Alt=90)
    assert abs(alt - 90.0) < 0.1
