import pytest
import numpy as np
from zenith.exoplanets import TransitSimulator

def test_transit_simulation():
    """
    E2E Test: Simulate full exoplanet detection pipeline.
    """
    # Define a "Hot Jupiter" around a Sun-like star
    sim = TransitSimulator(R_star_solar=1.0, R_planet_earth=11.2, period_days=4)
    # R_planet = 11.2 Earth radii ~ Jupiter radius
    # Depth should be (R_p/R_s)^2
    # R_earth/R_sun ~ 0.009
    # R_jupiter/R_sun ~ 0.1
    # Depth ~ 0.01

    time, flux = sim.generate_light_curve(duration_hours=6)

    # Check minimum flux
    min_flux = np.min(flux)
    expected_depth = sim.depth

    assert abs((1.0 - min_flux) - expected_depth) < 1e-4

    # Check that flux recovers to 1.0
    assert flux[0] == 1.0
    assert flux[-1] == 1.0
