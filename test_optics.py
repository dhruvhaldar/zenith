import numpy as np
from zenith.optics import Telescope, CCD

scope = Telescope(aperture=0.203, focal_length=2.0)
camera = CCD()

# Test scalar
snr_scalar = scope.calculate_snr(target_mag=12.0, exposure=60.0, ccd=camera)
print(f"Scalar SNR: {snr_scalar}")

# Test array
sky_mags = np.array([20.0, 21.0, 22.0])
snr_array = scope.calculate_snr(target_mag=12.0, exposure=60.0, ccd=camera, sky_mag=sky_mags)
print(f"Array SNR: {snr_array}")
