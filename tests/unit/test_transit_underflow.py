import pytest
from api.index import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_transit_underflow(client):
    response = client.get('/api/transit?period=1e-300')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
