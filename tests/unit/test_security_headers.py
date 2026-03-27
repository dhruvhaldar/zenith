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
