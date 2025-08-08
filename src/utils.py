# src/utils.py
"""
Utilities used across the project: loading secrets and saving data.

Design goals:
- Keep "environment concerns" (like reading .env) isolated from business logic.
- Provide small, single-purpose functions that are easy to test.
- Avoid side effects (e.g., no printing inside helpers unless necessary).
"""

import os
from typing import Optional
from dotenv import load_dotenv
import json
import pandas as pd

def load_api_key(env_path: Optional[str] = None) -> str:
    """
    Load the YouTube API key securely from a .env file (or the current env).

    Why a parameter?
    - `env_path` lets tests pass a temporary .env path so tests don't depend on your real machine.
      In production code, "injecting" dependencies like file paths makes functions testable and reliable.

    What this does:
    1) Calls load_dotenv() so environment variables from `.env` are available via os.getenv().
       If `env_path` is None, it looks for `.env` in the working directory by default.
    2) Reads the 'YOUTUBE_API_KEY' environment variable.
    3) Fails fast with a clear error if the key is missing (so you don't get deep mysterious failures later).

    Returns:
        str: The API key string.

    Raises:
        ValueError: If the key is missing. Fail-fast is a standard engineering practice.
    """
    load_dotenv(dotenv_path=env_path)
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        # Fail-fast: better to stop here with a clear message than to make a broken API call later.
        raise ValueError("❌ API key not found. Add YOUTUBE_API_KEY to your .env file.")
    return api_key


def save_to_json(data: dict, filepath: str) -> None:
    """
    Persist the raw API response to a JSON file.

    Why JSON?
    - JSON is a faithful representation of the API response and good for auditing/debugging.
    - It's human-readable (with indent) and easy to diff in PRs.

    Args:
        data: The parsed API response (a Python dict).
        filepath: Where to write the file, e.g., 'trending_US.json'.
    """
    # 'with' ensures the file is properly closed even if an exception occurs.
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_to_csv(data: dict, filepath: str) -> None:
    """
    Convert a subset of the API response into a flat table and write CSV.

    Why CSV?
    - CSV is a common interchange format for analytics tools and spreadsheets.
    - A flat table is easy to inspect and test.

    What we extract:
    - title (from snippet)
    - views (from statistics.viewCount)

    Note:
    - We guard with .get() to avoid KeyErrors if the API shape changes or fields are missing.
    """
    items = data.get("items", [])  # Gracefully handle missing/empty lists.
    records = []
    for item in items:
        snippet = item.get("snippet", {})         # Safe access to nested dict
        stats = item.get("statistics", {})
        title = snippet.get("title", None)        # If missing, leave as None
        views = stats.get("viewCount", None)      # YouTube returns strings; we keep them as-is here
        records.append({"title": title, "views": views})

    df = pd.DataFrame(records)        # Create a simple tabular view
    df.to_csv(filepath, index=False)  # No index column in CSV


