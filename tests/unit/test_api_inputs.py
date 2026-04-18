import pytest
from api.index import app, safe_get_float
from werkzeug.datastructures import MultiDict

def test_safe_get_float_valid():
    """Test that valid floats are accepted."""
    assert safe_get_float(MultiDict([('val', '12.5')]), 'val', 0.0) == 12.5
    assert safe_get_float(MultiDict([('val', '-12.5')]), 'val', 0.0) == -12.5
    assert safe_get_float(MultiDict([('val', '0')]), 'val', 0.0) == 0.0

def test_safe_get_float_nan():
    """Test that NaN is rejected."""
    with pytest.raises(ValueError, match="must be a finite number"):
        safe_get_float(MultiDict([('val', 'nan')]), 'val', 0.0)
    with pytest.raises(ValueError, match="must be a finite number"):
        safe_get_float(MultiDict([('val', 'NaN')]), 'val', 0.0)

def test_safe_get_float_inf():
    """Test that Infinity is rejected."""
    with pytest.raises(ValueError, match="must be a finite number"):
        safe_get_float(MultiDict([('val', 'inf')]), 'val', 0.0)
    with pytest.raises(ValueError, match="must be a finite number"):
        safe_get_float(MultiDict([('val', 'infinity')]), 'val', 0.0)
    with pytest.raises(ValueError, match="must be a finite number"):
        safe_get_float(MultiDict([('val', '-inf')]), 'val', 0.0)
    with pytest.raises(ValueError, match="must be a finite number"):
        safe_get_float(MultiDict([('val', '-Infinity')]), 'val', 0.0)

def test_safe_get_float_too_long():
    """Test that overly long strings are rejected."""
    with pytest.raises(ValueError, match="exceeds maximum length"):
        safe_get_float(MultiDict([('val', '1' * 51)]), 'val', 0.0)

def test_safe_get_float_multiple_values():
    """Test that multiple values are rejected."""
    with pytest.raises(ValueError, match="Multiple values provided for val, which is not allowed"):
        safe_get_float(MultiDict([('val', '12.5'), ('val', '15.0')]), 'val', 0.0)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_api_rejects_nan_inf(client):
    """Test that the API endpoints return 400 for NaN and Infinity."""
    response = client.get('/api/snr?mag=nan')
    assert response.status_code == 400
    assert response.get_json()['error'] == "Invalid input parameters"

    response = client.get('/api/transit?period=inf')
    assert response.status_code == 400
    assert response.get_json()['error'] == "Invalid input parameters"

    response = client.get('/api/hubble?d=-infinity')
    assert response.status_code == 400
    assert response.get_json()['error'] == "Invalid input parameters"
