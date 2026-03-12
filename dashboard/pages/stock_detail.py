"""Stock Detail page — full chart with all indicator panels."""

import streamlit as st

from data.symbols import symbol_display_name
from indicators.engine import compute_all, get_latest_values
from scanner.signals import compute_signals
from dashboard.components.charts import build_stock_chart


def render(scan_df, stock_data):
    """Render the stock detail page."""
    st.header("Stock Detail")

    if scan_df.empty or not stock_data:
        st.warning("No data available. Click 'Refresh Data' in the sidebar.")
        return

    # Stock selector
    symbols = scan_df["Symbol"].tolist() if not scan_df.empty else []
    default_idx = 0
    if "selected_stock" in st.session_state and st.session_state["selected_stock"] in symbols:
        default_idx = symbols.index(st.session_state["selected_stock"])

    selected = st.selectbox("Select Stock", options=symbols, index=default_idx)

    if not selected:
        return

    yf_symbol = f"{selected}.NS"
    if yf_symbol not in stock_data:
        st.error(f"No data found for {selected}")
        return

    df = stock_data[yf_symbol]
    enriched = compute_all(df)
    values = get_latest_values(enriched)
    sigs = compute_signals(values)

    # Signal summary cards
    st.subheader("Signal Summary")
    signal_items = list(sigs["signals"].items())
    cols = st.columns(len(signal_items))
    for i, (name, sig_data) in enumerate(signal_items):
        with cols[i]:
            icon = "🟢" if sig_data["score"] == 1 else "🔴" if sig_data["score"] == -1 else "⚪"
            st.metric(name, sig_data["label"], delta=f"{icon}")

    # Overall verdict
    verdict_color = {
        "STRONG BUY": "🟢🟢",
        "BUY": "🟢",
        "NEUTRAL": "⚪",
        "SELL": "🔴",
        "STRONG SELL": "🔴🔴",
    }
    v = sigs["verdict"]
    st.markdown(
        f"### {verdict_color.get(v, '')} Overall: **{v}** (Score: {sigs['composite_score']})"
    )

    # Key values
    st.subheader("Key Values")
    kv_cols = st.columns(8)
    key_vals = [
        ("Close", f"₹{values['Close']:,.2f}"),
        ("Change", f"{values['Change%']:+.2f}%"),
        ("RSI 14", f"{values['RSI_14']:.1f}"),
        ("SMI", f"{values['SMI']:.1f}"),
        ("ADX", f"{values['ADX']:.1f}"),
        ("MACD Hist", f"{values['MACD_Hist']:.2f}"),
        ("Body%", f"{values['Body_Ratio']*100:.0f}%"),
        ("Vol Ratio", f"{values['Vol_Ratio']:.1f}x"),
    ]
    for i, (label, val) in enumerate(key_vals):
        with kv_cols[i]:
            st.metric(label, val)

    # Full chart
    st.subheader("Technical Chart")
    period = st.selectbox(
        "Chart Period",
        options=["3M", "6M", "1Y"],
        index=2,
        key="chart_period",
    )
    period_map = {"3M": 63, "6M": 126, "1Y": len(enriched)}
    bars = min(period_map[period], len(enriched))
    chart_data = enriched.tail(bars)

    fig = build_stock_chart(chart_data, selected)
    st.plotly_chart(fig, use_container_width=True)
