# src/fetch.py

import requests

def fetch_trending_videos(api_key, region="US", max_results=5):
    """Fetches trending videos from YouTube API."""
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",
        "regionCode": region,
        "maxResults": max_results,
        "key": api_key
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"❌ API Error: {response.status_code} — {response.text}")
