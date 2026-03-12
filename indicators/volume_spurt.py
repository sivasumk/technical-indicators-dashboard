"""Volume Spurt detection.

Volume Spurt = current volume >= 2x the 5-day average volume.
"""

import numpy as np
import pandas as pd

from config import VOLUME_MA_PERIOD

SPURT_MULTIPLIER = 2.0
VOL_AVG_PERIOD = 5


def calculate(df, period=VOL_AVG_PERIOD, multiplier=SPURT_MULTIPLIER):
    """Detect volume spurts.

    Adds columns:
    - Vol_Avg_5: 5-day average volume
    - Vol_Ratio: current volume / 5-day average
    - Vol_Spurt: True if volume >= 2x average
    """
    result = df.copy()

    vol_avg = df["Volume"].rolling(window=period).mean()
    result["Vol_Avg_5"] = vol_avg

    ratio = np.where(vol_avg > 0, df["Volume"] / vol_avg, 0.0)
    result["Vol_Ratio"] = ratio

    result["Vol_Spurt"] = ratio >= multiplier

    return result
