import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app.lib.data import CATEGORIES, CATEGORY_COLOR_KEY, SHORT_NAME, TIME_SLOTS, load_presence_matrix
from app.lib.stats import association_by_timeslot, compute_association_table, cooccurrence_matrix
from app.lib.theme import card_title, category_legend, significance_pill

TIME_SLOT_COLORS = {"Morning": "#F59E0B", "Afternoon": "#3B82F6", "Evening": "#8B5CF6"}

st.title("Explorer")
st.markdown(
    "Pick the time slots and categories you care about. Every statistic below gets "
    "recalculated on the fly from the raw transactions, not read from a pre-baked "
    "results table."
)

presence = load_presence_matrix()

with st.container():
    card_title("Filters")
    filter_col1, filter_col2 = st.columns([1, 2])
    with filter_col1:
        time_slots = st.segmented_control(
            "Time slot", options=TIME_SLOTS, selection_mode="multi", default=TIME_SLOTS
        )
    with filter_col2:
        categories = st.multiselect(
            "Categories", options=CATEGORIES, default=CATEGORIES, format_func=SHORT_NAME.get
        )
    category_legend(categories or CATEGORIES, CATEGORY_COLOR_KEY, SHORT_NAME)

if len(categories) < 2:
    st.warning("Pick at least two categories to compute an association.")
    st.stop()
if not time_slots:
    st.warning("Pick at least one time slot.")
    st.stop()

table = compute_association_table(presence, categories, time_slots)
if table.empty:
    st.info("No co-purchases found for this combination of filters.")
    st.stop()

counts = cooccurrence_matrix(presence, categories, time_slots)
by_slot = association_by_timeslot(presence, categories)

with st.container():
    card_title("Co-purchase frequency")
    heat = go.Figure(
        data=go.Heatmap(
            z=counts.values,
            x=[SHORT_NAME[c] for c in categories],
            y=[SHORT_NAME[c] for c in categories],
            colorscale=[[0, "#EEF3F8"], [1, "#3B82F6"]],
            hovertemplate="%{y} + %{x}<br>Co-purchases: %{z}<extra></extra>",
            showscale=False,
        )
    )
    heat.update_layout(
        height=380,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#16202A"),
        yaxis=dict(autorange="reversed"),
    )
    st.plotly_chart(heat, use_container_width=True)

with st.container():
    card_title("Cramer's V by time slot")
    st.caption("Association strength for every pair, split by time slot. This is the core comparison of the project.")
    by_slot["Pair"] = by_slot["Category A"].map(SHORT_NAME) + " + " + by_slot["Category B"].map(SHORT_NAME)
    bar = px.bar(
        by_slot,
        x="Pair",
        y="Cramers V",
        color="Time Slot",
        barmode="group",
        color_discrete_map=TIME_SLOT_COLORS,
        labels={"Cramers V": "Cramer's V"},
    )
    bar.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#16202A"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        xaxis=dict(tickangle=-30),
    )
    st.plotly_chart(bar, use_container_width=True)

with st.container():
    card_title("Results table")
    top_pair = table.iloc[0]
    st.markdown(
        significance_pill(True, "Strongest in this selection")
        + f" &nbsp; {SHORT_NAME[top_pair['Category A']]} + "
        f"{SHORT_NAME[top_pair['Category B']]} (V = {top_pair['Cramers V']:.4f})",
        unsafe_allow_html=True,
    )

    display_table = table.rename(columns={"Cramers V": "Cramer's V"})
    st.dataframe(
        display_table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Significant": st.column_config.CheckboxColumn("Significant", disabled=True),
            "p-value": st.column_config.NumberColumn("p-value", format="%.4f"),
            "Cramer's V": st.column_config.NumberColumn("Cramer's V", format="%.4f"),
            "Odds Ratio": st.column_config.NumberColumn("Odds Ratio", format="%.4f"),
        },
    )

    st.download_button(
        "Download results as CSV",
        data=display_table.to_csv(index=False).encode("utf-8"),
        file_name="association_results.csv",
        mime="text/csv",
    )
