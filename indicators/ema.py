"""Exponential Moving Average."""

import pandas as pd
from config import EMA_PERIOD


def calculate(df, period=EMA_PERIOD):
    """Add EMA column to dataframe."""
    result = df.copy()
    result[f"EMA_{period}"] = df["Close"].ewm(span=period, adjust=False).mean()
    return result
