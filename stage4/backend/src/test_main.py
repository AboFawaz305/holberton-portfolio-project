"""Unit tests for the FastAPI application."""
from fastapi.testclient import TestClient

from core import search_groups
from main import app

client = TestClient(app)


def test_search_groups_returns_match_from_keywords():
    """Test search groups returns match from keywords
    """
    results = search_groups("fastapi")
    assert any("FastAPI" in group["name"] for group in results)


def test_search_route_returns_results():
    """Test search route returns results
    """
    response = client.get("/groups/search", params={"keyword": "python"})
    assert response.status_code == 200
    payload = response.json()
    assert "results" in payload
    assert any("python" in group["keywords"] for group in payload["results"])


def test_search_route_handles_no_matches():
    """Test search route handles no matches
    """
    response = client.get(
        "/groups/search", params={"keyword": "zzzz-not-found"})
    assert response.status_code == 200
    assert response.json()["results"] == []
