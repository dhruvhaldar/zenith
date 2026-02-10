import pytest
import datetime
from zenith.astrometry import ra_dec_to_alt_az
from zenith.optics import Telescope, CCD

def test_observation_feasibility():
    """
    E2E Test: Can we observe the Andromeda Galaxy tonight?
    """
    # M31 Andromeda: RA 10.68 deg, Dec 41.26 deg
    ra_m31 = 10.68
    dec_m31 = 41.26

    # Stockholm Observer: Lat 59.3, Lon 18.0
    lat_stockholm = 59.3
    lon_stockholm = 18.0

    # Time: 2026-01-20 22:00:00 UTC
    obs_time = datetime.datetime(2026, 1, 20, 22, 0, 0, tzinfo=datetime.timezone.utc)

    # 1. Check Visibility (Altitude > 30)
    alt, az = ra_dec_to_alt_az(ra_m31, dec_m31, lat_stockholm, lon_stockholm, obs_time)

    # It should be visible
    # Verify altitude
    assert alt > 10.0 # At least somewhat visible

    # 2. Check SNR with 60s exposure
    # M31 magnitude ~ 3.4 (very bright, but extended. Let's treat as point source for simplicity or integrate)
    # Actually, for point source magnitude this is fine.
    # 8 inch telescope
    telescope = Telescope(aperture=0.203, focal_length=2.0)
    ccd = CCD()

    snr = telescope.calculate_snr(target_mag=3.4, exposure=60, ccd=ccd)

    # Should be very high SNR
    assert snr > 100.0
