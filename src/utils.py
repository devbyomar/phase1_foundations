# src/utils.py

import os
from dotenv import load_dotenv
import json
import pandas as pd

def save_to_json(data: dict, filepath: str):
    """Save JSON data to a file."""
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved JSON to {filepath}")

def save_to_csv(data: dict, filepath: str):
    """Convert YouTube JSON to DataFrame and save as CSV."""
    items = data.get("items", [])
    records = [
        {
            "title": item["snippet"]["title"],
            "views": item["statistics"].get("viewCount", "N/A")
        }
        for item in items
    ]
    df = pd.DataFrame(records)
    df.to_csv(filepath, index=False)
    print(f"Saved CSV to {filepath}")

def load_api_key():
    """Loads API key from .env file securely."""
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("❌ API key not found. Make sure it's in .env")
    return api_key

def save_to_json(data: dict, filepath: str):
    """Save JSON data to a file."""
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved JSON to {filepath}")

def save_to_csv(data: dict, filepath: str):
    """Convert YouTube JSON to DataFrame and save as CSV."""
    items = data.get("items", [])
    records = [
        {
            "title": item["snippet"]["title"],
            "views": item["statistics"].get("viewCount", "N/A")
        }
        for item in items
    ]
    df = pd.DataFrame(records)
    df.to_csv(filepath, index=False)
    print(f"Saved CSV to {filepath}")

