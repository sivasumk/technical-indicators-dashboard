"""Directional Movement Index (DMI) and Average Directional Index (ADX)."""

import numpy as np
import pandas as pd
from config import DMI_PERIOD, ADX_SMOOTHING


def calculate(df, period=DMI_PERIOD, adx_smooth=ADX_SMOOTHING):
    """Calculate +DI, -DI, and ADX."""
    result = df.copy()

    high = df["High"]
    low = df["Low"]
    close = df["Close"]

    # True Range
    tr1 = high - low
    tr2 = (high - close.shift(1)).abs()
    tr3 = (low - close.shift(1)).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    # Directional Movement
    up_move = high - high.shift(1)
    down_move = low.shift(1) - low

    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)

    plus_dm = pd.Series(plus_dm, index=df.index)
    minus_dm = pd.Series(minus_dm, index=df.index)

    # Wilder's smoothing (RMA)
    atr = tr.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    plus_dm_smooth = plus_dm.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    minus_dm_smooth = minus_dm.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()

    # +DI and -DI
    result["Plus_DI"] = 100 * (plus_dm_smooth / atr.replace(0, np.nan))
    result["Minus_DI"] = 100 * (minus_dm_smooth / atr.replace(0, np.nan))

    # DX and ADX
    di_sum = result["Plus_DI"] + result["Minus_DI"]
    di_diff = (result["Plus_DI"] - result["Minus_DI"]).abs()
    dx = 100 * (di_diff / di_sum.replace(0, np.nan))
    result.loc[:, "ADX"] = dx.ewm(alpha=1 / adx_smooth, min_periods=adx_smooth, adjust=False).mean()

    return result
