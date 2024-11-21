"""Sets up the S&P data for use in the Life-Cycle-Prime-Time estimation."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from estimark.parameters import (
    age_mapping,
    final_age_data,
    initial_age,
    remove_ages_from_snp,
)

file_path = (
    Path(__file__).resolve().parent / ".." / "data" / "S&P Target Date glidepath.xlsx"
)

# Define column mapping and columns to keep
column_mapping = {"Current Age": "age", "S&P Target Date Equity allocation": "share"}

# Load data, rename columns, filter data
snp_data = (
    pd.read_excel(file_path, usecols=column_mapping.keys())
    .rename(columns=column_mapping)
    .query(f"{initial_age} < age <= {final_age_data}")
)

# Assign age groups
bins = [initial_age + 1] + [group[-1] + 1 for group in age_mapping.values()]
labels = list(age_mapping.keys())

snp_data = snp_data.assign(
    age_group=pd.cut(snp_data["age"], bins=bins, labels=labels, right=False),
)

snp_data_full = snp_data.copy()
# Remove ages
snp_data = snp_data.loc[
    ~snp_data.age.isin(remove_ages_from_snp),
    ["age", "share", "age_group"],
]
