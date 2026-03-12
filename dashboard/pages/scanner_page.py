"""Scanner page — filter stocks by preset or custom conditions."""

import streamlit as st
import pandas as pd

from scanner.conditions import PRESETS
from scanner.scanner import apply_preset
from dashboard.components.tables import (
    format_overview_df, style_verdict, style_score, style_change,
    style_signal_label, style_impulse, style_vol_spurt, style_smi_cross,
)


def render(scan_df, stock_data):
    """Render the scanner page."""
    st.header("Stock Scanner")

    if scan_df.empty:
        st.warning("No data available. Click 'Refresh Data' in the sidebar.")
        return

    # Preset selector
    preset_names = list(PRESETS.keys())
    selected_preset = st.selectbox(
        "Scan Preset",
        options=["All Stocks"] + preset_names,
        index=0,
    )

    # Show preset description
    if selected_preset != "All Stocks":
        st.caption(PRESETS[selected_preset]["description"])

    # Custom filters
    st.subheader("Custom Filters")
    col1, col2, col3 = st.columns(3)
    with col1:
        min_score = st.slider("Min Score", -6, 6, -6)
        max_score = st.slider("Max Score", -6, 6, 6)
    with col2:
        min_adx = st.slider("Min ADX", 0, 100, 0)
        rsi_range = st.slider("RSI 14 Range", 0, 100, (0, 100))
    with col3:
        min_change = st.number_input("Min Change%", value=-100.0, step=0.5)
        max_change = st.number_input("Max Change%", value=100.0, step=0.5)

    # Apply filters
    if st.button("Scan Now", type="primary"):
        with st.spinner("Scanning..."):
            filtered = scan_df.copy()

            # Apply preset
            if selected_preset != "All Stocks":
                filtered = apply_preset(filtered, stock_data, selected_preset)

            # Apply custom filters
            filtered = filtered[
                (filtered["Score"] >= min_score)
                & (filtered["Score"] <= max_score)
                & (filtered["ADX"] >= min_adx)
                & (filtered["RSI_14"] >= rsi_range[0])
                & (filtered["RSI_14"] <= rsi_range[1])
                & (filtered["Change%"] >= min_change)
                & (filtered["Change%"] <= max_change)
            ]

            st.session_state["scan_results"] = filtered

    # Display results
    results = st.session_state.get("scan_results", scan_df)

    st.subheader(f"Results: {len(results)} stocks")

    display_cols = [
        "Symbol", "Close", "Change%", "RSI_14", "SMI", "ADX",
        "Plus_DI", "Minus_DI", "MACD_Hist", "OBV",
        "ROC_Diff", "ATR", "Score", "Verdict",
    ]
    available = [c for c in display_cols if c in results.columns]
    label_cols = [c for c in results.columns if c.endswith("_Label")]
    show_cols = available + label_cols

    formatted = format_overview_df(results[show_cols])

    styled = formatted.style
    if "Verdict" in formatted.columns:
        styled = styled.map(style_verdict, subset=["Verdict"])
    if "Score" in formatted.columns:
        styled = styled.map(style_score, subset=["Score"])
    if "Change%" in formatted.columns:
        styled = styled.map(style_change, subset=["Change%"])

    sig_cols = [c for c in formatted.columns if c.endswith(" Sig")]
    for col in sig_cols:
        if "Impulse" in col:
            styled = styled.map(style_impulse, subset=[col])
        elif "Vol_Spurt" in col:
            styled = styled.map(style_vol_spurt, subset=[col])
        elif "SMI" in col:
            styled = styled.map(style_smi_cross, subset=[col])
        else:
            styled = styled.map(style_signal_label, subset=[col])

    st.dataframe(styled, use_container_width=True, height=500)
