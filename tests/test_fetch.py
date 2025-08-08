# tests/test_fetch.py

"""
Unit tests for src.fetch.fetch_trending_videos.

Core testing strategy:
----------------------
- We want this test to validate our fetch_trending_videos logic **without**
  making actual HTTP requests to the YouTube Data API (which would be:
  - slow
  - flaky due to network or quota limits
  - potentially expensive if billed).
- Instead, we use pytest's `monkeypatch` fixture to replace `requests.get`
  with a deterministic in-memory dummy function.

Why monkeypatch here?
---------------------
- Monkeypatch lets us *temporarily* override functions or attributes at runtime
  **only for the duration of the test**.
- This avoids adding test-only code to production logic.
- By patching at the module path where it's used (`src.fetch.requests.get`),
  we ensure the function under test sees *our* replacement, not the real network.

Expected behavior under test:
-----------------------------
- Given: A fake HTTP 200 OK response with a known JSON structure.
- When: `fetch_trending_videos` is called with any API key & parameters.
- Then: It should return the parsed JSON, preserving the `items` structure.

This style of test is called a **unit test with a stubbed dependency**.
"""

import pytest
from src.fetch import fetch_trending_videos

class DummyResponse:
    """
    A minimal stand-in for `requests.Response`.

    Why this exists:
    - `fetch_trending_videos` calls `.status_code` and `.json()` on the response.
    - Instead of importing the actual `Response` object, we fake just enough
      behavior to satisfy our test.
    - This keeps the test lightweight and decoupled from the actual `requests` internals.
    """
    status_code = 200

    def __init__(self, data):
        # Store the data we want `.json()` to return
        self._data = data

    def json(self):
        # Simulate `requests.Response.json()` by returning preloaded data
        return self._data


def dummy_request(*args, **kwargs):
    """
    Replacement for `requests.get` during the test.

    Why `*args, **kwargs`?
    - The real `requests.get` is called with positional and keyword args
      (URL, params, timeout, etc.).
    - By accepting arbitrary args, our dummy won't break if the call signature
      changes in production code.

    Returns:
        DummyResponse: containing a controlled, predictable YouTube-like payload.
    """
    return DummyResponse({
        "items": [
            {
                "snippet": {"title": "Test Vid"},
                "statistics": {"viewCount": "123"}
            }
        ]
    })


def test_fetch_trending(monkeypatch):
    """
    GIVEN:
        - `fetch_trending_videos` depends on `requests.get` to call the YouTube API.
        - We don't want real HTTP calls in unit tests.
    WHEN:
        - We monkeypatch `src.fetch.requests.get` to our `dummy_request`.
        - We call `fetch_trending_videos` with a dummy API key and parameters.
    THEN:
        - The returned dict contains the `items` key.
        - The first item's title matches our dummy payload ("Test Vid").

    Why this matters:
    - Verifies correct integration between our code and the `requests` API contract.
    - Ensures our JSON parsing logic works with the expected YouTube API schema.
    - Prevents false positives/negatives caused by network flakiness or live API changes.
    """
    # Replace `requests.get` in the *module under test* with our dummy
    monkeypatch.setattr("src.fetch.requests.get", dummy_request)

    # Call the function with dummy values; they don't matter since dummy_request ignores them
    data = fetch_trending_videos("dummy_key", region="US", max_results=1)

    # Assertions check *structure* and *specific known value*
    assert "items" in data
    assert data["items"][0]["snippet"]["title"] == "Test Vid"
