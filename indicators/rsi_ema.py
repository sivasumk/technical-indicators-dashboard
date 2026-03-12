"""RSI with EMA crossover system.

RSI calculated for periods 5 and 14.
Two EMAs of RSI: fast (5) and slow (55).
Bullish when EMA_5 of RSI > EMA_55 of RSI, bearish otherwise.
"""

import numpy as np
import pandas as pd
from config import RSI_PERIOD_SHORT, RSI_PERIOD_LONG, RSI_EMA_FAST, RSI_EMA_SLOW


def _rsi(series, period):
    """Calculate RSI using RMA (Wilder's smoothing)."""
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta).where(delta < 0, 0.0)

    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)


def calculate(df, rsi_short=RSI_PERIOD_SHORT, rsi_long=RSI_PERIOD_LONG,
              ema_fast=RSI_EMA_FAST, ema_slow=RSI_EMA_SLOW):
    """Calculate RSI values and EMA crossover signals."""
    result = df.copy()

    # RSI for both periods
    result[f"RSI_{rsi_short}"] = _rsi(df["Close"], rsi_short)
    result[f"RSI_{rsi_long}"] = _rsi(df["Close"], rsi_long)

    # Use RSI_14 as the base for EMA crossover
    rsi_base = result[f"RSI_{rsi_long}"]

    # EMA of RSI
    ema_fast_col = rsi_base.ewm(span=ema_fast, adjust=False).mean()
    ema_slow_col = rsi_base.ewm(span=ema_slow, adjust=False).mean()
    result.loc[:, f"RSI_EMA_{ema_fast}"] = ema_fast_col
    result.loc[:, f"RSI_EMA_{ema_slow}"] = ema_slow_col

    # Signal: 1 = bullish (fast > slow), -1 = bearish
    result.loc[:, "RSI_Signal"] = np.where(ema_fast_col > ema_slow_col, 1, -1)

    return result
