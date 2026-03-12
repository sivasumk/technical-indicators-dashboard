"""Convert indicator values into BUY/SELL/NEUTRAL signals."""

import numpy as np
from config import SMI_OVERSOLD, SMI_OVERBOUGHT, ADX_TREND_THRESHOLD


def smi_signal(values):
    """SMI signal: fresh crossover takes priority, then oversold/overbought."""
    bull_cross = values.get("SMI_Bull_Cross", False)
    bear_cross = values.get("SMI_Bear_Cross", False)
    smi = values.get("SMI", 0)

    if bull_cross:
        return 1, "Bull Cross"
    elif bear_cross:
        return -1, "Bear Cross"
    elif smi < SMI_OVERSOLD:
        return 1, "Oversold"
    elif smi > SMI_OVERBOUGHT:
        return -1, "Overbought"
    return 0, "Neutral"


def rsi_ema_signal(values):
    """RSI EMA crossover: fast > slow = Bullish."""
    sig = values.get("RSI_Signal", 0)
    if sig == 1:
        return 1, "Bullish"
    return -1, "Bearish"


def dmi_signal(values):
    """DMI: +DI > -DI with strong ADX = Bullish."""
    plus_di = values.get("Plus_DI", 0)
    minus_di = values.get("Minus_DI", 0)
    adx = values.get("ADX", 0)

    if adx < ADX_TREND_THRESHOLD:
        return 0, "No Trend"
    if plus_di > minus_di:
        return 1, "Bullish Trend"
    return -1, "Bearish Trend"


def obv_signal(values):
    """OBV: above EMA = accumulation, below = distribution."""
    obv = values.get("OBV", 0)
    obv_ema = values.get("OBV_EMA", 0)
    if obv > obv_ema:
        return 1, "Accumulation"
    return -1, "Distribution"


def roc_diff_signal(values):
    """ROC Diff: above smooth = bullish momentum."""
    diff = values.get("ROC_Diff", 0)
    smooth = values.get("ROC_Diff_Smooth", 0)
    if diff > smooth:
        return 1, "Bullish"
    return -1, "Bearish"


def macd_signal(values):
    """MACD: positive histogram = bullish."""
    hist = values.get("MACD_Hist", 0)
    if hist > 0:
        return 1, "Bullish"
    return -1, "Bearish"


def atr_signal(values):
    """ATR: above RMA = high volatility."""
    atr_val = values.get("ATR", 0)
    rma = values.get("ATR_RMA", 0)
    if atr_val > rma:
        return 0, "High Vol"
    return 0, "Low Vol"


def impulse_signal(values):
    """Impulse candle: bullish impulse=BUY, bearish impulse=SELL."""
    impulse_dir = values.get("Impulse_Dir", 0)
    if impulse_dir == 1:
        return 1, "Bull Impulse"
    elif impulse_dir == -1:
        return -1, "Bear Impulse"
    return 0, "No Impulse"


def volume_spurt_signal(values):
    """Volume Spurt: 2x+ avg volume = notable activity."""
    spurt = values.get("Vol_Spurt", False)
    ratio = values.get("Vol_Ratio", 0)
    if spurt:
        return 0, f"Spurt {ratio:.1f}x"
    return 0, "Normal"


ALL_SIGNALS = {
    "SMI": smi_signal,
    "RSI_EMA": rsi_ema_signal,
    "DMI": dmi_signal,
    "OBV": obv_signal,
    "ROC_Diff": roc_diff_signal,
    "MACD": macd_signal,
    "ATR": atr_signal,
    "Impulse": impulse_signal,
    "Vol_Spurt": volume_spurt_signal,
}


def compute_signals(values):
    """Compute all signals and composite score."""
    signals = {}
    score = 0
    for name, func in ALL_SIGNALS.items():
        val, label = func(values)
        signals[name] = {"score": val, "label": label}
        score += val

    # Overall verdict
    if score >= 3:
        verdict = "STRONG BUY"
    elif score >= 1:
        verdict = "BUY"
    elif score <= -3:
        verdict = "STRONG SELL"
    elif score <= -1:
        verdict = "SELL"
    else:
        verdict = "NEUTRAL"

    return {
        "signals": signals,
        "composite_score": score,
        "verdict": verdict,
    }
