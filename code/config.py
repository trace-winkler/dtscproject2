"""Settings shared by all scripts. Edit this file, not the scripts."""
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data"
OUT = ROOT / "outputs"
DATA.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)

# Draft years to model. Rankings for draft year Y must be the PRESEASON rankings
# from the season BEFORE that draft (e.g. 2023 preseason -> 2024 draft).
# Your CSV has a column "year". If it holds the PRESEASON year, keep OFFSET = 1
# (draft_year = year + 1). If it already holds the DRAFT year, set OFFSET = 0.
RANK_YEAR_OFFSET = 1
START_YEAR = 2021     # first DRAFT year (preseason 2020 rankings -> 2021 draft)
END_YEAR = 2026       # last DRAFT year
LOOKBACK = 5          # extra earlier drafts pulled to compute team draft history

# How many of the most recent draft years to hold out as the test set.
N_TEST_YEARS = 2   # (only used if you switch off leave-one-year-out in step 3)

# Draft position (from the data) -> your target classes. CHECK the printed counts
# after running 01 and adjust. Anything not listed becomes "OTHER".
POSITION_MAP = {
    "QB": "QB",
    "WR": "WR",
    "T": "OL", "G": "OL", "C": "OL", "OL": "OL", "OT": "OL", "OG": "OL",
    "DE": "DL", "OLB": "DL", "EDGE": "DL",   # EDGE merged into DL (small sample)
    "DT": "DL", "NT": "DL", "DL": "DL",
    "CB": "DB", "S": "DB", "DB": "DB", "FS": "DB", "SS": "DB", "SAF": "DB",
    # RB, TE, LB, K, P, FB -> OTHER (merge or split these as you see fit)
}

# Different sources abbreviate teams differently. Everything is mapped to ESPN-style.
TEAM_MAP = {
    "WAS": "WSH", "JAC": "JAX", "ARZ": "ARI", "CRD": "ARI", "CLT": "IND",
    "HTX": "HOU", "OTI": "TEN", "RAV": "BAL", "BLT": "BAL", "GNB": "GB",
    "KAN": "KC", "NWE": "NE", "NOR": "NO", "SFO": "SF", "TAM": "TB",
    "SDG": "LAC", "SD": "LAC", "LVR": "LV", "RAI": "LV", "OAK": "LV",
    "STL": "LAR", "LA": "LAR",
}

RANK_COLS = ["qb", "rb", "wr", "te", "ol", "dt", "de", "lb", "cb", "s"]
