from flask import Flask, jsonify, request
import os
import sys

# Add project root to path for Vercel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from zenith.optics import Telescope, CCD
from zenith.exoplanets import TransitSimulator
from zenith.cosmology import recession_velocity

app = Flask(__name__)

from werkzeug.exceptions import HTTPException

# 🛡️ Sentinel: Global error handler to prevent stack trace leakage
@app.errorhandler(Exception)
def handle_exception(e):
    # Pass through HTTP errors
    if isinstance(e, HTTPException):
        return e
    return jsonify({"error": "An internal error occurred"}), 500

@app.route('/')
def home():
    return "Zenith Astronomy Toolkit API. Visit /api/snr or /api/transit for examples."

@app.route('/api/snr')
def get_snr():
    try:
        # 🛡️ Sentinel: Input validation
        mag = float(request.args.get('mag', 12.0))
        exposure = float(request.args.get('exposure', 60.0))
        if exposure < 0:
            return jsonify({"error": "Exposure cannot be negative"}), 400
    except ValueError:
        return jsonify({"error": "Invalid input parameters"}), 400

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
    try:
        # 🛡️ Sentinel: Input validation
        period = float(request.args.get('period', 4.0))
        if period <= 0:
            return jsonify({"error": "Period must be greater than 0"}), 400
    except ValueError:
        return jsonify({"error": "Invalid input parameters"}), 400

    sim = TransitSimulator(period_days=period)

    return jsonify({
        "period_days": period,
        "transit_depth": sim.depth,
        "transit_duration_hours": sim.duration / 3600.0
    })

@app.route('/api/hubble')
def get_hubble():
    try:
        # 🛡️ Sentinel: Input validation
        d = float(request.args.get('d', 10.0))
        if d < 0:
            return jsonify({"error": "Distance cannot be negative"}), 400
    except ValueError:
        return jsonify({"error": "Invalid input parameters"}), 400

    v = recession_velocity(d)
    return jsonify({
        "distance_mpc": d,
        "recession_velocity_km_s": v
    })

if __name__ == '__main__':
    # 🛡️ Sentinel: Do not hardcode debug=True
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app.run(debug=debug_mode)
