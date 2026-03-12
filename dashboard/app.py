"""Main Streamlit dashboard application."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

from data.symbols import get_symbols
from data.fetcher import fetch_all, get_last_update_time
from scanner.scanner import scan_all
from dashboard.pages import overview, scanner_page, stock_detail

st.set_page_config(
    page_title="Technical Indicators Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(ttl=300)
def load_data(universe):
    """Fetch and cache stock data."""
    symbols = get_symbols(universe)
    return fetch_all(symbols)


@st.cache_data(ttl=300)
def run_scan(_stock_data):
    """Run scanner on all stocks."""
    return scan_all(_stock_data)


def main():
    # Sidebar
    st.sidebar.title("📊 TI Dashboard")

    universe = st.sidebar.selectbox(
        "Stock Universe",
        options=["nifty50", "nifty200"],
        index=0,
        format_func=lambda x: x.upper().replace("NIFTY", "Nifty "),
    )

    if st.sidebar.button("🔄 Refresh Data", type="primary"):
        st.cache_data.clear()
        st.rerun()

    # Last update time
    last_update = get_last_update_time()
    if last_update:
        st.sidebar.caption(f"Last updated: {last_update.strftime('%Y-%m-%d %H:%M IST')}")

    # Navigation
    page = st.sidebar.radio(
        "Navigation",
        options=["Overview", "Scanner", "Stock Detail"],
        index=0,
    )

    st.sidebar.divider()
    st.sidebar.caption("Data: Yahoo Finance | Indicators: Custom")

    # Load data
    with st.spinner(f"Loading {universe} data..."):
        stock_data = load_data(universe)

    if not stock_data:
        st.error("Failed to load stock data. Check your internet connection.")
        return

    with st.spinner("Computing indicators..."):
        scan_df = run_scan(stock_data)

    # Render page
    if page == "Overview":
        overview.render(scan_df)
    elif page == "Scanner":
        scanner_page.render(scan_df, stock_data)
    elif page == "Stock Detail":
        stock_detail.render(scan_df, stock_data)


if __name__ == "__main__":
    main()
