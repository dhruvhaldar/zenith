import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from zenith.optics import Telescope, CCD

def main():
    # Define an 8-inch amateur telescope
    scope = Telescope(aperture=0.203, focal_length=2.0)
    camera = CCD(pixel_size=3.76e-6, read_noise=1.5, dark_current=0.01)

    # Calculate SNR for a Mag 12 star with 60s exposure
    snr = scope.calculate_snr(target_mag=12, exposure=60, ccd=camera)
    print(f"SNR for Mag 12 star (60s): {snr:.2f}")

    # Plot SNR vs Exposure Time
    output_path = os.path.join(os.path.dirname(__file__), '../public/assets/figure1.png')
    scope.plot_performance_curve(mag_range=[10, 18], ccd=camera, filename=output_path)
    print(f"Artifact generated: {output_path}")

if __name__ == "__main__":
    main()
