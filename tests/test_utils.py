# tests/test_utils.py
"""
Tests for utils.py.

Testing principles on display:
- Use tmp_path (a pytest fixture) to create temporary files/folders that auto-clean.
- Make functions deterministic by passing explicit paths (env_path).
- Assert both happy paths and failure paths (positive/negative testing).
"""

import json
from pathlib import Path
import pandas as pd
import pytest

from src.utils import load_api_key, save_to_json, save_to_csv


def test_load_api_key_from_custom_env(tmp_path):
    """
    GIVEN a temporary .env file that contains a key
    WHEN we call load_api_key with that env path
    THEN we get the correct key string.

    Why this matters:
    - The function's behavior is decoupled from your real machine's state (.env in project root).
    - Deterministic tests are reliable and fast in CI.
    """
    env_file: Path = tmp_path / ".env"
    env_file.write_text("YOUTUBE_API_KEY=TEST_KEY_123\n", encoding="utf-8")

    key = load_api_key(env_path=str(env_file))

    assert key == "TEST_KEY_123"


def test_load_api_key_raises_if_missing(tmp_path):
    """
    GIVEN a temporary .env file with no key
    WHEN load_api_key is called
    THEN it should raise ValueError (fail-fast) with a clear message.

    Why this matters:
    - We want explicit, early failures instead of confusing downstream errors.
    """
    def test_load_api_key_raises_if_missing(tmp_path, monkeypatch):
        env_file = tmp_path / ".env"
        env_file.write_text("", encoding="utf-8")
        monkeypatch.delenv("YOUTUBE_API_KEY", raising=False)

        with pytest.raises(ValueError) as excinfo:
            load_api_key(env_file)

        assert "API key not found" in str(excinfo.value)


def test_save_to_json_roundtrip(tmp_path):
    """
    GIVEN a small dict representing an API response subset
    WHEN save_to_json is called
    THEN reading the file back yields identical data (round-trip).
    """
    data = {"items": [{"snippet": {"title": "A"}, "statistics": {"viewCount": "7"}}]}
    out = tmp_path / "out.json"

    save_to_json(data, filepath=str(out))

    loaded = json.loads(out.read_text(encoding="utf-8"))
    assert loaded == data


def test_save_to_csv_structure(tmp_path):
    """
    GIVEN a dict with two items
    WHEN save_to_csv writes a CSV
    THEN the CSV has the expected columns and row count.

    We don't assert exact numeric types here (APIs often return strings); we only assert shape & content.
    """
    data = {
        "items": [
            {"snippet": {"title": "A"}, "statistics": {"viewCount": "7"}},
            {"snippet": {"title": "B"}, "statistics": {"viewCount": "9"}},
        ]
    }
    out = tmp_path / "out.csv"

    save_to_csv(data, filepath=str(out))

    df = pd.read_csv(out)
    assert list(df.columns) == ["title", "views"]
    assert df.shape == (2, 2)
    assert df.iloc[0]["title"] == "A"
    # views may be read as string or number, so we only assert the textual value is present
    assert str(df.iloc[1]["views"]) in {"9", "9.0"}
