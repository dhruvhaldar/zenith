import numpy as np
import matplotlib.pyplot as plt
from zenith.utils import c, h, rad_to_deg

class CCD:
    """
    Represents a CCD camera.
    """
    def __init__(self, pixel_size=3.76e-6, read_noise=1.5, dark_current=0.01, quantum_efficiency=0.8):
        """
        Parameters:
            pixel_size (float): Size of a pixel in meters.
            read_noise (float): Read noise in electrons/pixel.
            dark_current (float): Dark current in electrons/pixel/second.
            quantum_efficiency (float): Quantum efficiency (0-1).
        """
        self.pixel_size = pixel_size
        self.read_noise = read_noise
        self.dark_current = dark_current
        self.qe = quantum_efficiency

class Telescope:
    """
    Represents an optical telescope.
    """
    def __init__(self, aperture, focal_length):
        """
        Parameters:
            aperture (float): Diameter of the primary mirror/lens in meters.
            focal_length (float): Focal length in meters.
        """
        self.aperture = aperture
        self.focal_length = focal_length
        self.area = np.pi * (self.aperture / 2)**2

    def diffraction_limit(self, wavelength=550e-9):
        """
        Calculate the Rayleigh diffraction limit in arcseconds.

        Parameters:
            wavelength (float): Wavelength of light in meters.

        Returns:
            float: Resolution limit in arcseconds.
        """
        theta_rad = 1.22 * wavelength / self.aperture
        return rad_to_deg(theta_rad) * 3600.0

    def calculate_snr(self, target_mag, exposure, ccd, sky_mag=21.0):
        """
        Calculate Signal-to-Noise Ratio (CCD Equation).

        Parameters:
            target_mag (float): Apparent magnitude of the target.
            exposure (float): Exposure time in seconds.
            ccd (CCD): CCD camera object.
            sky_mag (float): Sky background magnitude per arcsec^2.

        Returns:
            float: Signal-to-Noise Ratio.
        """
        # Constants
        # Zero point flux (approximate for V-band) in photons/s/m^2
        ZERO_MAG_FLUX = 1.0e10

        # 1. Calculate Signal (S)
        # Flux from target
        # ⚡ Bolt: Fast array exponentiation (10**x -> np.exp(ln(10) * x)) provides ~2x speedup
        flux_target = ZERO_MAG_FLUX * np.exp(-0.9210340371976183 * target_mag)
        # Photons hitting the detector
        # ⚡ Bolt: Grouped scalar variables to calculate a constant factor before array multiplication to avoid creating intermediate arrays
        photons_target = flux_target * (self.area * exposure * ccd.qe)

        # 2. Calculate Noise
        # a. Shot noise from target (sqrt(S))

        # b. Sky Background
        # Sky flux per arcsec^2
        # ⚡ Bolt: Fast array exponentiation
        flux_sky_arcsec = ZERO_MAG_FLUX * np.exp(-0.9210340371976183 * sky_mag)
        # Pixel scale in arcsec/pixel
        pixel_scale = 206265 * (ccd.pixel_size / self.focal_length)
        # Area of a pixel in arcsec^2
        # ⚡ Bolt: Use explicit multiplication to avoid small integer power overhead
        pixel_area_arcsec = pixel_scale * pixel_scale
        # Photons from sky per pixel
        # ⚡ Bolt: Grouped scalar variables to calculate a constant factor before array multiplication to avoid creating intermediate arrays
        photons_sky_pixel = flux_sky_arcsec * (self.area * exposure * ccd.qe * pixel_area_arcsec)
        # Assuming star light is concentrated in a certain number of pixels (aperture photometry)
        # Let's assume a seeing disk of roughly 2 arcsec diameter, area ~ pi*1^2 = 3.14 arcsec^2
        # Number of pixels for aperture
        n_pixels = 3.14 / pixel_area_arcsec
        if n_pixels < 1: n_pixels = 1

        total_sky_photons = photons_sky_pixel * n_pixels

        # c. Dark Current
        dark_electrons = ccd.dark_current * exposure * n_pixels

        # d. Read Noise
        # ⚡ Bolt: Use explicit multiplication
        read_noise_electrons = (ccd.read_noise * ccd.read_noise) * n_pixels

        # Total Noise
        # ⚡ Bolt: Combine scalar constant noise terms before array addition to avoid redundant array iterations
        constant_noise = total_sky_photons + dark_electrons + read_noise_electrons
        noise = np.sqrt(photons_target + constant_noise)

        return photons_target / noise

    def plot_performance_curve(self, mag_range, ccd, exposure=60, filename="snr_curve.png"):
        """
        Plot SNR vs Magnitude for a fixed exposure time.
        """
        mags = np.linspace(mag_range[0], mag_range[1], 50)
        # ⚡ Bolt: Vectorized SNR calculation over magnitude array to avoid slow Python loop
        snrs = self.calculate_snr(mags, exposure, ccd)

        plt.figure(figsize=(10, 6))
        plt.plot(mags, snrs, label=f"Exposure {exposure}s")
        plt.xlabel("Apparent Magnitude")
        plt.ylabel("Signal-to-Noise Ratio (SNR)")
        plt.title(f"Telescope Performance (D={self.aperture}m, f={self.focal_length}m)")
        plt.axhline(y=5, color='r', linestyle='--', label="Detection Limit (SNR=5)")
        plt.grid(True)
        plt.legend()
        plt.savefig(filename)
        plt.close()
