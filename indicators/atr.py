"""Average True Range (ATR) with RMA smoothing."""

import numpy as np
import pandas as pd
from config import ATR_PERIOD, ATR_RMA_PERIOD


def calculate(df, period=ATR_PERIOD, rma_period=ATR_RMA_PERIOD):
    """Calculate ATR and its RMA."""
    result = df.copy()

    high = df["High"]
    low = df["Low"]
    close = df["Close"]

    # True Range
    tr1 = high - low
    tr2 = (high - close.shift(1)).abs()
    tr3 = (low - close.shift(1)).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    # ATR using RMA (Wilder's smoothing)
    result["ATR"] = tr.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()

    # RMA of ATR for longer-term volatility reference
    result.loc[:, "ATR_RMA"] = result["ATR"].ewm(
        alpha=1 / rma_period, min_periods=rma_period, adjust=False
    ).mean()

    return result
