import timeit
import datetime
import math
from zenith.utils import deg_to_rad, rad_to_deg
from zenith.astrometry import calculate_lst
from datetime import timezone

def ra_dec_to_alt_az_old(ra, dec, lat, lon, time):
    lst = calculate_lst(lon, time)
    ha = (lst - ra) % 360.0
    ha_rad = deg_to_rad(ha)
    dec_rad = deg_to_rad(dec)
    lat_rad = deg_to_rad(lat)
    sin_alt = math.sin(dec_rad) * math.sin(lat_rad) + \
              math.cos(dec_rad) * math.cos(lat_rad) * math.cos(ha_rad)
    sin_alt = max(-1.0, min(1.0, sin_alt))
    alt_rad = math.asin(sin_alt)
    Y = -math.sin(ha_rad)
    X = math.tan(dec_rad) * math.cos(lat_rad) - math.sin(lat_rad) * math.cos(ha_rad)
    az_rad = math.atan2(Y, X)
    alt = rad_to_deg(alt_rad)
    az = rad_to_deg(az_rad)
    return alt, az % 360.0

def ra_dec_to_alt_az_new(ra, dec, lat, lon, time):
    lst = calculate_lst(lon, time)
    ha = (lst - ra) % 360.0
    ha_rad = math.radians(ha)
    dec_rad = math.radians(dec)
    lat_rad = math.radians(lat)
    sin_alt = math.sin(dec_rad) * math.sin(lat_rad) + \
              math.cos(dec_rad) * math.cos(lat_rad) * math.cos(ha_rad)
    sin_alt = max(-1.0, min(1.0, sin_alt))
    alt_rad = math.asin(sin_alt)
    Y = -math.sin(ha_rad)
    X = math.tan(dec_rad) * math.cos(lat_rad) - math.sin(lat_rad) * math.cos(ha_rad)
    az_rad = math.atan2(Y, X)
    alt = math.degrees(alt_rad)
    az = math.degrees(az_rad)
    return alt, az % 360.0

time = datetime.datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
print("Old:", timeit.timeit("ra_dec_to_alt_az_old(83.63, 22.01, 59.3293, 18.0686, time)", globals=globals(), number=100000))
print("New:", timeit.timeit("ra_dec_to_alt_az_new(83.63, 22.01, 59.3293, 18.0686, time)", globals=globals(), number=100000))
