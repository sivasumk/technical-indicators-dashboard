"""Fetch and cache stock data from yfinance."""

import os
import pickle
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import pytz
import yfinance as yf

from config import (
    CACHE_DIR, DATA_INTERVAL, DATA_PERIOD,
    MARKET_CLOSE_HOUR, MARKET_CLOSE_MINUTE, TIMEZONE,
)


def _cache_path(symbol):
    Path(CACHE_DIR).mkdir(exist_ok=True)
    safe = symbol.replace(".", "_")
    return os.path.join(CACHE_DIR, f"{safe}.pkl")


def _is_cache_fresh(path):
    """Check if cache file has today's data (post market close)."""
    if not os.path.exists(path):
        return False
    try:
        with open(path, "rb") as f:
            df = pickle.load(f)
        if df.empty:
            return False
        ist = pytz.timezone(TIMEZONE)
        now = datetime.now(ist)
        last_date = pd.Timestamp(df.index[-1]).date()
        today = now.date()
        # If today is weekend, check if we have Friday's data
        if today.weekday() >= 5:
            days_since_friday = today.weekday() - 4
            expected_date = today - timedelta(days=days_since_friday)
            return last_date >= expected_date
        # On weekdays after market close, we should have today's data
        market_closed = now.hour > MARKET_CLOSE_HOUR or (
            now.hour == MARKET_CLOSE_HOUR and now.minute >= MARKET_CLOSE_MINUTE
        )
        if market_closed:
            return last_date >= today
        # Before market close, yesterday's data is fine
        return last_date >= today - timedelta(days=1)
    except Exception:
        return False


def fetch_stock(symbol, period=DATA_PERIOD, interval=DATA_INTERVAL, use_cache=True):
    """Fetch OHLCV data for a single stock."""
    cache = _cache_path(symbol)
    if use_cache and _is_cache_fresh(cache):
        with open(cache, "rb") as f:
            return pickle.load(f)

    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        if not df.empty:
            with open(cache, "wb") as f:
                pickle.dump(df, f)
        return df
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        # Try returning cached data even if stale
        if os.path.exists(cache):
            with open(cache, "rb") as f:
                return pickle.load(f)
        return pd.DataFrame()


def fetch_all(symbols, use_cache=True):
    """Fetch data for all symbols. Returns dict of {symbol: DataFrame}."""
    data = {}
    failed = []
    for i, symbol in enumerate(symbols):
        print(f"  [{i+1}/{len(symbols)}] Fetching {symbol}...", end="\r")
        df = fetch_stock(symbol, use_cache=use_cache)
        if not df.empty:
            data[symbol] = df
        else:
            failed.append(symbol)
    print(f"\nFetched {len(data)} stocks, {len(failed)} failed.")
    if failed:
        print(f"Failed: {', '.join(failed)}")
    return data


def get_last_update_time():
    """Get the most recent cache file modification time."""
    cache_dir = Path(CACHE_DIR)
    if not cache_dir.exists():
        return None
    files = list(cache_dir.glob("*.pkl"))
    if not files:
        return None
    latest = max(files, key=lambda f: f.stat().st_mtime)
    ist = pytz.timezone(TIMEZONE)
    return datetime.fromtimestamp(latest.stat().st_mtime, tz=ist)
