"""Kaggle Titanic: 891 labelled passengers, turned into 13 numeric inputs.

Source: train.csv from https://www.kaggle.com/c/titanic, downloaded with the Kaggle CLI:
`kaggle competitions download titanic -p data/download` (then unzip). Kaggle's own test.csv has no labels, so both
splits below come from train.csv. The data is not redistributed here; download it to rerun.

Splits, stratified by survival, from a fixed random permutation (seed 1912):
  val:  600 passengers, the feedback the LLM sees (its training set in practice); gradient baselines train on it too
  test: 291 passengers, never shown to the LLM
"""
import csv
import hashlib
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent / "data"
CSV = HERE / "download" / "train.csv"
SHA256 = "7d118fef8b6ccf7f81111877bc388536f7b1e498a655e3d649d19aaa010e9f6f"
N_VAL = 600

FEATURES = [
    ("pclass_1", "1 if first class, else 0"),
    ("pclass_2", "1 if second class, else 0"),
    ("pclass_3", "1 if third class, else 0"),
    ("female", "1 if female, 0 if male"),
    ("age_decades", "age in years divided by 10 (0.42 years -> 0.042, 80 years -> 8.0); 0 when age is unknown"),
    ("age_known", "1 if age is recorded, 0 if it is missing (about 20% of passengers)"),
    ("sibsp", "number of siblings and spouses aboard (0 to 8)"),
    ("parch", "number of parents and children aboard (0 to 6)"),
    ("log_fare", "natural log of (1 + ticket fare in 1912 pounds); fares run from 0 to 512, so 0 to 6.24"),
    ("embarked_c", "1 if boarded at Cherbourg, else 0"),
    ("embarked_q", "1 if boarded at Queenstown, else 0"),
    ("embarked_s", "1 if boarded at Southampton, else 0 (all three are 0 for the 2 passengers with no port)"),
    ("cabin_known", "1 if a cabin number is recorded, else 0"),
]


def encode(row):
    age = row["Age"]
    return [
        float(row["Pclass"] == "1"), float(row["Pclass"] == "2"), float(row["Pclass"] == "3"),
        float(row["Sex"] == "female"),
        float(age) / 10 if age else 0.0, float(bool(age)),
        float(row["SibSp"]), float(row["Parch"]),
        math.log1p(float(row["Fare"])),
        float(row["Embarked"] == "C"), float(row["Embarked"] == "Q"), float(row["Embarked"] == "S"),
        float(bool(row["Cabin"])),
    ]


# Anonymised variant: columns shuffled by this fixed permutation (anonymous column j is named column PERMUTATION[j]),
# then each standardised to mean 0, standard deviation 1 over the 600 validation rows.
PERMUTATION = [int(i) for i in np.random.default_rng(1913).permutation(len(FEATURES))]


def load(anonymous=False):
    """Return {"val": (x, y), "test": (x, y)}, x of shape (N, 13) float32, y 0 = died, 1 = survived.

    anonymous=True shuffles the columns (PERMUTATION) and standardises each one, so the feature order, units and
    ranges no longer identify the dataset."""
    digest = hashlib.sha256(CSV.read_bytes()).hexdigest()
    if digest != SHA256:
        raise RuntimeError(f"{CSV} has SHA-256 {digest}, expected {SHA256}")
    with CSV.open(newline="") as f:
        rows = list(csv.DictReader(f))
    x = np.array([encode(r) for r in rows], dtype=np.float32)
    y = np.array([int(r["Survived"]) for r in rows], dtype=np.int64)
    rng = np.random.default_rng(1912)
    val = []
    for c in (0, 1):
        idx = rng.permutation(np.flatnonzero(y == c))
        val += list(idx[:round(N_VAL * len(idx) / len(y))])
    val = np.array(sorted(val))
    test = np.setdiff1d(np.arange(len(y)), val)
    if anonymous:
        x = x[:, PERMUTATION]
        mean, std = x[val].mean(axis=0), x[val].std(axis=0)
        x = ((x - mean) / std).astype(np.float32)
    return {"val": (x[val], y[val]), "test": (x[test], y[test])}
