"""Run scans across the stock universe."""

import pandas as pd

from data.symbols import symbol_display_name
from indicators.engine import compute_all, get_latest_values
from scanner.signals import compute_signals
from scanner.conditions import PRESETS


def scan_all(stock_data):
    """Compute indicators and signals for all stocks.

    Args:
        stock_data: dict of {symbol: DataFrame} from fetcher.

    Returns:
        DataFrame with one row per stock, all indicator values + signals.
    """
    rows = []
    for symbol, df in stock_data.items():
        try:
            enriched = compute_all(df)
            values = get_latest_values(enriched)
            sigs = compute_signals(values)

            row = {
                "Symbol": symbol_display_name(symbol),
                "yf_symbol": symbol,
                **values,
                "Score": sigs["composite_score"],
                "Verdict": sigs["verdict"],
            }
            # Add individual signal labels
            for sig_name, sig_data in sigs["signals"].items():
                row[f"{sig_name}_Label"] = sig_data["label"]

            rows.append(row)
        except Exception as e:
            print(f"Error processing {symbol}: {e}")

    result = pd.DataFrame(rows)
    if not result.empty:
        result = result.sort_values("Score", ascending=False).reset_index(drop=True)
    return result


def apply_preset(scan_df, stock_data, preset_name):
    """Filter scan results using a preset condition."""
    if preset_name not in PRESETS:
        return scan_df

    preset = PRESETS[preset_name]
    matching = []

    for _, row in scan_df.iterrows():
        symbol = row["yf_symbol"]
        if symbol not in stock_data:
            continue
        df = stock_data[symbol]
        enriched = compute_all(df)
        values = get_latest_values(enriched)
        sigs = compute_signals(values)

        if preset["filter"](sigs):
            matching.append(row["Symbol"])

    return scan_df[scan_df["Symbol"].isin(matching)].reset_index(drop=True)
