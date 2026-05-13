import math
import timeit

def orig():
    ha_rad, dec_rad, lat_rad = 0.5, 0.5, 0.5
    sin_alt = math.sin(dec_rad) * math.sin(lat_rad) + \
              math.cos(dec_rad) * math.cos(lat_rad) * math.cos(ha_rad)
    sin_alt = max(-1.0, min(1.0, sin_alt))
    alt_rad = math.asin(sin_alt)

    Y = -math.sin(ha_rad)
    X = math.tan(dec_rad) * math.cos(lat_rad) - math.sin(lat_rad) * math.cos(ha_rad)

    az_rad = math.atan2(Y, X)
    return alt_rad, az_rad

def opt():
    ha_rad, dec_rad, lat_rad = 0.5, 0.5, 0.5
    sin_dec = math.sin(dec_rad)
    cos_dec = math.cos(dec_rad)
    sin_lat = math.sin(lat_rad)
    cos_lat = math.cos(lat_rad)
    sin_ha = math.sin(ha_rad)
    cos_ha = math.cos(ha_rad)

    sin_alt = sin_dec * sin_lat + cos_dec * cos_lat * cos_ha
    sin_alt = max(-1.0, min(1.0, sin_alt))
    alt_rad = math.asin(sin_alt)

    Y = -sin_ha
    X = (sin_dec / cos_dec) * cos_lat - sin_lat * cos_ha

    az_rad = math.atan2(Y, X)
    return alt_rad, az_rad

print("Orig:", timeit.timeit(orig, number=1000000))
print("Opt:", timeit.timeit(opt, number=1000000))
