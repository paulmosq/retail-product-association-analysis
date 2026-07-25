import pandas as pd
import streamlit as st

from app.lib.data import TIME_SLOTS, load_presence_matrix
from app.lib.stats import contingency_table, cramers_v, odds_ratio
from app.lib.theme import card_title, stat_list

st.title("Methodology")
st.markdown(
    "Three techniques, applied to every pair of product categories, and repeated "
    "per time slot to see whether the association itself shifts across the day."
)

presence = load_presence_matrix()

with st.container():
    card_title("1. Chi-squared test of independence")
    st.markdown(
        "For a pair of categories A and B, transactions get cross-tabulated into a "
        "2x2 table (both present, only A, only B, neither) and tested against the "
        "null hypothesis that the two categories are purchased independently."
    )
    st.latex(r"\chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}")

    st.markdown("**Worked example**: dairy & eggs vs. meats & sausages, all transactions.")
    example_table = contingency_table(presence, "Dairy products and eggs", "Meats and sausages")
    example_table.index = ["No dairy & eggs", "Dairy & eggs"]
    example_table.columns = ["No meats", "Meats"]
    st.dataframe(example_table, use_container_width=False)

    chi2, p, dof, v = cramers_v(example_table)
    stat_list([
        ("Chi-squared", f"{chi2:.4f}", False),
        ("Degrees of freedom", f"{dof}", False),
        ("p-value", f"{p:.4f}", p < 0.05),
    ])

    st.markdown(
        "**The catch**: with n = 10,000, the test has enormous statistical power. "
        "It rejects independence for almost any non-zero association, no matter how "
        "commercially trivial. All 15 category pairs in this dataset come back significant, "
        "so the p-value alone can't rank them by importance. That's what Cramer's V is for."
    )

with st.container():
    card_title("2. Cramer's V (effect size)")
    st.markdown(
        "Cramer's V rescales the chi-squared statistic into a 0-to-1 measure of "
        "association strength, independent of sample size. It is the primary metric "
        "used throughout this app to compare pairs and time slots."
    )
    st.latex(r"V = \sqrt{\dfrac{\chi^2}{n \cdot (\min(r, c) - 1)}}")

    both, only_a, only_b, neither = (
        int(example_table.loc["Dairy & eggs", "Meats"]),
        int(example_table.loc["Dairy & eggs", "No meats"]),
        int(example_table.loc["No dairy & eggs", "Meats"]),
        int(example_table.loc["No dairy & eggs", "No meats"]),
    )
    stat_list([("Cramer's V for this pair", f"{v:.4f}", v >= 0.10)])

    interp = pd.DataFrame({
        "Cramer's V": ["< 0.10", "0.10 - 0.30", "> 0.30"],
        "Interpretation": ["Weak association", "Moderate association", "Strong association"],
    })
    st.dataframe(interp, use_container_width=False, hide_index=True)

with st.container():
    card_title("3. Odds ratio (commercial magnitude)")
    st.markdown(
        "Where Cramer's V says how strong an association is, the odds ratio says "
        "which direction it points and by how much: the odds of buying B when A is "
        "in the basket, divided by the odds of buying B when A is not."
    )
    st.latex(r"OR = \dfrac{a \cdot d}{b \cdot c} \quad \text{where } a=\text{both},\ b=\text{only A},\ c=\text{only B},\ d=\text{neither}")
    or_value = odds_ratio(both, only_a, only_b, neither)
    stat_list([("Odds ratio for this pair", f"{or_value:.4f}", False)])
    st.caption(
        "OR above 1 means the categories reinforce each other. Below 1, buying one "
        "makes the other slightly less likely, often just a basket-size effect since "
        "every transaction has a limited number of category slots."
    )

with st.container():
    card_title("Why segment by time slot")
    st.markdown(
        f"Repeating all three tests separately for {', '.join(TIME_SLOTS)} is the "
        "core analytical move of this project. A global analysis would have found the "
        "same 15 significant pairs, but it would have missed *when* each pairing peaks, "
        "and that timing is what turns a descriptive result into a schedulable promotion. "
        "Compare any pair across time slots on the Explorer page, or see what it means "
        "for the business on the Business insights page."
    )
