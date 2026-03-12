"""On Balance Volume (OBV)."""

import numpy as np
import pandas as pd


def calculate(df):
    """Calculate OBV and its EMA for trend detection."""
    result = df.copy()

    direction = np.sign(df["Close"].diff())
    result["OBV"] = (direction * df["Volume"]).fillna(0).cumsum()

    # 20-period EMA of OBV for trend
    result.loc[:, "OBV_EMA"] = result["OBV"].ewm(span=20, adjust=False).mean()

    return result
