"""Convert API and CSV data into one consistent table."""
import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
SAMPLE_FILE = DATA_DIR / "sample_matches.csv"
MATCH_FILE = DATA_DIR / "matches.csv"


def first_number(score):
    """Extract the first innings' runs from text such as '245/8 & 120'."""
    if score is None or pd.isna(score):
        return None
    match = re.search(r"\d+", str(score))
    return int(match.group()) if match else None


def api_rows_to_frame(rows):
    """Flatten the API's match objects into one row per match."""
    cleaned = []
    for item in rows:
        teams = item.get("teams") or []
        team_a = teams[0] if len(teams) > 0 else {}
        team_b = teams[1] if len(teams) > 1 else {}

        cleaned.append({
            "match_id": item.get("match", ""),
            "date": item.get("date", ""),
            "format": item.get("format", "Unknown"),
            "competition": item.get("competition", "Unknown"),
            "team_1": team_a.get("name", "Unknown"),
            "team_2": team_b.get("name", "Unknown"),
            "team_1_score": team_a.get("score", ""),
            "team_2_score": team_b.get("score", ""),
            "team_1_runs": first_number(team_a.get("score")),
            "team_2_runs": first_number(team_b.get("score")),
            "winner": (
                team_a.get("name") if team_a.get("won") is True
                else team_b.get("name") if team_b.get("won") is True
                else "No result"
            ),
            "result": item.get("result", ""),
            "venue": item.get("ground", ""),
            "coverage": item.get("coverage", ""),
        })

    return clean_frame(pd.DataFrame(cleaned))


def clean_frame(frame):
    """Standardize columns and remove unusable duplicate records."""
    if frame.empty:
        return frame

    expected = [
        "match_id", "date", "format", "competition", "team_1", "team_2",
        "team_1_score", "team_2_score", "team_1_runs", "team_2_runs",
        "winner", "result", "venue", "coverage"
    ]
    for column in expected:
        if column not in frame.columns:
            frame[column] = None

    frame = frame[expected].copy()
    text_columns = [
        "match_id", "format", "competition", "team_1", "team_2",
        "winner", "result", "venue", "coverage"
    ]
    for column in text_columns:
        frame[column] = frame[column].fillna("Unknown").astype(str).str.strip()
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    for column in ["team_1_runs", "team_2_runs"]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")

    frame = frame.drop_duplicates(subset=["match_id"], keep="last")
    frame = frame.dropna(subset=["date"])
    frame["year"] = frame["date"].dt.year
    return frame.reset_index(drop=True)


def load_sample():
    return clean_frame(pd.read_csv(SAMPLE_FILE))


def save_matches(frame, path=MATCH_FILE):
    DATA_DIR.mkdir(exist_ok=True)
    frame.to_csv(path, index=False)


def load_saved():
    if not MATCH_FILE.exists():
        return pd.DataFrame()
    return clean_frame(pd.read_csv(MATCH_FILE))
