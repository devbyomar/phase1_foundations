# src/main.py

"""
CLI Entrypoint for YouTube Trending Videos ETL.
Usage: python3 src/main.py --region US --limit 5
"""

import typer
from utils import load_api_key
from fetch import fetch_trending_videos
from utils import save_to_json, save_to_csv

app = typer.Typer()

@app.command(help="Fetch and save trending YouTube videos")
def fetch(
    region: str = typer.Option("US", help="Region code, e.g., US, CA"),
    limit: int = typer.Option(5, help="Number of trending videos to fetch"),
    to_json: bool = typer.Option(False, "--json", help="Save output to JSON"),
    to_csv: bool = typer.Option(False, "--csv", help="Save output to CSV")
):
    api_key = load_api_key()
    data = fetch_trending_videos(api_key, region=region, max_results=limit)
    if data:
        typer.echo(f"\nFetched top {limit} trending videos in {region}\n")
        if to_json:
            save_to_json(data, filepath=f"trending_{region}.json")
        if to_csv:
            save_to_csv(data, filepath=f"trending_{region}.csv")

if __name__ == "__main__":
    app()