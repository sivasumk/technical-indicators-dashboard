"""Impulse Candle detection.

An impulse candle has a large body relative to its total range (High - Low),
indicating strong conviction. Body >= 70% of total range qualifies.
"""

import numpy as np
import pandas as pd


BODY_RATIO_THRESHOLD = 0.70


def calculate(df, threshold=BODY_RATIO_THRESHOLD):
    """Detect impulse candles.

    Adds columns:
    - Impulse: True if body >= threshold * range
    - Impulse_Dir: 1 = bullish impulse, -1 = bearish impulse, 0 = no impulse
    - Body_Ratio: body size as fraction of total range
    """
    result = df.copy()

    body = (df["Close"] - df["Open"]).abs()
    total_range = df["High"] - df["Low"]

    # Avoid division by zero (doji candles)
    ratio = np.where(total_range > 0, body / total_range, 0.0)
    result["Body_Ratio"] = ratio

    is_impulse = ratio >= threshold
    result["Impulse"] = is_impulse

    # Direction: bullish if close > open, bearish if close < open
    direction = np.where(df["Close"] > df["Open"], 1, np.where(df["Close"] < df["Open"], -1, 0))
    result["Impulse_Dir"] = np.where(is_impulse, direction, 0)

    return result
