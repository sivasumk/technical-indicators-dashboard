"""Pre-built scan condition presets."""


PRESETS = {
    "Bullish Momentum": {
        "description": "RSI bullish + MACD positive + ADX trending up",
        "filter": lambda s: (
            s["signals"]["RSI_EMA"]["score"] == 1
            and s["signals"]["MACD"]["score"] == 1
            and s["signals"]["DMI"]["score"] == 1
        ),
    },
    "Oversold Bounce": {
        "description": "SMI oversold + RSI low + MACD histogram turning positive",
        "filter": lambda s: (
            s["signals"]["SMI"]["score"] == 1  # oversold = potential bounce
            and s["signals"]["MACD"]["score"] == 1
        ),
    },
    "Bearish Breakdown": {
        "description": "All momentum indicators bearish",
        "filter": lambda s: (
            s["signals"]["RSI_EMA"]["score"] == -1
            and s["signals"]["MACD"]["score"] == -1
            and s["signals"]["DMI"]["score"] == -1
        ),
    },
    "Strong Buy": {
        "description": "Composite score >= 3",
        "filter": lambda s: s["composite_score"] >= 3,
    },
    "Strong Sell": {
        "description": "Composite score <= -3",
        "filter": lambda s: s["composite_score"] <= -3,
    },
    "Volume Breakout": {
        "description": "OBV accumulation + bullish momentum",
        "filter": lambda s: (
            s["signals"]["OBV"]["score"] == 1
            and s["signals"]["ROC_Diff"]["score"] == 1
            and s["signals"]["MACD"]["score"] == 1
        ),
    },
    "Impulse + Volume Spurt": {
        "description": "Bullish impulse candle with 2x+ volume spurt",
        "filter": lambda s: (
            s["signals"]["Impulse"]["score"] == 1
            and "Spurt" in s["signals"]["Vol_Spurt"]["label"]
        ),
    },
    "Bearish Impulse": {
        "description": "Bearish impulse candle (large red body, small wicks)",
        "filter": lambda s: s["signals"]["Impulse"]["score"] == -1,
    },
}
