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

## 2026-03-29 - [DoS via Unbounded Input Length in Python Type Casting]
**Vulnerability:** API query parameters were extracted and directly cast using `float(request.args.get('param'))` without checking the length of the incoming string. An attacker supplying extremely long strings (e.g. 50+ million characters) could cause the server to spend excessive CPU time and memory attempting to allocate, parse, and evaluate the type cast.
**Learning:** Even built-in type casting functions like `float()` or `int()` in Python can become Denial of Service (DoS) vectors if the input string is arbitrarily long, due to the $O(n)$ or worse complexity of string parsing and internal memory allocations.
**Prevention:** Always enforce a strict maximum length limit (e.g., `len(val) <= 50`) on string inputs before attempting to cast them to numeric types, ensuring the length matches practical application bounds.

## 2026-03-30 - Implicit text/html in JSON APIs
**Vulnerability:** The root endpoint (`/`) of the Flask application was returning a simple Python string, which Flask implicitly renders with a `text/html` Content-Type by default. In an API meant strictly for JSON responses, returning generic HTML endpoints can introduce cross-site scripting (XSS) or MIME-sniffing risks if an attacker can manipulate that path or bypass content-security-policies (CSP). Additionally, `Referrer-Policy` and `Permissions-Policy` headers were missing, weakening the application's defense in depth.
**Learning:** Returning strings instead of explicit JSON (e.g., using `jsonify()`) in a framework like Flask causes it to default to `text/html`. This is a common oversight when building simple "healthcheck" or "info" root endpoints for an API.
**Prevention:** Always enforce a strict `application/json` Content-Type for all endpoints in a JSON API, including the root route. Utilize comprehensive security headers, including `Referrer-Policy` and `Permissions-Policy`, to proactively mitigate cross-origin and browser-feature risks.

## 2026-03-31 - Missing Global Security Headers for Static Frontend
**Vulnerability:** Security headers (like CSP, X-Frame-Options, X-Content-Type-Options) were only applied within the Flask application using `@app.after_request`. However, Vercel routes standard HTTP traffic directly to static files (e.g., `public/index.html`), entirely bypassing Flask. This architectural gap meant the static frontend was completely exposed to clickjacking, MIME-sniffing, and lacked a Content Security Policy.
**Learning:** In serverless deployments using tools like Vercel, web framework security middlewares only protect API routes. They do not protect statically hosted frontend files.
**Prevention:** Always define global security headers at the hosting configuration level (e.g., in `vercel.json`), ensuring defense-in-depth for the entire application, including both dynamic APIs and static assets.
