"""Overview page — summary table of all stocks with signals."""

import streamlit as st
import pandas as pd

from dashboard.components.tables import (
    format_overview_df, style_verdict, style_score, style_change,
    style_signal_label, style_impulse, style_vol_spurt, style_smi_cross,
    OVERVIEW_COLUMNS,
)


def render(scan_df):
    """Render the overview page."""
    st.header("Market Overview")

    if scan_df.empty:
        st.warning("No data available. Click 'Refresh Data' in the sidebar.")
        return

    # Summary metrics
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        bullish = len(scan_df[scan_df["Score"] >= 1])
        st.metric("Bullish", bullish)
    with col2:
        bearish = len(scan_df[scan_df["Score"] <= -1])
        st.metric("Bearish", bearish)
    with col3:
        neutral = len(scan_df[scan_df["Score"] == 0])
        st.metric("Neutral", neutral)
    with col4:
        strong_buy = len(scan_df[scan_df["Score"] >= 3])
        st.metric("Strong Buy", strong_buy)
    with col5:
        strong_sell = len(scan_df[scan_df["Score"] <= -3])
        st.metric("Strong Sell", strong_sell)
    with col6:
        if "Impulse_Label" in scan_df.columns:
            impulse_count = len(scan_df[scan_df["Impulse_Label"].isin(["Bull Impulse", "Bear Impulse"])])
        else:
            impulse_count = 0
        st.metric("Impulse", impulse_count)
    with col7:
        if "Vol_Spurt_Label" in scan_df.columns:
            spurt_count = len(scan_df[scan_df["Vol_Spurt_Label"].str.contains("Spurt", na=False)])
        else:
            spurt_count = 0
        st.metric("Vol Spurt", spurt_count)

    st.divider()

    # Filters
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        verdict_filter = st.multiselect(
            "Filter by Verdict",
            options=["STRONG BUY", "BUY", "NEUTRAL", "SELL", "STRONG SELL"],
            default=[],
        )
    with col_f2:
        sort_col = st.selectbox(
            "Sort by",
            options=["Score", "Change%", "RSI_14", "SMI", "ADX", "MACD_Hist", "Symbol"],
            index=0,
        )

    display = scan_df.copy()
    if verdict_filter:
        display = display[display["Verdict"].isin(verdict_filter)]

    ascending = sort_col == "Symbol"
    display = display.sort_values(sort_col, ascending=ascending).reset_index(drop=True)

    # Select columns for display
    available_cols = [c for c in OVERVIEW_COLUMNS if c in display.columns]
    label_cols = [c for c in display.columns if c.endswith("_Label")]
    show_cols = available_cols + label_cols

    formatted = format_overview_df(display[show_cols])

    # Apply styling
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

    st.dataframe(styled, use_container_width=True, height=600)

    # Stock selector for detail view
    st.divider()
    selected = st.selectbox(
        "Select stock for detailed view",
        options=display["Symbol"].tolist(),
        index=0,
        key="overview_stock_select",
    )
    if selected:
        st.session_state["selected_stock"] = selected
        st.info(f"Switch to **Stock Detail** page to view {selected} charts.")
