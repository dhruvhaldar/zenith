import numpy as np
import matplotlib.pyplot as plt
from zenith.utils import G, solar_mass, solar_radius, AU, earth_radius, jupiter_radius

class TransitSimulator:
    """
    Simulate exoplanet transit light curves.
    """
    def __init__(self, R_star_solar=1.0, R_planet_earth=1.0, period_days=365.25, M_star_solar=1.0):
        """
        Parameters:
            R_star_solar (float): Radius of the star in Solar Radii.
            R_planet_earth (float): Radius of the planet in Earth Radii.
            period_days (float): Orbital period in days.
            M_star_solar (float): Mass of the star in Solar Masses.
        """
        self.R_star = R_star_solar * solar_radius
        self.R_planet = R_planet_earth * earth_radius
        self.period = period_days * 86400.0 # seconds
        self.M_star = M_star_solar * solar_mass

        # Calculate semi-major axis using Kepler's 3rd Law
        # a^3 = G * M * T^2 / (4 * pi^2)
        self.a = (G * self.M_star * self.period**2 / (4 * np.pi**2))**(1.0/3.0)

        # Orbital velocity (assuming circular)
        self.v_orb = 2 * np.pi * self.a / self.period

        # Transit depth
        self.depth = (self.R_planet / self.R_star)**2

        # Duration (full transit chord, center to center)
        # T = 2 * R_star / v_orb (approx for edge-on)
        self.duration = 2 * (self.R_star + self.R_planet) / self.v_orb

    def generate_light_curve(self, duration_hours=6, points=1000):
        """
        Generate a synthetic light curve.

        Parameters:
            duration_hours (float): Total time window to simulate.
            points (int): Number of data points.

        Returns:
            tuple: (time_hours, normalized_flux)
        """
        t_half = duration_hours * 3600.0 / 2.0
        time = np.linspace(-t_half, t_half, points)
        flux = np.ones_like(time)

        # Impact parameter b=0 (edge-on)
        # Distance from star center as function of time
        # x(t) = v * t
        x = self.v_orb * time

        # Simple geometric overlap model (uniform disk star)
        # If |x| < R_star + R_planet: partial or full transit
        # If |x| < R_star - R_planet: full transit

        for i, val in enumerate(x):
            dist = abs(val)
            if dist > (self.R_star + self.R_planet):
                flux[i] = 1.0
            elif dist < (self.R_star - self.R_planet):
                # Full transit
                flux[i] = 1.0 - self.depth
            else:
                # Ingress/Egress
                # Simplified linear interpolation for "introductory" model
                # Overlap fraction approx
                overlap = (self.R_star + self.R_planet - dist) / (2 * self.R_planet)
                flux[i] = 1.0 - self.depth * overlap

        return time / 3600.0, flux

    def plot_light_curve(self, duration_hours=6, filename="transit_light_curve.png"):
        """
        Plot the light curve.
        """
        time, flux = self.generate_light_curve(duration_hours)

        plt.figure(figsize=(10, 6))
        plt.plot(time, flux, 'b-', label='Model')

        # Add some noise for realism
        noise = np.random.normal(0, 0.0001, len(time))
        plt.plot(time, flux + noise, 'k.', alpha=0.3, label='Simulated Data')

        plt.xlabel("Time from mid-transit (hours)")
        plt.ylabel("Normalized Flux")
        plt.title(f"Exoplanet Transit (P={self.period/86400:.1f}d, Depth={self.depth:.4f})")
        plt.legend()
        plt.grid(True)
        plt.savefig(filename)
        plt.close()
