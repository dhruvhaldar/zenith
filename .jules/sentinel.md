## 2026-03-23 - [Flask Debug Mode and Missing Input Validation]
**Vulnerability:** The Flask application in `api/index.py` runs with a hardcoded `debug=True`. At the same time, the API endpoints lack input validation (e.g. `float(request.args.get('mag', 12.0))` fails with `ValueError` for strings like "invalid"). This combination allows an attacker to intentionally trigger unhandled exceptions, exposing the interactive Werkzeug Debugger which can lead to Remote Code Execution (RCE) and sensitive data exposure (environment variables, source code).
**Learning:** Hardcoding `debug=True` in a deployable codebase (e.g., Vercel or any production-like environment) is extremely dangerous, particularly when user inputs aren't sanitized or safely handled.
**Prevention:** Never commit `debug=True`. Use environment variables to toggle debug modes locally. Always implement input validation and global exception handlers to fail securely.

## 2026-03-24 - [Missing Input Length Limits (DoS Risk)]
**Vulnerability:** The API endpoints (`/api/snr`, `/api/transit`, `/api/hubble`) lacked maximum bounds checks on incoming float parameters (like `exposure`, `period`, `d`). While it prevented negative values, it allowed extremely large numbers (e.g., `1e300`). Passing exceptionally large variables into complex astronomy calculations caused intensive processing operations, memory inflation, or mathematical overflows (resulting in 500 server errors).
**Learning:** Accepting unbounded numeric data in computationally heavy API endpoints can easily lead to Application-level Denial of Service (DoS) attacks, especially in python environments processing math.
**Prevention:** Always implement both lower and upper boundary checks on numeric API parameters. Make sure bounds match practical use case limits.

## 2026-03-28 - Enforce JSON Responses for All API Errors
**Vulnerability:** Passing through Werkzeug's HTTPExceptions in Flask returns default HTML error pages (e.g., for 404 or 405), which can lead to MIME-sniffing and potential reflected XSS if the CSP fails or is overly permissive in the future.
**Learning:** Default error handlers in web frameworks often leak HTML templates even when the rest of the application is designed to be a JSON API.
**Prevention:** Always explicitly capture HTTP errors in the global error handler and explicitly format them as JSON, rather than relying on the framework's default behavior.
