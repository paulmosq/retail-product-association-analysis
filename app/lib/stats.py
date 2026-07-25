"""Association statistics: chi-squared, Cramer's V and odds ratio, recomputed
live from a presence matrix for whatever time-slot / category filter the user
picks in the Explorer page. Mirrors the functions defined in
notebooks/03_statistical_analysis.ipynb so the app and the notebook agree."""

from itertools import combinations

import numpy as np
import pandas as pd
from scipy import stats as scipy_stats

from app.lib.data import TIME_SLOTS


def cramers_v(contingency_table):
    """Chi2, p-value, degrees of freedom and Cramer's V from a contingency table."""
    chi2, p, dof, _expected = scipy_stats.chi2_contingency(contingency_table)
    n = contingency_table.to_numpy().sum()
    min_dim = min(contingency_table.shape) - 1
    v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 and n > 0 else np.nan
    return chi2, p, dof, v


def odds_ratio(both, only_a, only_b, neither):
    """Odds ratio from a 2x2 table: both present, only A, only B, neither."""
    if only_a * only_b == 0:
        return np.nan
    return (both * neither) / (only_a * only_b)


def contingency_table(subset: pd.DataFrame, cat_a: str, cat_b: str) -> pd.DataFrame:
    """2x2 contingency table for cat_a x cat_b within `subset` (already time-slot filtered)."""
    table = pd.crosstab(subset[cat_a], subset[cat_b])
    return table.reindex(index=[0, 1], columns=[0, 1], fill_value=0)


def compute_association_table(
    presence_df: pd.DataFrame, categories: list[str], time_slots: list[str]
) -> pd.DataFrame:
    """Chi2 / p-value / Cramer's V / odds ratio for every pair among `categories`,
    restricted to transactions whose time_slot is in `time_slots`."""
    slots = time_slots or TIME_SLOTS
    subset = presence_df[presence_df["time_slot"].isin(slots)]

    rows = []
    for cat_a, cat_b in combinations(categories, 2):
        table = contingency_table(subset, cat_a, cat_b)
        n = table.to_numpy().sum()
        if n == 0:
            continue
        both = int(table.loc[1, 1])
        only_a = int(table.loc[1, 0])
        only_b = int(table.loc[0, 1])
        neither = int(table.loc[0, 0])
        chi2, p, _dof, v = cramers_v(table)
        or_ = odds_ratio(both, only_a, only_b, neither)
        rows.append({
            "Category A": cat_a,
            "Category B": cat_b,
            "Both": both,
            "Only A": only_a,
            "Only B": only_b,
            "Neither": neither,
            "Chi2": round(float(chi2), 4),
            "p-value": round(float(p), 4),
            "Significant": bool(p < 0.05),
            "Cramers V": round(float(v), 4) if not np.isnan(v) else np.nan,
            "Odds Ratio": round(float(or_), 4) if not np.isnan(or_) else np.nan,
        })

    return (
        pd.DataFrame(rows)
        .sort_values("Cramers V", ascending=False, na_position="last")
        .reset_index(drop=True)
    )


def association_by_timeslot(presence_df: pd.DataFrame, categories: list[str]) -> pd.DataFrame:
    """Same table as compute_association_table, but broken out by every canonical
    time slot at once (regardless of the user's time-slot filter) so pairs can be
    compared Morning vs Afternoon vs Evening."""
    frames = []
    for slot in TIME_SLOTS:
        t = compute_association_table(presence_df, categories, [slot])
        if t.empty:
            continue
        t.insert(0, "Time Slot", slot)
        frames.append(t)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def cooccurrence_matrix(
    presence_df: pd.DataFrame, categories: list[str], time_slots: list[str]
) -> pd.DataFrame:
    """Symmetric co-purchase count matrix among `categories`, diagonal masked."""
    slots = time_slots or TIME_SLOTS
    subset = presence_df[presence_df["time_slot"].isin(slots)]
    mat = pd.DataFrame(index=categories, columns=categories, dtype=float)
    for cat_a in categories:
        for cat_b in categories:
            if cat_a == cat_b:
                mat.loc[cat_a, cat_b] = np.nan
            else:
                mat.loc[cat_a, cat_b] = float(
                    ((subset[cat_a] == 1) & (subset[cat_b] == 1)).sum()
                )
    return mat
