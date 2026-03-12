"""Compute all indicators for a stock."""

from indicators import (
    ema, smi, rsi_ema, dmi_adx, obv, roc_diff, atr, macd,
    impulse_candle, volume_spurt,
)


def compute_all(df):
    """Run all 10 indicators on a DataFrame. Returns enriched DataFrame."""
    if df.empty:
        return df

    result = df.copy()
    result = ema.calculate(result)
    result = smi.calculate(result)
    result = rsi_ema.calculate(result)
    result = dmi_adx.calculate(result)
    result = obv.calculate(result)
    result = roc_diff.calculate(result)
    result = atr.calculate(result)
    result = macd.calculate(result)
    result = impulse_candle.calculate(result)
    result = volume_spurt.calculate(result)
    return result


def get_latest_values(df):
    """Extract the most recent indicator values as a dict."""
    if df.empty:
        return {}

    last = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else last

    return {
        "Close": last.get("Close", 0),
        "Volume": last.get("Volume", 0),
        "Change%": ((last["Close"] - prev["Close"]) / prev["Close"] * 100)
        if prev["Close"] != 0 else 0,
        "EMA_5": last.get("EMA_5", 0),
        "SMI": last.get("SMI", 0),
        "SMI_Signal": last.get("SMI_Signal", 0),
        "SMI_Bull_Cross": bool(last.get("SMI_Bull_Cross", False)),
        "SMI_Bear_Cross": bool(last.get("SMI_Bear_Cross", False)),
        "RSI_5": last.get("RSI_5", 0),
        "RSI_14": last.get("RSI_14", 0),
        "RSI_EMA_5": last.get("RSI_EMA_5", 0),
        "RSI_EMA_55": last.get("RSI_EMA_55", 0),
        "RSI_Signal": last.get("RSI_Signal", 0),
        "Plus_DI": last.get("Plus_DI", 0),
        "Minus_DI": last.get("Minus_DI", 0),
        "ADX": last.get("ADX", 0),
        "OBV": last.get("OBV", 0),
        "OBV_EMA": last.get("OBV_EMA", 0),
        "ROC_Diff": last.get("ROC_Diff", 0),
        "ROC_Diff_Smooth": last.get("ROC_Diff_Smooth", 0),
        "ATR": last.get("ATR", 0),
        "ATR_RMA": last.get("ATR_RMA", 0),
        "MACD": last.get("MACD", 0),
        "MACD_Signal": last.get("MACD_Signal", 0),
        "MACD_Hist": last.get("MACD_Hist", 0),
        # Impulse Candle
        "Impulse": bool(last.get("Impulse", False)),
        "Impulse_Dir": int(last.get("Impulse_Dir", 0)),
        "Body_Ratio": last.get("Body_Ratio", 0),
        # Volume Spurt
        "Vol_Avg_5": last.get("Vol_Avg_5", 0),
        "Vol_Ratio": last.get("Vol_Ratio", 0),
        "Vol_Spurt": bool(last.get("Vol_Spurt", False)),
    }
