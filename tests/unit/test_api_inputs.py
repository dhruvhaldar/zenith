import pytest
from api.index import app, safe_get_float

def test_safe_get_float_valid():
    """Test that valid floats are accepted."""
    assert safe_get_float({'val': '12.5'}, 'val', 0.0) == 12.5
    assert safe_get_float({'val': '-12.5'}, 'val', 0.0) == -12.5
    assert safe_get_float({'val': '0'}, 'val', 0.0) == 0.0

def test_safe_get_float_nan():
    """Test that NaN is rejected."""
    with pytest.raises(ValueError, match="must be a finite number"):
        safe_get_float({'val': 'nan'}, 'val', 0.0)
    with pytest.raises(ValueError, match="must be a finite number"):
        safe_get_float({'val': 'NaN'}, 'val', 0.0)

def test_safe_get_float_inf():
    """Test that Infinity is rejected."""
    with pytest.raises(ValueError, match="must be a finite number"):
        safe_get_float({'val': 'inf'}, 'val', 0.0)
    with pytest.raises(ValueError, match="must be a finite number"):
        safe_get_float({'val': 'infinity'}, 'val', 0.0)
    with pytest.raises(ValueError, match="must be a finite number"):
        safe_get_float({'val': '-inf'}, 'val', 0.0)
    with pytest.raises(ValueError, match="must be a finite number"):
        safe_get_float({'val': '-Infinity'}, 'val', 0.0)

def test_safe_get_float_too_long():
    """Test that overly long strings are rejected."""
    with pytest.raises(ValueError, match="exceeds maximum length"):
        safe_get_float({'val': '1' * 51}, 'val', 0.0)

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
