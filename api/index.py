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

# 🛡️ Sentinel: Add global security headers for defense in depth
@app.after_request
def add_security_headers(response):
    # Prevent clickjacking attacks
    response.headers['X-Frame-Options'] = 'DENY'
    # Prevent MIME-sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    # Enforce HTTPS connections
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    # Prevent Cross-Site Scripting (XSS) and data injection
    response.headers['Content-Security-Policy'] = "default-src 'none'"
    return response

@app.route('/')
def home():
    return "Zenith Astronomy Toolkit API. Visit /api/snr or /api/transit for examples."

@app.route('/api/snr')
def get_snr():
    try:
        # 🛡️ Sentinel: Input validation with reasonable boundaries to prevent DoS via huge values
        mag = float(request.args.get('mag', 12.0))
        exposure = float(request.args.get('exposure', 60.0))

        if not (-30 <= mag <= 50):
            return jsonify({"error": "Magnitude out of reasonable bounds (-30 to 50)"}), 400
        if not (0 <= exposure <= 100000):
            return jsonify({"error": "Exposure out of reasonable bounds (0 to 100000 seconds)"}), 400
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
        # 🛡️ Sentinel: Input validation with limits
        period = float(request.args.get('period', 4.0))
        if not (0 < period <= 100000):
            return jsonify({"error": "Period must be between 0 and 100000 days"}), 400
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
        # 🛡️ Sentinel: Input validation with limits
        d = float(request.args.get('d', 10.0))
        if not (0 <= d <= 15000):
            return jsonify({"error": "Distance out of reasonable bounds (0 to 15000 Mpc)"}), 400
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
