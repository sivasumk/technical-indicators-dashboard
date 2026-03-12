"""Styled dataframe displays for Streamlit."""

import pandas as pd


def style_verdict(val):
    """Color code the verdict column."""
    colors = {
        "STRONG BUY": "background-color: #1B5E20; color: white",
        "BUY": "background-color: #2E7D32; color: white",
        "NEUTRAL": "background-color: #424242; color: white",
        "SELL": "background-color: #C62828; color: white",
        "STRONG SELL": "background-color: #B71C1C; color: white",
    }
    return colors.get(val, "")


def style_score(val):
    """Color code score values."""
    try:
        v = float(val)
        if v >= 3:
            return "background-color: #1B5E20; color: white"
        elif v >= 1:
            return "background-color: #2E7D32; color: white"
        elif v <= -3:
            return "background-color: #B71C1C; color: white"
        elif v <= -1:
            return "background-color: #C62828; color: white"
    except (ValueError, TypeError):
        pass
    return "background-color: #424242; color: white"


def style_change(val):
    """Color code change percentage."""
    try:
        v = float(val)
        if v > 0:
            return "color: #4CAF50"
        elif v < 0:
            return "color: #F44336"
    except (ValueError, TypeError):
        pass
    return ""


def style_signal_label(val):
    """Color code signal labels."""
    val_str = str(val)
    bullish = ["Bullish", "Bullish Trend", "Accumulation", "Oversold", "Bull Impulse", "Bull Cross"]
    bearish = ["Bearish", "Bearish Trend", "Distribution", "Overbought", "Bear Impulse", "Bear Cross"]
    if val_str in bullish:
        return "color: #4CAF50"
    elif val_str in bearish:
        return "color: #F44336"
    elif "Spurt" in val_str:
        return "color: #FF9800; font-weight: bold"
    return "color: #9E9E9E"


def style_impulse(val):
    """Color code impulse candle column."""
    val_str = str(val)
    if val_str == "Bull Impulse":
        return "background-color: #1B5E20; color: white; font-weight: bold"
    elif val_str == "Bear Impulse":
        return "background-color: #B71C1C; color: white; font-weight: bold"
    return ""


def style_smi_cross(val):
    """Color code SMI crossover column — highlighted with background."""
    val_str = str(val)
    if val_str == "Bull Cross":
        return "background-color: #00C853; color: black; font-weight: bold"
    elif val_str == "Bear Cross":
        return "background-color: #FF1744; color: white; font-weight: bold"
    elif val_str == "Oversold":
        return "color: #4CAF50"
    elif val_str == "Overbought":
        return "color: #F44336"
    return "color: #9E9E9E"


def style_vol_spurt(val):
    """Color code volume spurt column."""
    val_str = str(val)
    if "Spurt" in val_str:
        return "background-color: #E65100; color: white; font-weight: bold"
    return ""


OVERVIEW_COLUMNS = [
    "Symbol", "Close", "Change%", "RSI_14", "SMI",
    "ADX", "MACD_Hist", "Score", "Verdict",
]

DETAIL_COLUMNS = [
    "Symbol", "Close", "Change%",
    "RSI_14", "RSI_EMA_5", "RSI_EMA_55", "RSI_EMA_Label",
    "SMI", "SMI_Signal",
    "Plus_DI", "Minus_DI", "ADX", "DMI_Label",
    "MACD", "MACD_Signal", "MACD_Hist", "MACD_Label",
    "OBV_Label", "ROC_Diff_Label",
    "Score", "Verdict",
]


def format_overview_df(scan_df):
    """Prepare overview DataFrame for display."""
    if scan_df.empty:
        return scan_df

    display = scan_df.copy()

    # Rename signal labels for display
    label_cols = [c for c in display.columns if c.endswith("_Label")]
    for col in label_cols:
        short = col.replace("_Label", "")
        display.rename(columns={col: f"{short} Sig"}, inplace=True)

    # Round and format numeric columns to 2 decimal places
    numeric_cols = display.select_dtypes(include="number").columns
    for col in numeric_cols:
        display[col] = display[col].apply(
            lambda x: f"{x:.2f}" if pd.notna(x) else x
        )

    return display
