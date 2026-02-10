import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from zenith.exoplanets import TransitSimulator

def main():
    # Simulate a "Hot Jupiter" around a Sun-like star
    sim = TransitSimulator(R_star_solar=1.0, R_planet_earth=11.2, period_days=4)
    # 11.2 Earth Radii ~ Jupiter Radius

    # Generate light curve
    flux, time = sim.generate_light_curve(duration_hours=6)

    # Plot Light Curve
    output_path = os.path.join(os.path.dirname(__file__), '../public/assets/figure2.png')
    sim.plot_light_curve(duration_hours=6, filename=output_path)
    print(f"Artifact generated: {output_path}")

if __name__ == "__main__":
    main()
