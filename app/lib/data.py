"""Data access layer: reads the raw transactions straight from the SQLite
database generated in notebooks/00_generate_dataset.ipynb, so the app always
recomputes statistics from source rather than from pre-baked CSVs."""

from pathlib import Path
import sqlite3

import pandas as pd
import streamlit as st

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "retail_ecuador.db"

CATEGORIES = [
    "Dairy products and eggs",
    "Meats and sausages",
    "Fruits and vegetables",
    "Snacks and drinks",
    "Home cleaning",
    "Personal care",
]

TIME_SLOTS = ["Morning", "Afternoon", "Evening"]

# maps a category to the design-token color key used in theme.py
CATEGORY_COLOR_KEY = {
    "Dairy products and eggs": "dairy",
    "Meats and sausages": "meats",
    "Fruits and vegetables": "produce",
    "Snacks and drinks": "snacks",
    "Home cleaning": "cleaning",
    "Personal care": "care",
}

SHORT_NAME = {
    "Dairy products and eggs": "Dairy & eggs",
    "Meats and sausages": "Meats",
    "Fruits and vegetables": "Fruits & veg",
    "Snacks and drinks": "Snacks & drinks",
    "Home cleaning": "Home cleaning",
    "Personal care": "Personal care",
}


@st.cache_data(show_spinner=False)
def load_transactions() -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query("SELECT * FROM transactions", conn)
    finally:
        conn.close()
    return df


@st.cache_data(show_spinner=False)
def load_presence_matrix() -> pd.DataFrame:
    """One row per transaction: context columns plus a 0/1 column per category."""
    df = load_transactions()
    presence = pd.DataFrame(0, index=df.index, columns=CATEGORIES)
    for cat in CATEGORIES:
        presence[cat] = df["categories"].str.contains(cat, regex=False).astype(int)
    context_cols = [
        "transaction_id", "date", "time", "day_of_week", "time_slot",
        "city", "customer_type", "payment_method",
    ]
    return pd.concat([df[context_cols], presence], axis=1)
