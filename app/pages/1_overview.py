import plotly.graph_objects as go
import streamlit as st

from app.lib.data import (
    CATEGORIES,
    CATEGORY_COLOR_KEY,
    SHORT_NAME,
    TIME_SLOTS,
    load_presence_matrix,
    load_transactions,
)
from app.lib.stats import compute_association_table, cooccurrence_matrix
from app.lib.theme import card_title, category_legend, kpi_row

st.title("Retail product association analysis")
st.markdown(
    """
    This project tests whether product categories in a supermarket basket are
    statistically independent, or whether some pairings show up together more
    than chance would predict. It also asks whether that changes across the day.
    All statistics on this page are recomputed live from `retail_ecuador.db`,
    the same SQLite database built in `notebooks/00_generate_dataset.ipynb`.
    """
)

transactions = load_transactions()
presence = load_presence_matrix()
table = compute_association_table(presence, CATEGORIES, TIME_SLOTS)

n_significant = int(table["Significant"].sum())
n_pairs = len(table)
top = table.iloc[0]

with st.container():
    card_title("At a glance")
    kpi_row([
        ("Transactions", f"{len(transactions):,}", "Jan-Dec 2024, 3 Ecuadorian cities"),
        ("Significant pairs", f"{n_significant} / {n_pairs}", "chi-squared test, p < 0.05"),
        ("Strongest association", f"{top['Cramers V']:.4f}", f"{SHORT_NAME[top['Category A']]} + {SHORT_NAME[top['Category B']]}"),
    ])

with st.container():
    card_title("Product categories")
    category_legend(CATEGORIES, CATEGORY_COLOR_KEY, SHORT_NAME)

with st.container():
    card_title("Global co-purchase frequency")
    st.caption("How often each pair of categories appears together in the same transaction, across all time slots.")

    counts = cooccurrence_matrix(presence, CATEGORIES, TIME_SLOTS)
    fig = go.Figure(
        data=go.Heatmap(
            z=counts.values,
            x=[SHORT_NAME[c] for c in CATEGORIES],
            y=[SHORT_NAME[c] for c in CATEGORIES],
            colorscale=[[0, "#EEF3F8"], [1, "#3B82F6"]],
            hovertemplate="%{y} + %{x}<br>Co-purchases: %{z}<extra></extra>",
            showscale=False,
        )
    )
    fig.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#16202A"),
        yaxis=dict(autorange="reversed"),
    )
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    card_title("Reading this app")
    st.markdown(
        "**Overview** is this page. **Explorer** lets you filter by time slot and "
        "category with everything recomputed live. **Methodology** explains chi-squared, "
        "Cramer's V and odds ratio. **Business insights** turns the strongest patterns "
        "into what to promote, and when."
    )
