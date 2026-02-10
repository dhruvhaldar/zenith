import os
import sys
import datetime
import numpy as np
import matplotlib.pyplot as plt

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from zenith.astrometry import ra_dec_to_alt_az

def main():
    # Stockholm Observer
    lat = 59.3293
    lon = 18.0686

    # Target: Sirius (RA ~6.75h, Dec ~-16.7deg)
    # RA in degrees: 6.75 * 15 = 101.25
    ra = 101.28
    dec = -16.7161

    # Date: 2026-01-20
    start_time = datetime.datetime(2026, 1, 20, 16, 0, 0, tzinfo=datetime.timezone.utc)

    times = [start_time + datetime.timedelta(minutes=m) for m in range(0, 800, 10)]
    alts = []

    for t in times:
        alt, az = ra_dec_to_alt_az(ra, dec, lat, lon, t)
        alts.append(alt)

    time_hours = [(t - start_time).total_seconds() / 3600.0 for t in times]

    plt.figure(figsize=(10, 6))
    plt.plot(time_hours, alts, label='Sirius')
    plt.axhline(y=0, color='black', linestyle='-', label='Horizon')
    plt.axhline(y=30, color='r', linestyle='--', label='Airmass < 2')

    plt.xlabel(f"Hours from {start_time.strftime('%H:%M UTC')}")
    plt.ylabel("Altitude (degrees)")
    plt.title(f"Visibility of Sirius from Stockholm ({start_time.strftime('%Y-%m-%d')})")
    plt.legend()
    plt.grid(True)
    plt.ylim(min(alts)-5, 90)

    output_path = os.path.join(os.path.dirname(__file__), '../public/assets/figure3.png')
    plt.savefig(output_path)
    print(f"Artifact generated: {output_path}")

if __name__ == "__main__":
    main()
