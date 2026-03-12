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
        "Close": round(last.get("Close", 0), 2),
        "Volume": last.get("Volume", 0),
        "Change%": round(((last["Close"] - prev["Close"]) / prev["Close"] * 100)
        if prev["Close"] != 0 else 0, 2),
        "EMA_5": round(last.get("EMA_5", 0), 2),
        "SMI": round(last.get("SMI", 0), 2),
        "SMI_Signal": round(last.get("SMI_Signal", 0), 2),
        "SMI_Bull_Cross": bool(last.get("SMI_Bull_Cross", False)),
        "SMI_Bear_Cross": bool(last.get("SMI_Bear_Cross", False)),
        "RSI_5": round(last.get("RSI_5", 0), 2),
        "RSI_14": round(last.get("RSI_14", 0), 2),
        "RSI_EMA_5": round(last.get("RSI_EMA_5", 0), 2),
        "RSI_EMA_55": round(last.get("RSI_EMA_55", 0), 2),
        "RSI_Signal": last.get("RSI_Signal", 0),
        "Plus_DI": round(last.get("Plus_DI", 0), 2),
        "Minus_DI": round(last.get("Minus_DI", 0), 2),
        "ADX": round(last.get("ADX", 0), 2),
        "OBV": round(last.get("OBV", 0), 2),
        "OBV_EMA": round(last.get("OBV_EMA", 0), 2),
        "ROC_Diff": round(last.get("ROC_Diff", 0), 2),
        "ROC_Diff_Smooth": round(last.get("ROC_Diff_Smooth", 0), 2),
        "ATR": round(last.get("ATR", 0), 2),
        "ATR_RMA": round(last.get("ATR_RMA", 0), 2),
        "MACD": round(last.get("MACD", 0), 2),
        "MACD_Signal": round(last.get("MACD_Signal", 0), 2),
        "MACD_Hist": round(last.get("MACD_Hist", 0), 2),
        # Impulse Candle
        "Impulse": bool(last.get("Impulse", False)),
        "Impulse_Dir": int(last.get("Impulse_Dir", 0)),
        "Body_Ratio": round(last.get("Body_Ratio", 0), 2),
        # Volume Spurt
        "Vol_Avg_5": round(last.get("Vol_Avg_5", 0), 2),
        "Vol_Ratio": round(last.get("Vol_Ratio", 0), 2),
        "Vol_Spurt": bool(last.get("Vol_Spurt", False)),
    }
