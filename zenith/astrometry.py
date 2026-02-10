import numpy as np
from datetime import datetime, timezone
from zenith.utils import deg_to_rad, rad_to_deg

def calculate_lst(longitude, time):
    """
    Calculate Local Sidereal Time (LST) in degrees.

    Parameters:
        longitude (float): Observer's longitude in degrees (East is positive).
        time (datetime): UTC datetime object.

    Returns:
        float: LST in degrees [0, 360).
    """
    # Julian Date calculation
    # J2000 epoch is 2000-01-01 12:00:00 UTC
    # JD at J2000 = 2451545.0

    # Calculate JD
    # Python datetime timestamp is seconds since 1970-01-01 00:00:00 UTC
    # JD of 1970-01-01 is 2440587.5
    ts = time.replace(tzinfo=timezone.utc).timestamp()
    jd = (ts / 86400.0) + 2440587.5

    # Days since J2000
    d = jd - 2451545.0

    # Greenwich Mean Sidereal Time (GMST) in degrees
    # Approximate formula
    gmst = 280.46061837 + 360.98564736629 * d
    gmst = gmst % 360.0

    # Local Sidereal Time
    lst = gmst + longitude
    return lst % 360.0

def ra_dec_to_alt_az(ra, dec, lat, lon, time):
    """
    Convert Right Ascension/Declination to Altitude/Azimuth.

    Parameters:
        ra (float): Right Ascension in degrees.
        dec (float): Declination in degrees.
        lat (float): Observer's latitude in degrees.
        lon (float): Observer's longitude in degrees.
        time (datetime): UTC datetime object.

    Returns:
        tuple: (altitude, azimuth) in degrees.
    """
    lst = calculate_lst(lon, time)
    ha = (lst - ra) % 360.0 # Hour Angle in degrees

    # Convert to radians
    ha_rad = deg_to_rad(ha)
    dec_rad = deg_to_rad(dec)
    lat_rad = deg_to_rad(lat)

    # Altitude
    sin_alt = np.sin(dec_rad) * np.sin(lat_rad) + \
              np.cos(dec_rad) * np.cos(lat_rad) * np.cos(ha_rad)
    alt_rad = np.arcsin(sin_alt)

    # Azimuth
    # cos(Az) = (sin(Dec) - sin(Alt)sin(Lat)) / (cos(Alt)cos(Lat))
    # Using atan2 for better quadrant handling
    # tan(Az) = -sin(HA)cos(Dec) / (sin(Dec)cos(Lat) - sin(Lat)cos(Dec)cos(HA)) -> wait this formula is tricky.

    # Standard spherical trig for Az:
    # sin(Az) = - sin(HA) * cos(Dec) / cos(Alt)
    # cos(Az) = (sin(Dec) - sin(Lat) * sin(Alt)) / (cos(Lat) * cos(Alt))

    # Let's use the explicit atan2 form:
    # Y = -sin(H)
    # X = tan(delta)cos(phi) - sin(phi)cos(H)
    # Az = atan2(Y, X)

    Y = -np.sin(ha_rad)
    X = np.tan(dec_rad) * np.cos(lat_rad) - np.sin(lat_rad) * np.cos(ha_rad)

    az_rad = np.arctan2(Y, X)

    # Convert back to degrees
    alt = rad_to_deg(alt_rad)
    az = rad_to_deg(az_rad)

    return alt, az % 360.0

def calculate_airmass(altitude):
    """
    Calculate airmass using simple approximation (sec(z)).

    Parameters:
        altitude (float): Altitude in degrees.

    Returns:
        float: Airmass (approximate).
    """
    if altitude <= 0:
        return float('inf')

    zenith_angle_rad = deg_to_rad(90.0 - altitude)
    # Simple secant approximation: X = sec(z)
    # Better approximation for low altitudes: Young's or Pickering's
    # Using simple secant for now as per "introductory" scope, but let's add a clamp
    return 1.0 / np.cos(zenith_angle_rad)
