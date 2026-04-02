import pytest
from api.index import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_security_headers_root(client):
    """Test that security headers are applied to the root route."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.headers.get('X-Frame-Options') == 'DENY'
    assert response.headers.get('X-Content-Type-Options') == 'nosniff'
    assert response.headers.get('Strict-Transport-Security') == 'max-age=31536000; includeSubDomains'
    assert response.headers.get('Content-Security-Policy') == "default-src 'none'; frame-ancestors 'none'"

def test_security_headers_api_endpoint(client):
    """Test that security headers are applied to an API route."""
    response = client.get('/api/snr?mag=12&exposure=60')
    assert response.status_code == 200
    assert response.headers.get('X-Frame-Options') == 'DENY'
    assert response.headers.get('X-Content-Type-Options') == 'nosniff'
    assert response.headers.get('Strict-Transport-Security') == 'max-age=31536000; includeSubDomains'
    assert response.headers.get('Content-Security-Policy') == "default-src 'none'; frame-ancestors 'none'"

def test_security_headers_error_response(client):
    """Test that security headers are applied even on error responses."""
    response = client.get('/api/snr?mag=invalid')
    assert response.status_code == 400
    assert response.headers.get('X-Frame-Options') == 'DENY'
    assert response.headers.get('X-Content-Type-Options') == 'nosniff'
    assert response.headers.get('Strict-Transport-Security') == 'max-age=31536000; includeSubDomains'
    assert response.headers.get('Content-Security-Policy') == "default-src 'none'; frame-ancestors 'none'"

def test_security_headers_additional_headers(client):
    """Test that additional security headers are applied to the root route."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.headers.get('Referrer-Policy') == 'strict-origin-when-cross-origin'
    assert response.headers.get('Permissions-Policy') == 'geolocation=(), microphone=(), camera=()'

def test_root_endpoint_json_response(client):
    """Test that the root endpoint returns a valid JSON response."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.headers.get('Content-Type') == 'application/json'
    data = response.get_json()
    assert "message" in data
    assert "endpoints" in data

def test_request_payload_too_large(client):
    """Test that requests with a payload larger than MAX_CONTENT_LENGTH return 413."""
    from flask import Flask, request, jsonify
    from werkzeug.exceptions import HTTPException

    # Create a new standalone test app to avoid modifying the main app after its first request
    test_app = Flask(__name__)
    test_app.config['MAX_CONTENT_LENGTH'] = app.config['MAX_CONTENT_LENGTH']
    test_app.config['TESTING'] = True

    # Register the same error handler as the main app
    @test_app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return jsonify({"error": e.name, "description": e.description}), e.code
        return jsonify({"error": "An internal error occurred"}), 500

    @test_app.route('/_test_post', methods=['POST'])
    def test_post():
        _ = request.get_data()
        return {"status": "ok"}

    large_payload = "A" * (11 * 1024) # 11 KB payload

    with test_app.test_client() as test_client:
        response = test_client.post('/_test_post', data=large_payload)
        assert response.status_code == 413
        assert response.headers.get('Content-Type') == 'application/json'
        data = response.get_json()
        assert "error" in data
