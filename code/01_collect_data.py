"""Step 1: pull first-round picks and prior-season win % from nflreadpy (nflverse data).
Run once (needs internet):  python 01_collect_data.py
Writes data/first_round_picks.csv and data/win_pct.csv
"""
import pandas as pd
import nflreadpy as nfl
from config import *

years = list(range(START_YEAR - LOOKBACK, END_YEAR + 1))

# ---- Draft picks (target variable) ----
picks = nfl.load_draft_picks(years).to_pandas()
picks = picks.rename(columns={"season": "draft_year"})
picks = picks[picks["round"] == 1].copy()
picks["team"] = picks["team"].replace(TEAM_MAP)
picks["target"] = picks["position"].map(POSITION_MAP).fillna("OTHER")
picks = picks[["draft_year", "pick", "team", "pfr_player_name", "position", "target"]]
picks.to_csv(DATA / "first_round_picks.csv", index=False)

got = sorted(picks["draft_year"].unique())
print("Draft years pulled:", got)
absent = [y for y in range(START_YEAR, END_YEAR + 1) if y not in got]
if absent:
    print(f"\nWARNING: no first-round picks found for {absent}. nflverse may not have these yet.")
    print("Tell Claude and we'll add them manually to data/first_round_picks.csv.")

print("First-round picks pulled:", len(picks))
print("\nRaw positions found (check they are all mapped how you want):")
print(picks["position"].value_counts().to_string())
print("\nTarget class counts:")
print(picks["target"].value_counts().to_string())

# ---- Prior-season regular-season win % ----
sched = nfl.load_schedules(list(range(START_YEAR - 1, END_YEAR))).to_pandas()
sched = sched[sched["game_type"] == "REG"].dropna(subset=["home_score", "away_score"])
rows = []
for _, g in sched.iterrows():
    h, a = g["home_team"], g["away_team"]
    hs, as_ = g["home_score"], g["away_score"]
    hw = 1.0 if hs > as_ else 0.5 if hs == as_ else 0.0
    rows.append((g["season"], h, hw))
    rows.append((g["season"], a, 1.0 - hw))
wp = pd.DataFrame(rows, columns=["season", "team", "w"])
wp["team"] = wp["team"].replace(TEAM_MAP)
wp = wp.groupby(["season", "team"], as_index=False)["w"].mean()
wp = wp.rename(columns={"w": "win_pct"})
wp["draft_year"] = wp["season"] + 1       # season before the draft
wp[["draft_year", "team", "win_pct"]].to_csv(DATA / "win_pct.csv", index=False)
print("\nWin % rows:", len(wp))
