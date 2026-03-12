"""Plotly chart builders for stock detail view."""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


def build_stock_chart(df, symbol_name):
    """Build a full multi-panel chart mimicking the TradingView layout."""

    fig = make_subplots(
        rows=8, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        row_heights=[0.25, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
        subplot_titles=[
            f"{symbol_name} - Price", "SMI (10,3,3)", "RSI EMA (14,5,55)",
            "DMI/ADX (14,14)", "OBV", "ROC Diff (5,16,3)",
            "ATR (14,34)", "MACD (12,26,9)"
        ],
    )

    # --- Panel 1: Line chart + EMA ---
    fig.add_trace(go.Scatter(
        x=df.index, y=df["Close"], name="Close",
        line=dict(color="#E0E0E0", width=1.5),
        fill="tozeroy", fillcolor="rgba(224,224,224,0.05)",
    ), row=1, col=1)

    if "EMA_5" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["EMA_5"], name="EMA 5",
            line=dict(color="#2196F3", width=1),
        ), row=1, col=1)

    # Volume as bar chart overlay — highlight spurts in orange
    vol_colors = []
    for i in range(len(df)):
        row = df.iloc[i]
        if row.get("Vol_Spurt", False):
            vol_colors.append("#FF6D00")  # bright orange for spurt
        elif row["Close"] >= row["Open"]:
            vol_colors.append("#26a69a")
        else:
            vol_colors.append("#ef5350")
    fig.add_trace(go.Bar(
        x=df.index, y=df["Volume"], name="Volume",
        marker_color=vol_colors, opacity=0.4,
    ), row=1, col=1)

    # Mark impulse candles with triangles on the price chart
    if "Impulse_Dir" in df.columns:
        bull_impulse = df[df["Impulse_Dir"] == 1]
        bear_impulse = df[df["Impulse_Dir"] == -1]
        if not bull_impulse.empty:
            fig.add_trace(go.Scatter(
                x=bull_impulse.index, y=bull_impulse["Close"] * 0.99,
                mode="markers", name="Bull Impulse",
                marker=dict(symbol="triangle-up", size=10, color="#00E676"),
            ), row=1, col=1)
        if not bear_impulse.empty:
            fig.add_trace(go.Scatter(
                x=bear_impulse.index, y=bear_impulse["Close"] * 1.01,
                mode="markers", name="Bear Impulse",
                marker=dict(symbol="triangle-down", size=10, color="#FF1744"),
            ), row=1, col=1)

    # Mark SMI crossovers on the price chart
    if "SMI_Bull_Cross" in df.columns:
        smi_bull = df[df["SMI_Bull_Cross"] == True]
        if not smi_bull.empty:
            fig.add_trace(go.Scatter(
                x=smi_bull.index, y=smi_bull["Close"] * 0.985,
                mode="markers", name="SMI Bull Cross",
                marker=dict(symbol="star", size=14, color="#00E676",
                            line=dict(width=1, color="white")),
            ), row=1, col=1)
    if "SMI_Bear_Cross" in df.columns:
        smi_bear = df[df["SMI_Bear_Cross"] == True]
        if not smi_bear.empty:
            fig.add_trace(go.Scatter(
                x=smi_bear.index, y=smi_bear["Close"] * 1.015,
                mode="markers", name="SMI Bear Cross",
                marker=dict(symbol="star", size=14, color="#FF1744",
                            line=dict(width=1, color="white")),
            ), row=1, col=1)

    # --- Panel 2: SMI ---
    if "SMI" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["SMI"], name="SMI",
            line=dict(color="#2196F3", width=1),
        ), row=2, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=df["SMI_Signal"], name="SMI Signal",
            line=dict(color="#FF9800", width=1),
        ), row=2, col=1)
        fig.add_hline(y=40, line_dash="dash", line_color="gray", opacity=0.5, row=2, col=1)
        fig.add_hline(y=-40, line_dash="dash", line_color="gray", opacity=0.5, row=2, col=1)

        # SMI bullish crossover markers
        if "SMI_Bull_Cross" in df.columns:
            bull_cross = df[df["SMI_Bull_Cross"] == True]
            if not bull_cross.empty:
                fig.add_trace(go.Scatter(
                    x=bull_cross.index, y=bull_cross["SMI"],
                    mode="markers", name="SMI Bull Cross",
                    marker=dict(symbol="triangle-up", size=12, color="#00E676",
                                line=dict(width=1, color="white")),
                ), row=2, col=1)

        # SMI bearish crossover markers
        if "SMI_Bear_Cross" in df.columns:
            bear_cross = df[df["SMI_Bear_Cross"] == True]
            if not bear_cross.empty:
                fig.add_trace(go.Scatter(
                    x=bear_cross.index, y=bear_cross["SMI"],
                    mode="markers", name="SMI Bear Cross",
                    marker=dict(symbol="triangle-down", size=12, color="#FF1744",
                                line=dict(width=1, color="white")),
                ), row=2, col=1)

    # --- Panel 3: RSI with EMAs ---
    if "RSI_14" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["RSI_14"], name="RSI 14",
            line=dict(color="#9C27B0", width=1),
        ), row=3, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=df["RSI_5"], name="RSI 5",
            line=dict(color="#E91E63", width=1),
        ), row=3, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=df["RSI_EMA_5"], name="RSI EMA 5",
            line=dict(color="#FFEB3B", width=1.5),
        ), row=3, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=df["RSI_EMA_55"], name="RSI EMA 55",
            line=dict(color="#00BCD4", width=1.5),
        ), row=3, col=1)
        fig.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.5, row=3, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.5, row=3, col=1)

    # --- Panel 4: DMI/ADX ---
    if "Plus_DI" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["Plus_DI"], name="+DI",
            line=dict(color="#4CAF50", width=1),
        ), row=4, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=df["Minus_DI"], name="-DI",
            line=dict(color="#F44336", width=1),
        ), row=4, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=df["ADX"], name="ADX",
            line=dict(color="white", width=1.5),
        ), row=4, col=1)
        fig.add_hline(y=25, line_dash="dash", line_color="gray", opacity=0.5, row=4, col=1)

    # --- Panel 5: OBV ---
    if "OBV" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["OBV"], name="OBV",
            line=dict(color="#4CAF50", width=1),
        ), row=5, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=df["OBV_EMA"], name="OBV EMA",
            line=dict(color="#FFC107", width=1),
        ), row=5, col=1)

    # --- Panel 6: ROC Diff ---
    if "ROC_Diff" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["ROC_Diff"], name="ROC Diff",
            line=dict(color="#E91E63", width=1),
        ), row=6, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=df["ROC_Diff_Smooth"], name="ROC Smooth",
            line=dict(color="#4CAF50", width=1),
        ), row=6, col=1)
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5, row=6, col=1)

    # --- Panel 7: ATR ---
    if "ATR" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["ATR"], name="ATR",
            line=dict(color="#2196F3", width=1),
        ), row=7, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=df["ATR_RMA"], name="ATR RMA",
            line=dict(color="#FF9800", width=1),
        ), row=7, col=1)

    # --- Panel 8: MACD ---
    if "MACD" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["MACD"], name="MACD",
            line=dict(color="#2196F3", width=1),
        ), row=8, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=df["MACD_Signal"], name="Signal",
            line=dict(color="#FF9800", width=1),
        ), row=8, col=1)
        hist_colors = ["#26a69a" if v >= 0 else "#ef5350" for v in df["MACD_Hist"]]
        fig.add_trace(go.Bar(
            x=df.index, y=df["MACD_Hist"], name="Histogram",
            marker_color=hist_colors,
        ), row=8, col=1)
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5, row=8, col=1)

    # Layout
    fig.update_layout(
        height=1600,
        template="plotly_dark",
        showlegend=False,
        xaxis_rangeslider_visible=False,
        margin=dict(l=50, r=50, t=30, b=30),
    )

    # Hide rangesliders and weekends
    for i in range(1, 9):
        xaxis = f"xaxis{i}" if i > 1 else "xaxis"
        fig.update_layout(**{xaxis: dict(
            rangeslider=dict(visible=False),
            rangebreaks=[dict(bounds=["sat", "mon"])],
        )})

    return fig
