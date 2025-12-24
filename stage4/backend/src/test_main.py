"""Unit tests to test the API
"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_always_pass():
    """Make sure the testing suite work
    """
    assert True
