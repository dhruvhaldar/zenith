import pytest
from api.index import rate_cache

@pytest.fixture(autouse=True)
def clear_rate_limit_state():
    rate_cache.clear()
