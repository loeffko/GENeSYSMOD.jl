#!/usr/bin/env python3
"""Merge similar output CSVs and tag each row with its scenario.

Reads every *.csv in INPUT_DIR, groups files by "type" (the filename with the
scenario token removed), concatenates files of the same type into one table,
and adds a "scenario" column holding the scenario suffix (e.g. "_122").

This lets you drop several scenario runs into /input and compare them in one
merged file per output type.
"""

import re
import sys
from pathlib import Path

import pandas as pd

# --- config ---------------------------------------------------------------
INPUT_DIR = Path("input")        # folder with the raw CSVs
OUTPUT_DIR = Path("merged")      # folder for the merged CSVs

# Scenario = the run id that changes between versions. By default it is the
# numeric token sitting right before ".csv" or before a trailing "_word".
# Examples matched:
#   ..._globalLimit_122.csv          -> 122
#   ..._globalLimit_122_example.csv  -> 122
SCENARIO_RE = re.compile(r"_(\d+)(?=(?:_[A-Za-z]+)?\.csv$)")

# TYPE = the bit between "output_" and "_north_america".
#   output_annual_production_north_america_..._122.csv -> annual_production
TYPE_RE = re.compile(r"^output_(.+?)_north_america")
# --------------------------------------------------------------------------


def parse_name(path: Path):
    """Return (file_type, scenario) for a filename.

    file_type = the TYPE token (e.g. "emission"), used in the output name
    scenario  = "_<digits>" suffix, or "_unknown" if none found
    """
    t = TYPE_RE.search(path.name)
    file_type = t.group(1) if t else path.stem  # fallback: whole stem

    m = SCENARIO_RE.search(path.name)
    scenario = "_" + m.group(1) if m else "_unknown"
    return file_type, scenario


def main():
    if not INPUT_DIR.is_dir():
        sys.exit(f"Input folder not found: {INPUT_DIR.resolve()}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    groups: dict[str, list[pd.DataFrame]] = {}
    for csv in sorted(INPUT_DIR.glob("*.csv")):
        file_type, scenario = parse_name(csv)
        df = pd.read_csv(csv)
        df.insert(len(df.columns), "scenario", scenario)  # add at end
        groups.setdefault(file_type, []).append(df)
        print(f"read {csv.name}  ->  type='{file_type}'  scenario='{scenario}'  rows={len(df)}")

    if not groups:
        sys.exit("No CSV files found in input folder.")

    print()
    for file_type, frames in groups.items():
        merged = pd.concat(frames, ignore_index=True, sort=False)
        out = OUTPUT_DIR / f"output_{file_type}_combined.csv"
        merged.to_csv(out, index=False)
        print(f"wrote {out.name}  ({len(frames)} file(s), {len(merged)} rows)")


if __name__ == "__main__":
    main()
