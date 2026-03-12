"""Stochastic Momentum Index (SMI)."""

import numpy as np
import pandas as pd
from config import SMI_K_PERIOD, SMI_D_PERIOD, SMI_SMOOTH


def calculate(df, k_period=SMI_K_PERIOD, d_period=SMI_D_PERIOD, smooth=SMI_SMOOTH):
    """Calculate SMI and signal line."""
    result = df.copy()

    # Highest high and lowest low over k_period
    highest_high = df["High"].rolling(window=k_period).max()
    lowest_low = df["Low"].rolling(window=k_period).min()

    # Midpoint
    midpoint = (highest_high + lowest_low) / 2

    # Distance from close to midpoint
    distance = df["Close"] - midpoint

    # Half range
    half_range = (highest_high - lowest_low) / 2

    # Double smooth the distance
    smooth_d1 = distance.ewm(span=d_period, adjust=False).mean()
    smooth_d2 = smooth_d1.ewm(span=d_period, adjust=False).mean()

    # Double smooth the half range
    smooth_r1 = half_range.ewm(span=d_period, adjust=False).mean()
    smooth_r2 = smooth_r1.ewm(span=d_period, adjust=False).mean()

    # SMI = 100 * (smoothed distance / smoothed half range)
    smi = np.where(smooth_r2 != 0, 100 * (smooth_d2 / smooth_r2), 0)
    result["SMI"] = smi

    # Signal line
    smi_series = pd.Series(smi, index=df.index)
    signal_line = smi_series.ewm(span=smooth, adjust=False).mean()
    result["SMI_Signal"] = signal_line

    # Crossover detection
    prev_smi = smi_series.shift(1)
    prev_signal = signal_line.shift(1)
    result["SMI_Bull_Cross"] = (prev_smi <= prev_signal) & (smi_series > signal_line)
    result["SMI_Bear_Cross"] = (prev_smi >= prev_signal) & (smi_series < signal_line)

    return result
