"""Shared constants, data loading and the IQR clipping transformer used by both notebooks."""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

COLUMNS = ["ID", "AGE", "GENDER", "HEIGHT", "WEIGHT", "AP_HI", "AP_LO",
           "CHOLESTEROL", "GLUC", "SMOKE", "ALCO", "ACTIVE", "CARDIO"]
NUMERIC = ["AGE", "HEIGHT", "WEIGHT", "AP_HI", "AP_LO"]
CATEGORICAL = ["GENDER", "CHOLESTEROL", "GLUC", "SMOKE", "ALCO", "ACTIVE"]
FEATURES = NUMERIC + CATEGORICAL
TARGET = "CARDIO"
BLOOD_PRESSURE = ["AP_HI", "AP_LO"]
EXPECTED_ROWS = 70000


def load_raw(path):
    """Read the semicolon-separated source file and validate its shape. AGE stays in days."""
    frame = pd.read_csv(Path(path), sep=";")
    frame.columns = frame.columns.str.upper()
    if list(frame.columns) != COLUMNS:
        raise ValueError(f"Unexpected columns: {list(frame.columns)}")
    if len(frame) != EXPECTED_ROWS or frame.ID.nunique() != EXPECTED_ROWS:
        raise ValueError("Expected 70,000 records with unique IDs.")
    return frame.sort_values("ID").reset_index(drop=True)


def age_in_years(frame):
    """Return a copy with AGE converted from days to whole years (integer division)."""
    out = frame.copy()
    out["AGE"] = out["AGE"] // 365
    return out


def iqr_limits(series, factor=1.5):
    q1, q3 = series.quantile([0.25, 0.75])
    iqr = q3 - q1
    return q1 - factor * iqr, q3 + factor * iqr


class IQRClipper(BaseEstimator, TransformerMixin):
    """Learn IQR limits on the data passed to fit() and cap the chosen columns to them."""

    def __init__(self, columns=tuple(BLOOD_PRESSURE), factor=1.5):
        self.columns = columns
        self.factor = factor

    def fit(self, X, y=None):
        X = pd.DataFrame(X)
        self.limits_ = {c: iqr_limits(X[c], self.factor) for c in self.columns}
        self.feature_names_in_ = np.asarray(X.columns, dtype=object)
        return self

    def transform(self, X):
        X = pd.DataFrame(X).copy()
        for c, (low, high) in self.limits_.items():
            X[c] = X[c].clip(low, high)
        return X

    def get_feature_names_out(self, input_features=None):
        return self.feature_names_in_
