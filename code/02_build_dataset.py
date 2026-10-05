"""Step 2: merge your ESPN rankings with draft picks and extra features.
Needs data/espn_rankings.csv (all years stacked) with columns:
  year (or draft_year), team, qb, rb, wr, te, ol, dt, de, lb, cb, s
Writes data/model_data.csv
"""
import pandas as pd
from config import *

# ---- Rankings (your data) ----
rk = pd.read_csv(DATA / "espn_rankings.csv")
rk = rk.loc[:, ~rk.columns.str.startswith("Unnamed")]
rk.columns = rk.columns.str.strip().str.lower()
rk = rk.drop(columns=["avg"], errors="ignore")
if "draft_year" not in rk.columns:
    assert "year" in rk.columns, "Rankings file needs a 'year' (or 'draft_year') column"
    rk["draft_year"] = rk["year"] + RANK_YEAR_OFFSET
    rk = rk.drop(columns=["year"])
rk["team"] = rk["team"].str.strip().str.upper().replace(TEAM_MAP)
missing = {"draft_year", "team", *RANK_COLS} - set(rk.columns)
assert not missing, f"espn_rankings.csv is missing columns: {missing}"
assert not rk.duplicated(["draft_year", "team"]).any(), "Duplicate team/year rows in rankings"

# Rank sanity check: each position should be a clean 1-32 ranking within each year
for y, g in rk.groupby("draft_year"):
    for c in RANK_COLS:
        if sorted(g[c]) != list(range(1, 33)):
            print(f"WARNING: draft_year {y}, column '{c}' is not a clean 1-32 ranking - check for a typo.")

# Keep only draft years that have happened / are in range
out_of_range = sorted(set(rk["draft_year"]) - set(range(START_YEAR, END_YEAR + 1)))
if out_of_range:
    print(f"Dropping ranking rows for draft years {out_of_range} (outside {START_YEAR}-{END_YEAR}; "
          "no draft results to learn from).")
rk = rk[rk["draft_year"].between(START_YEAR, END_YEAR)]

# ---- Draft picks + team draft history (uses only EARLIER drafts) ----
picks = pd.read_csv(DATA / "first_round_picks.csv")
classes = sorted(picks["target"].unique())
hist_rows = []
for _, r in picks.iterrows():
    prior = picks[(picks["team"] == r["team"]) &
                  (picks["draft_year"] < r["draft_year"]) &
                  (picks["draft_year"] >= r["draft_year"] - LOOKBACK)]
    hist_rows.append({f"hist_{c}": int((prior["target"] == c).sum()) for c in classes})
picks = pd.concat([picks.reset_index(drop=True), pd.DataFrame(hist_rows)], axis=1)

# ---- Win % ----
wp = pd.read_csv(DATA / "win_pct.csv")

df = picks.merge(rk, on=["draft_year", "team"], how="inner")
df = df.merge(wp, on=["draft_year", "team"], how="left")

# ---- Validation: make sure the merge didn't silently drop rows ----
exp = picks[picks["draft_year"].isin(rk["draft_year"].unique())]
print(f"First-round picks in ranking years: {len(exp)}  | after merge: {len(df)}")
lost = exp.merge(rk[["draft_year", "team"]], on=["draft_year", "team"], how="left", indicator=True)
lost = lost[lost["_merge"] == "left_only"]
if len(lost):
    print("\nPicks with NO matching ranking row (check team abbreviations / years):")
    print(lost[["draft_year", "team", "pick"]].to_string(index=False))
print("Missing win_pct:", int(df["win_pct"].isna().sum()))
print("\nRows per class:\n", df["target"].value_counts().to_string())
df.to_csv(DATA / "model_data.csv", index=False)
print("\nSaved data/model_data.csv", df.shape)
