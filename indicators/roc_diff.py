"""Rate of Change Difference oscillator.

ROC Diff = ROC(5) - ROC(16), smoothed with EMA(3).
Buy: roc_diff crosses above smooth. Sell: roc_diff crosses below smooth.
"""

import numpy as np
import pandas as pd
from config import ROC_SHORT, ROC_LONG, ROC_SMOOTH


def calculate(df, short=ROC_SHORT, long=ROC_LONG, smooth=ROC_SMOOTH):
    """Calculate ROC Diff and smoothed signal."""
    result = df.copy()
    close = df["Close"]

    # ROC = ((close - close[n]) / close[n]) * 100
    result[f"ROC_{short}"] = close.pct_change(periods=short) * 100
    result[f"ROC_{long}"] = close.pct_change(periods=long) * 100

    # Difference oscillator
    roc_diff_vals = result[f"ROC_{short}"] - result[f"ROC_{long}"]
    result.loc[:, "ROC_Diff"] = roc_diff_vals

    # Smoothed signal
    roc_smooth_vals = roc_diff_vals.ewm(span=smooth, adjust=False).mean()
    result.loc[:, "ROC_Diff_Smooth"] = roc_smooth_vals

    # Crossover signals
    prev_diff = roc_diff_vals.shift(1)
    prev_smooth = roc_smooth_vals.shift(1)
    result.loc[:, "ROC_Cross_Up"] = (prev_diff <= prev_smooth) & (roc_diff_vals > roc_smooth_vals)
    result.loc[:, "ROC_Cross_Down"] = (prev_diff >= prev_smooth) & (roc_diff_vals < roc_smooth_vals)

    return result
