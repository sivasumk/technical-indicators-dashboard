"""Streamlit Cloud entry point — runs the dashboard app."""

import sys
import os

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dashboard.app import main

main()
