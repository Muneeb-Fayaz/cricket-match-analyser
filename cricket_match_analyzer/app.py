"""Terminal entry point for Cricket Insights."""
from pathlib import Path

import pandas as pd

from cricket_analyzer.api import fetch_matches
from cricket_analyzer.analysis import (
    export_reports, filter_matches, overall_summary, team_summary
)
from cricket_analyzer.data_manager import (
    ROOT, api_rows_to_frame, load_sample, load_saved, save_matches
)


def pause():
    input("\nPress Enter to continue...")


def show_menu():
    print("\n" + "🏏 " + "=" * 48)
    print("             CRICKET INSIGHTS ANALYZER")
    print("=" * 52)
    print("1. Use included sample dataset")
    print("2. Fetch recent matches from free API")
    print("3. Load previously fetched API data")
    print("4. View overall analysis dashboard")
    print("5. Compare a team")
    print("6. Filter and view matches")
    print("7. Export CSV reports")
    print("8. Exit")
    print("=" * 52)


def main():
    frame = pd.DataFrame()

    while True:
        show_menu()
        choice = input("Choose an option (1-8): ").strip()

        if choice == "1":
            frame = load_sample()
            print(f"\nLoaded {len(frame)} sample matches.")
            pause()

        elif choice == "2":
            print("\nAPI filters (press Enter to skip a filter).")
            year_text = input("Year, e.g. 2025: ").strip()
            match_format = input(
                "Format (test / odi / t20i / t20 / all): "
            ).strip().lower() or "all"
            limit_text = input("Number of matches (max 100, default 50): ").strip()
            try:
                year = int(year_text) if year_text else None
                limit = int(limit_text) if limit_text else 50
                rows, meta = fetch_matches(year, match_format, limit)
                frame = api_rows_to_frame(rows)
                if frame.empty:
                    print("The API returned no usable match records.")
                else:
                    save_matches(frame)
                    print(f"\nLoaded and saved {len(frame)} matches.")
                    print(f"API plan: {meta.get('plan', 'not reported')}")
                    print("Saved to data/matches.csv")
            except ValueError as error:
                print(f"\nInput/configuration problem: {error}")
            except (RuntimeError, OSError) as error:
                print(f"\nCould not fetch matches: {error}")
            pause()

        elif choice == "3":
            frame = load_saved()
            print(f"\nLoaded {len(frame)} saved matches.")
            pause()

        elif choice == "4":
            if frame.empty:
                print("\nLoad sample or API data first.")
            else:
                overall_summary(frame)
            pause()

        elif choice == "5":
            if frame.empty:
                print("\nLoad data first.")
            else:
                team = input("Enter team name (e.g. India): ").strip()
                if team:
                    team_summary(frame, team)
            pause()

        elif choice == "6":
            if frame.empty:
                print("\nLoad data first.")
            else:
                team = input("Team filter (or Enter for all): ").strip()
                match_format = input(
                    "Format filter (test/odi/t20i/t20/all): "
                ).strip().lower() or "all"
                result = filter_matches(frame, team, match_format)
                print(f"\nFound {len(result)} matches.")
                if result.empty:
                    print("No matches match those filters.")
                else:
                    print(result[[
                        "date", "format", "team_1", "team_2",
                        "winner", "result"
                    ]].to_string(index=False, max_rows=40))
            pause()

        elif choice == "7":
            if frame.empty:
                print("\nLoad data first.")
            else:
                reports = ROOT / "reports"
                export_reports(frame, reports)
                print(f"\nReports exported to: {reports}")
                print("Created cleaned_matches.csv, matches_by_format.csv,")
                print("matches_by_year.csv and team_win_summary.csv.")
            pause()

        elif choice == "8":
            print("\nThanks for using Cricket Insights. Keep analysing! 🏏")
            break

        else:
            print("\nPlease choose a number from 1 to 8.")
            pause()


if __name__ == "__main__":
    main()
