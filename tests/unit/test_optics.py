import pytest
from zenith.optics import Telescope, CCD

def test_diffraction_limit():
    # 2.4m telescope (Hubble size)
    # Wavelength 500nm
    t = Telescope(aperture=2.4, focal_length=57.6)
    limit = t.diffraction_limit(wavelength=500e-9)
    # Theta = 1.22 * 500e-9 / 2.4 = 2.54e-7 rad
    # In arcsec: 2.54e-7 * 206265 = 0.052 arcsec
    assert abs(limit - 0.052) < 0.01

def test_snr_calculation():
    # 8 inch telescope
    t = Telescope(aperture=0.203, focal_length=2.0)
    ccd = CCD()
    snr = t.calculate_snr(target_mag=10, exposure=10, ccd=ccd)
    assert snr > 0
    # Brighter star should have higher SNR
    snr_bright = t.calculate_snr(target_mag=5, exposure=10, ccd=ccd)
    assert snr_bright > snr
