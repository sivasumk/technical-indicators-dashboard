"""MACD (Moving Average Convergence Divergence)."""

import pandas as pd
from config import MACD_FAST, MACD_SLOW, MACD_SIGNAL


def calculate(df, fast=MACD_FAST, slow=MACD_SLOW, signal=MACD_SIGNAL):
    """Calculate MACD line, signal line, and histogram."""
    result = df.copy()
    close = df["Close"]

    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()

    result["MACD"] = ema_fast - ema_slow
    result.loc[:, "MACD_Signal"] = result["MACD"].ewm(span=signal, adjust=False).mean()
    result.loc[:, "MACD_Hist"] = result["MACD"] - result["MACD_Signal"]

    return result
