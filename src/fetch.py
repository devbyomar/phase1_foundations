# src/fetch.py
"""
This module is responsible ONLY for fetching data from the YouTube API.

Design principles:
- Separation of concerns: fetching is independent of printing or saving.
- No side effects: it only returns data; it does not log, print, or write files.
- Explicit error handling for API calls.

Industry note:
FAANG engineers write fetchers this way so they can be reused in different pipelines
(ETL jobs, dashboards, ML feature generation, etc.) without changing code.
"""

import requests

def fetch_trending_videos(api_key: str, region: str = "US", max_results: int = 5) -> dict:
    """
    Call the YouTube Data API v3 to retrieve trending videos.

    Args:
        api_key (str): YouTube API key (from Google Cloud Console).
        region (str, optional): Region code for trending videos (ISO 3166-1 alpha-2).
                                Example: "US" (United States), "IN" (India).
        max_results (int, optional): Number of videos to return (1-50).

    Returns:
        dict: Parsed JSON response from the API.

    Raises:
        Exception: If the API returns a non-200 status code.
    """

    # Endpoint URL for YouTube API
    url = "https://www.googleapis.com/youtube/v3/videos"

    # Query parameters according to YouTube API documentation:
    # https://developers.google.com/youtube/v3/docs/videos/list
    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",        
        "regionCode": region,          
        "maxResults": max_results,     
        "key": api_key                 
    }

    # Make the GET request to the YouTube API
    response = requests.get(url, params=params)

    # If the response is successful, return parsed JSON data
    if response.status_code == 200:
        return response.json()

    # Otherwise, raise an exception with details — fail fast with context
    raise Exception(f"❌ API Error: {response.status_code} — {response.text}")

