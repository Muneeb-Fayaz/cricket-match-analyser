"""Pandas and NumPy analysis functions."""
import numpy as np
import pandas as pd


def score_values(frame):
    values = pd.concat(
        [frame["team_1_runs"], frame["team_2_runs"]],
        ignore_index=True
    ).dropna()
    return values.to_numpy(dtype=float)


def overall_summary(frame):
    scores = score_values(frame)
    print("\n" + "=" * 54)
    print("                 CRICKET INSIGHTS")
    print("=" * 54)
    print(f"Matches analysed       : {len(frame)}")
    print(f"Formats found          : {frame['format'].nunique()}")
    print(f"Competitions found     : {frame['competition'].nunique()}")
    if len(scores):
        print(f"Average team score     : {np.mean(scores):.2f}")
        print(f"Median team score      : {np.median(scores):.2f}")
        print(f"Highest recorded score : {np.max(scores):.0f}")
        print(f"Score standard dev.    : {np.std(scores):.2f}")
    else:
        print("Score statistics      : Not available in loaded records")

    print("\nMATCHES BY FORMAT")
    print(frame["format"].value_counts().to_string())
    print("\nTOP COMPETITIONS")
    print(frame["competition"].value_counts().head(5).to_string())

    print("\nMATCHES BY YEAR")
    print(frame.groupby("year").size().to_string())


def team_summary(frame, team_name):
    team_mask = (
        frame["team_1"].str.contains(team_name, case=False, na=False)
        | frame["team_2"].str.contains(team_name, case=False, na=False)
    )
    matches = frame[team_mask].copy()
    if matches.empty:
        print(f"No matches found for '{team_name}'.")
        return

    wins = int((matches["winner"].str.casefold() == team_name.casefold()).sum())
    # Resolve the displayed team name from the records for case-insensitive input.
    names = pd.concat([matches["team_1"], matches["team_2"]])
    exact_names = names[names.str.casefold() == team_name.casefold()]
    if len(exact_names):
        wins = int((matches["winner"] == exact_names.iloc[0]).sum())

    win_rate = (wins / len(matches)) * 100
    print(f"\nTEAM REPORT: {team_name}")
    print("-" * 40)
    print(f"Matches in loaded data : {len(matches)}")
    print(f"Wins in loaded data    : {wins}")
    print(f"Win percentage         : {win_rate:.1f}%")
    print("\nRecent matches:")
    print(matches[["date", "format", "team_1", "team_2", "winner", "result"]]
          .sort_values("date", ascending=False).head(10).to_string(index=False))


def filter_matches(frame, team="", match_format="all"):
    result = frame.copy()
    if team.strip():
        mask = (
            result["team_1"].str.contains(team, case=False, na=False)
            | result["team_2"].str.contains(team, case=False, na=False)
        )
        result = result[mask]
    if match_format.lower() != "all":
        result = result[result["format"].str.lower() == match_format.lower()]
    return result


def export_reports(frame, reports_dir):
    reports_dir.mkdir(exist_ok=True)
    frame.to_csv(reports_dir / "cleaned_matches.csv", index=False)

    frame["format"].value_counts().rename_axis("format").reset_index(
        name="matches"
    ).to_csv(reports_dir / "matches_by_format.csv", index=False)

    frame.groupby("year").size().reset_index(
        name="matches"
    ).to_csv(reports_dir / "matches_by_year.csv", index=False)

    team_rows = []
    all_teams = pd.concat([frame["team_1"], frame["team_2"]]).dropna().unique()
    for team in all_teams:
        played = frame[
            (frame["team_1"] == team) | (frame["team_2"] == team)
        ]
        wins = int((played["winner"] == team).sum())
        team_rows.append({
            "team": team,
            "matches": len(played),
            "wins": wins,
            "win_percentage": round(wins / len(played) * 100, 2) if len(played) else 0,
        })
    pd.DataFrame(team_rows).sort_values(
        ["wins", "matches"], ascending=False
    ).to_csv(reports_dir / "team_win_summary.csv", index=False)
