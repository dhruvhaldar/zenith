from flask import Flask, jsonify, request
import os
import sys

# Add project root to path for Vercel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from zenith.optics import Telescope, CCD
from zenith.exoplanets import TransitSimulator
from zenith.cosmology import recession_velocity
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
# 🛡️ Sentinel: Properly parse reverse proxy headers (Vercel) to log accurate remote client IPs
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# 🛡️ Sentinel: Enforce a strict maximum request size (10 KB) to prevent DoS via massive payloads
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024

import logging

class SanitizedFormatter(logging.Formatter):
    """🛡️ Sentinel: Prevent Log Injection by stripping newlines from the entire log record, including traceback."""
    def format(self, record):
        formatted_message = super().format(record)
        return formatted_message.replace('\n', '  |  ').replace('\r', '')

if app.logger.handlers:
    for handler in app.logger.handlers:
        handler.setFormatter(SanitizedFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
else:
    handler = logging.StreamHandler()
    handler.setFormatter(SanitizedFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

from werkzeug.exceptions import HTTPException

# 🛡️ Sentinel: Global error handler to prevent stack trace leakage and HTML injection
@app.errorhandler(Exception)
def handle_exception(e):
    # Pass through HTTP errors as JSON
    if isinstance(e, HTTPException):
        # 🛡️ Sentinel: Log HTTP exceptions (e.g., 404, 405, 413) to maintain an audit trail of potential fuzzing or scanning attempts.
        client_ip = request.remote_addr or "Unknown IP"
        app.logger.warning(f"HTTP Exception {e.code} on {request.method} {request.path} from {client_ip}: {e.name}")
        return jsonify({
            "error": e.name,
            "description": e.description
        }), e.code

    # 🛡️ Sentinel: Securely log unhandled exceptions internally to avoid silent failures
    # while preventing stack trace exposure to the client. Include request context for security auditing.
    client_ip = request.remote_addr or "Unknown IP"
    app.logger.error(f"Unhandled Exception on {request.method} {request.path} from {client_ip}: {e}", exc_info=True)
    return jsonify({"error": "An internal error occurred"}), 500

# 🛡️ Sentinel: Add global security headers for defense in depth
@app.after_request
def add_security_headers(response):
    # 🛡️ Sentinel: Enforce application/json to prevent implicit text/html MIME-sniffing/XSS on implicit OPTIONS
    if request.method == 'OPTIONS' and response.mimetype == 'text/html':
        response.mimetype = 'application/json'
        if response.data == b'':
            response.set_data(b'{}')

    # Prevent clickjacking attacks
    response.headers['X-Frame-Options'] = 'DENY'
    # Prevent MIME-sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    # Enforce HTTPS connections
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
    # Prevent XSS and data injection attacks
    response.headers['Content-Security-Policy'] = "default-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'; upgrade-insecure-requests"
    # Prevent leaking information in the referer header
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    # Restrict access to browser features
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    # Prevent caching of dynamic API responses
    response.headers['Cache-Control'] = 'no-store, max-age=0'
    # Prevent cross-origin information leaks
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    response.headers['Cross-Origin-Resource-Policy'] = 'same-origin'
    # 🛡️ Sentinel: Obfuscate Server header to prevent information leakage
    response.headers['Server'] = 'Zenith API'
    return response

import math

# 🛡️ Sentinel: Helper to prevent DoS via very long strings in float() casting
# Also prevents NaN/Inf injection which can bypass logic or cause mathematical errors downstream
def safe_get_float(args, key, default):
    vals = args.getlist(key)
    if len(vals) == 0:
        return default
    if len(vals) > 1:
        raise ValueError(f"Multiple values provided for {key}, potential HPP attack")
    val = vals[0]
    if len(val) > 50:
        raise ValueError(f"Input for {key} exceeds maximum length")
    parsed_val = float(val)
    if math.isnan(parsed_val) or math.isinf(parsed_val):
        raise ValueError(f"Input for {key} must be a finite number")
    return parsed_val


@app.route('/')
def home():
    # 🛡️ Sentinel: Enforce JSON response to prevent MIME sniffing and implicit text/html
    return jsonify({
        "message": "Zenith Astronomy Toolkit API",
        "endpoints": ["/api/snr", "/api/transit", "/api/hubble"]
    })

@app.route('/api/snr')
def get_snr():
    try:
        # 🛡️ Sentinel: Input validation with reasonable boundaries to prevent DoS via huge values
        mag = safe_get_float(request.args, 'mag', 12.0)
        exposure = safe_get_float(request.args, 'exposure', 60.0)

        if not (-30 <= mag <= 50):
            client_ip = request.remote_addr or "Unknown IP"
            app.logger.warning(f"Boundary validation failed on {request.method} {request.path} from {client_ip}: Magnitude {mag} out of reasonable bounds")
            return jsonify({"error": "Magnitude out of reasonable bounds (-30 to 50)"}), 400
        if not (0 <= exposure <= 100000):
            client_ip = request.remote_addr or "Unknown IP"
            app.logger.warning(f"Boundary validation failed on {request.method} {request.path} from {client_ip}: Exposure {exposure} out of reasonable bounds")
            return jsonify({"error": "Exposure out of reasonable bounds (0 to 100000 seconds)"}), 400
    except ValueError as e:
        client_ip = request.remote_addr or "Unknown IP"
        app.logger.warning(f"Input validation failed on {request.method} {request.path} from {client_ip}: {e}")
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
        period = safe_get_float(request.args, 'period', 4.0)
        # 🛡️ Sentinel: Enforce a practical lower bound to prevent float underflow
        # which can bypass > 0 checks and cause ZeroDivisionErrors in transit calculations
        if not (0.0001 <= period <= 100000):
            client_ip = request.remote_addr or "Unknown IP"
            app.logger.warning(f"Boundary validation failed on {request.method} {request.path} from {client_ip}: Period {period} out of reasonable bounds")
            return jsonify({"error": "Period must be between 0.0001 and 100000 days"}), 400
    except ValueError as e:
        client_ip = request.remote_addr or "Unknown IP"
        app.logger.warning(f"Input validation failed on {request.method} {request.path} from {client_ip}: {e}")
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
        d = safe_get_float(request.args, 'd', 10.0)
        if not (0 <= d <= 15000):
            client_ip = request.remote_addr or "Unknown IP"
            app.logger.warning(f"Boundary validation failed on {request.method} {request.path} from {client_ip}: Distance {d} out of reasonable bounds")
            return jsonify({"error": "Distance out of reasonable bounds (0 to 15000 Mpc)"}), 400
    except ValueError as e:
        client_ip = request.remote_addr or "Unknown IP"
        app.logger.warning(f"Input validation failed on {request.method} {request.path} from {client_ip}: {e}")
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
