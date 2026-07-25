import pandas as pd
import streamlit as st

from app.lib.data import load_presence_matrix
from app.lib.stats import association_by_timeslot
from app.lib.theme import card_title, stat_list

st.title("Business insights")
st.markdown(
    "The Methodology page explains why Cramer's V, not the p-value, drives these "
    "rankings. This page is about what that ranking means on the shop floor: which "
    "pairs to bundle, and when to run the promotion."
)

presence = load_presence_matrix()


def _v_for(cat_a: str, cat_b: str, slot: str, by_slot: pd.DataFrame) -> float:
    match = by_slot[
        (by_slot["Time Slot"] == slot)
        & (
            ((by_slot["Category A"] == cat_a) & (by_slot["Category B"] == cat_b))
            | ((by_slot["Category A"] == cat_b) & (by_slot["Category B"] == cat_a))
        )
    ]
    return float(match.iloc[0]["Cramers V"]) if not match.empty else float("nan")


with st.container():
    card_title("A dinner pattern, not a restock")
    by_slot_produce_meat = association_by_timeslot(
        presence, ["Fruits and vegetables", "Meats and sausages"]
    )
    v_evening = _v_for("Fruits and vegetables", "Meats and sausages", "Evening", by_slot_produce_meat)
    v_morning = _v_for("Fruits and vegetables", "Meats and sausages", "Morning", by_slot_produce_meat)
    v_afternoon = _v_for("Fruits and vegetables", "Meats and sausages", "Afternoon", by_slot_produce_meat)

    st.markdown(
        f"Fruits and vegetables plus meats and sausages peaks in the evening "
        f"(V = {v_evening:.4f}), clearly ahead of morning (V = {v_morning:.4f}) and "
        f"afternoon (V = {v_afternoon:.4f}). During the day the two categories mostly "
        "get bought on their own, as separate errands. By evening they start landing "
        "in the same basket often enough that it looks less like general shopping and "
        "more like someone deciding what's for dinner."
    )
    stat_list([
        ("Best window", "18:00 to 21:00", True),
        ("Action", "dinner-bundle promotion, produce and meat aisles placed adjacent", False),
    ])

with st.container():
    card_title("Two more patterns worth knowing")
    by_slot_dairy_snacks = association_by_timeslot(
        presence, ["Dairy products and eggs", "Snacks and drinks"]
    )
    v_dairy_afternoon = _v_for(
        "Dairy products and eggs", "Snacks and drinks", "Afternoon", by_slot_dairy_snacks
    )
    by_slot_clean_snacks = association_by_timeslot(presence, ["Home cleaning", "Snacks and drinks"])
    v_clean_morning = _v_for("Home cleaning", "Snacks and drinks", "Morning", by_slot_clean_snacks)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Dairy & eggs + snacks** (V = {v_dairy_afternoon:.4f} in the afternoon)")
        st.markdown(
            "This one reads as an after-lunch or after-school habit: a routine grocery "
            "stop that turns into an impulse snack grab. Afternoon is when it's strongest."
        )
    with col2:
        st.markdown(f"**Home cleaning + snacks** (V = {v_clean_morning:.4f} in the morning)")
        st.markdown(
            "This pairing is strongest earlier in the day, alongside a broader household "
            "shop rather than a quick errand, consistent with someone doing the week's "
            "main run before the day gets busy."
        )

with st.container():
    card_title("Priority pairs for commercial action")
    PRIORITY_PAIRS = [
        ("Fruits and vegetables", "Meats and sausages", "Evening", "Dinner bundle promotion, 18:00-21:00"),
        ("Dairy products and eggs", "Snacks and drinks", "Afternoon", "Combo discount, 12:00-17:00"),
        ("Home cleaning", "Snacks and drinks", "Morning", "Morning loyalty bundle"),
        ("Dairy products and eggs", "Home cleaning", "Afternoon", "Adjacent aisle placement"),
        ("Dairy products and eggs", "Fruits and vegetables", "Afternoon", "Fresh-products cross-promotion"),
    ]
    rows = []
    for cat_a, cat_b, slot, action in PRIORITY_PAIRS:
        by_slot = association_by_timeslot(presence, [cat_a, cat_b])
        v = _v_for(cat_a, cat_b, slot, by_slot)
        rows.append({"Pair": f"{cat_a} + {cat_b}", "Best time slot": slot, "Cramer's V": round(v, 4), "Action": action})

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.markdown(
        "A single global analysis, without splitting by time slot, would have flagged "
        "the same 15 pairs as significant. It just wouldn't have said when each one "
        "actually shows up, which is the part a promotions calendar needs. That's the "
        "whole argument for the temporal split running through this project."
    )
