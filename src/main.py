# src/main.py
"""
CLI entrypoint for the YouTube Trending Videos pipeline.

Why this exists:
- Allows running the fetch/save pipeline from the terminal.
- Typer provides easy-to-use CLI parsing and automatic help generation.

Usage example:
    python3 src/main.py fetch --region US --limit 5 --json --csv

Industry note:
At FAANG scale, CLI tools like this are used to kick off ETL jobs, test data sources,
and debug production pipelines.
"""

import typer
from src.utils import load_api_key, save_to_json, save_to_csv
from src.fetch import fetch_trending_videos

# Create a Typer application object — handles CLI command parsing
app = typer.Typer()

@app.command(help="Fetch and optionally save trending YouTube videos")
def fetch(
    region: str = typer.Option(
        "US", help="Region code (ISO 3166-1 alpha-2), e.g., US, IN, CA"
    ),
    limit: int = typer.Option(
        5, help="Number of trending videos to fetch (1-50)"
    ),
    to_json: bool = typer.Option(
        False, "--json", help="Save output to a JSON file"
    ),
    to_csv: bool = typer.Option(
        False, "--csv", help="Save output to a CSV file"
    )
):
    """
    CLI command to:
    1) Load API key from .env
    2) Fetch trending videos
    3) Print confirmation
    4) Save to file formats if requested
    """

    # Step 1: Load API key (securely, from environment)
    api_key = load_api_key()

    # Step 2: Fetch data from YouTube API
    data = fetch_trending_videos(api_key, region=region, max_results=limit)

    # Step 3: Feedback to user
    typer.echo(f"\n✅ Fetched top {limit} trending videos in {region}\n")

    # Step 4: Save to JSON if requested
    if to_json:
        filename = f"trending_{region}.json"
        save_to_json(data, filepath=filename)
        typer.echo(f"💾 Saved JSON to {filename}")

    # Step 5: Save to CSV if requested
    if to_csv:
        filename = f"trending_{region}.csv"
        save_to_csv(data, filepath=filename)
        typer.echo(f"💾 Saved CSV to {filename}")

# The app() call here turns the Typer object into a runnable CLI tool.
if __name__ == "__main__":
    app()