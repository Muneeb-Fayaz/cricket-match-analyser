"""Small API client for Cricket Database."""
import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


BASE_URL = "https://api.cricketdatabase.com/v1"


def read_api_key():
    """Read CDB_API_KEY from environment or a local .env file."""
    key = os.getenv("CDB_API_KEY", "").strip()
    if key:
        return key

    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as env_file:
            for line in env_file:
                line = line.strip()
                if line.startswith("CDB_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def fetch_matches(year=None, match_format=None, limit=100):
    """Fetch one page of match summaries. One request uses one API hit."""
    api_key = read_api_key()
    if not api_key:
        raise ValueError("API key not found. Add CDB_API_KEY to your .env file.")

    params = {"limit": min(max(int(limit), 1), 100), "page": 1}
    if year:
        params["year"] = int(year)
    if match_format and match_format.lower() != "all":
        params["format"] = match_format.lower()

    url = f"{BASE_URL}/matches?{urlencode(params)}"
    request = Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "User-Agent": "CricketInsightsStudentProject/1.0",
        },
    )

    try:
        with urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"API returned HTTP {error.code}: {details[:300]}") from error
    except URLError as error:
        raise RuntimeError(f"Could not connect to the API: {error.reason}") from error
    except TimeoutError as error:
        raise RuntimeError("API request timed out. Please try again.") from error

    rows = payload.get("data", [])
    if isinstance(rows, dict):
        rows = rows.get("results", [])
    if not isinstance(rows, list):
        raise RuntimeError("Unexpected API response: match list was not found.")

    return rows, payload.get("meta", {})
