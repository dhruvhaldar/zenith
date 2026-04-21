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

## 2024-05-18 - Missing Global Security Headers in Serverless Deployments
**Vulnerability:** Static frontend assets (HTML, images, JS) served by Vercel lacked basic security headers like `X-Frame-Options`, `Content-Security-Policy`, and `X-Content-Type-Options`. This exposed the frontend to clickjacking, MIME-sniffing, and potential XSS attacks.
**Learning:** In Vercel serverless deployments, backend framework middleware (e.g., Flask's `@app.after_request`) only protects API routes explicitly routed to the serverless function. Static assets are served directly by Vercel's edge network and bypass the backend completely, leaving them unprotected.
**Prevention:** Always configure global security headers in the deployment configuration file (e.g., `vercel.json`'s `headers` block) to ensure all routes, including static files, are properly protected, rather than relying solely on application-level middleware.

## 2026-04-07 - [Log Injection Bypass via exc_info]
**Vulnerability:** The exception message logged by `app.logger.error` could contain user-controlled newlines. Simply sanitizing the message string fails to prevent log injection because `exc_info=True` appends the full, unsanitized traceback containing the original string.
**Learning:** In Python's `logging` module, `exc_info=True` renders the raw traceback independently of the main message string, exposing it to CRLF injection.
**Prevention:** When mitigating Log Injection (CRLF) vulnerabilities, especially when `exc_info=True` is used, you must implement a custom `logging.Formatter` to strip newline characters (
, ) from the entire formatted record.

## 2026-04-08 - [Missing Cache-Control Header in JSON APIs]
**Vulnerability:** The API endpoints returned dynamic JSON responses without a `Cache-Control` header. While not containing explicitly personal data, the absence of this header allows browsers and intermediate proxies to cache the responses indefinitely, which could expose potentially sensitive calculations or error details over time.
**Learning:** Even if an API doesn't seem to return highly sensitive personal data, allowing dynamic JSON responses to be cached by default is a poor defense-in-depth strategy that can lead to unintentional data exposure.
**Prevention:** Always enforce `Cache-Control: no-store, max-age=0` in global security middleware for dynamic API endpoints to proactively prevent unwanted caching across all layers.

## 2026-04-09 - [Math Underflow DoS via Unbounded Inputs]
**Vulnerability:** The `/api/transit` endpoint had a lower bound validation for `period` using `> 0`. However, this naive check allowed exceptionally small numbers (like `1e-300`) to pass validation. In the transit calculations, Kepler's 3rd law involves squaring the period (`period**2`), which underflowed entirely to `0.0` in Python's standard floating-point representation, causing a subsequent `ZeroDivisionError` when attempting to divide by the derived velocity. This exposed the server to DoS (500 errors) for specific mathematical operations.
**Learning:** Floating-point underflow (values close to zero) can be just as dangerous as overflow. Naive `> 0` checks are insufficient for inputs that act as denominators or are subjected to operations that can shrink them to zero.
**Prevention:** Always enforce practical, strictly defined lower bounds (e.g., `0.0001 <= val`) rather than just checking if it is non-zero, especially before routing values into complex mathematical formulas.

## 2026-04-10 - [NaN/Inf Injection in Python APIs]
**Vulnerability:** API query parameters cast via `float()` could accept special floating-point values like `nan` (Not a Number) and `inf` (Infinity). These values propagate silently through simple mathematical bounds checks (like `0 <= val <= 100`, which returns `False` for `nan`), allowing the attacker to bypass validation logic or trigger unexpected mathematical errors, 500 status codes, or uncontrolled resource consumption downstream.
**Learning:** Checking ranges is insufficient when dealing with floats because `nan` fails comparison operators and `inf` might pass if upper bounds are missing.
**Prevention:** Explicitly check for `math.isnan()` and `math.isinf()` immediately after casting user input to a float, explicitly rejecting them before performing any logic or range validation.
## 2026-04-11 - [Missing Cross-Origin Isolation Headers]
**Vulnerability:** The application was missing modern Cross-Origin Isolation security headers (`Cross-Origin-Opener-Policy` and `Cross-Origin-Resource-Policy`). While the CSP was strong, the lack of these headers meant the application was not isolated from other origins, potentially leaving it vulnerable to Spectre-like side-channel attacks and unintended cross-origin resource sharing.
**Learning:** Even with a strong Content-Security-Policy, true cross-origin isolation requires setting COOP and CORP to `same-origin`. These must be set both in the application layer (for dynamic API routes) and the CDN/edge layer (for static assets) to ensure complete coverage.
**Prevention:** Always include `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Resource-Policy: same-origin` alongside standard security headers (like X-Frame-Options and CSP) in both application middleware and deployment configurations.
## 2026-04-13 - [Weak CSP and Missing HSTS Preload]
**Vulnerability:** The Content-Security-Policy (CSP) in `vercel.json` and `api/index.py` allowed default form actions, base-uri modifications, and insecure HTTP downgrades within a secure origin. The `Strict-Transport-Security` header lacked the `preload` directive.
**Learning:** Even a relatively strict CSP like `default-src 'none'` or `default-src 'self'` doesn't fully protect against `<base>` tag injection or unauthorized `<form>` submissions unless `base-uri 'none'` and `form-action 'none'` are explicitly defined. Similarly, without HSTS `preload`, users visiting the site for the very first time via HTTP are vulnerable to man-in-the-middle attacks before the HSTS policy is cached.
**Prevention:** Always strengthen CSPs with explicit constraints like `base-uri 'none'`, `form-action 'none'`, and `upgrade-insecure-requests`, especially in environments hosting API endpoints and strict static assets. Always include `; preload` in HSTS headers for production web applications to qualify for hardcoded HTTPS enforcement in browsers.
## 2026-04-15 - [Server Header Information Leakage]
**Vulnerability:** The API and static assets deployed on Vercel were returning default `Server` HTTP headers (e.g., exposing Werkzeug/Flask versions or Vercel edge infrastructure). This fingerprinting information allows attackers to identify backend technologies and target them with known CVEs specific to those versions.
**Learning:** Relying solely on framework defaults or hosting provider edge networks often leaks underlying stack information via the `Server` header, providing unnecessary intelligence to potential attackers during the reconnaissance phase.
**Prevention:** Always explicitly override the `Server` HTTP header with a generic, unified value (e.g., `Server: Custom API`) in both the backend application middleware and the frontend edge deployment configuration (like `vercel.json`) to minimize the application's attack surface fingerprint.

## 2026-04-16 - [Implicit text/html in Flask OPTIONS Requests]
**Vulnerability:** Implicit HTTP responses generated by Flask, particularly for CORS `OPTIONS` preflight requests, default to a `text/html` Content-Type with an empty body. When deploying a strictly JSON API, this can trigger security scanner alerts and theoretically introduce MIME-sniffing vulnerabilities or edge-case XSS if browsers misinterpret the empty payload.
**Learning:** Even when all custom API routes and explicitly caught error handlers use `jsonify()` or return `application/json`, the underlying web framework (Flask/Werkzeug) will still fall back to `text/html` for requests it automatically intercepts and responds to, like `OPTIONS`.
**Prevention:** Intercept responses globally via `@app.after_request` middleware. Specifically target implicit responses (e.g., `request.method == 'OPTIONS'` and `response.mimetype == 'text/html'`) and safely enforce `response.mimetype = 'application/json'`, ensuring empty bodies are safely formatted as empty JSON objects (`{}`) to maintain uniform Content-Type guarantees across the entire application surface.
## 2025-02-28 - [Prevent HTTP Parameter Pollution in Flask request.args]
**Vulnerability:** HTTP Parameter Pollution (HPP) in `request.args.get(key)`.
**Learning:** `request.args.get(key)` silently discards multiple values for the same key, which can cause bypassing of upstream WAFs or WAFs parsing the query string differently.
**Prevention:** Use `request.args.getlist(key)` and explicitly reject requests with multiple values if they are not expected.
