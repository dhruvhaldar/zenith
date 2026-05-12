import timeit
import datetime
import math
from zenith.astrometry import ra_dec_to_alt_az, calculate_lst
from datetime import timezone

time = datetime.datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
print(calculate_lst(18.0, time))

def calculate_lst_new(longitude, time):
    ts = time.timestamp()
    d = (ts / 86400.0) - 10957.5
    gmst = 280.46061837 + 360.98564736629 * d
    return (gmst + longitude) % 360.0

print(calculate_lst_new(18.0, time))
