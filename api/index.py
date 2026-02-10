from flask import Flask, jsonify, request
import os
import sys

# Add project root to path for Vercel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from zenith.optics import Telescope, CCD
from zenith.exoplanets import TransitSimulator
from zenith.cosmology import recession_velocity

app = Flask(__name__)

@app.route('/')
def home():
    return "Zenith Astronomy Toolkit API. Visit /api/snr or /api/transit for examples."

@app.route('/api/snr')
def get_snr():
    mag = float(request.args.get('mag', 12.0))
    exposure = float(request.args.get('exposure', 60.0))

    scope = Telescope(aperture=0.203, focal_length=2.0)
    camera = CCD()
    snr = scope.calculate_snr(target_mag=mag, exposure=exposure, ccd=camera)

    return jsonify({
        "telescope": "8-inch f/10",
        "magnitude": mag,
        "exposure": exposure,
        "snr": snr
    })

@app.route('/api/transit')
def get_transit():
    period = float(request.args.get('period', 4.0))
    sim = TransitSimulator(period_days=period)

    return jsonify({
        "period_days": period,
        "transit_depth": sim.depth,
        "transit_duration_hours": sim.duration / 3600.0
    })

@app.route('/api/hubble')
def get_hubble():
    d = float(request.args.get('d', 10.0))
    v = recession_velocity(d)
    return jsonify({
        "distance_mpc": d,
        "recession_velocity_km_s": v
    })

if __name__ == '__main__':
    app.run(debug=True)
