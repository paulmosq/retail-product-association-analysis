from pathlib import Path

import streamlit as st

from app.lib.theme import inject_theme

st.set_page_config(
    page_title="Retail Product Association Analysis",
    page_icon="🧾",
    layout="wide",
)
inject_theme()

PAGES_DIR = Path(__file__).parent / "app" / "pages"

pages = [
    st.Page(str(PAGES_DIR / "1_overview.py"), title="Overview", icon=":material/receipt_long:", default=True),
    st.Page(str(PAGES_DIR / "2_explorer.py"), title="Explorer", icon=":material/filter_alt:"),
    st.Page(str(PAGES_DIR / "3_methodology.py"), title="Methodology", icon=":material/functions:"),
    st.Page(str(PAGES_DIR / "4_insights.py"), title="Business insights", icon=":material/lightbulb:"),
]

nav = st.navigation(pages)
nav.run()
