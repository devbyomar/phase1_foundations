# tests/test_fetch.py

import pytest
from src.fetch import fetch_trending_videos

class DummyResponse:
    status_code = 200
    def __init__(self, data): self._data = data
    def json(self): return self._data

def dummy_request(*args, **kwargs):
    return DummyResponse({
        "items": [
            {"snippet": {"title": "Test Vid"}, "statistics": {"viewCount": "123"}}
        ]
    })

def test_fetch_trending(monkeypatch):
    monkeypatch.setattr("src.fetch.requests.get", dummy_request)
    data = fetch_trending_videos("dummy_key", region="US", max_results=1)
    assert "items" in data
    assert data["items"][0]["snippet"]["title"] == "Test Vid"