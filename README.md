# Retail Product Association Analysis
### Statistical Analysis of Product Co-purchasing Patterns by Time Context

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite)](https://sqlite.org)


---

## Overview

This project investigates whether product category combinations in a supermarket
are statistically independent, or whether certain pairings occur significantly
more often than expected by chance.

The key differentiator is temporal segmentation: associations are tested
separately by time slot (Morning, Afternoon, Evening), revealing that purchasing
patterns shift across the day. This has direct implications for promotional
scheduling and inventory restocking decisions.

The dataset is synthetic but calibrated to reflect real purchasing patterns
of Ecuadorian supermarket chains (Supermaxi, Mi Comisariato).

---

## Business Questions:

1. Which product category pairs show statistically significant co-purchasing?
2. Do these associations vary by time of day?
3. Which associations carry the highest commercial leverage?
4. What concrete promotion and restocking decisions can be made from this?

---

## Statistical Methods

| Technique | Purpose |
|---|---|
| Contingency tables | Cross-tabulate category pairs per time segment |
| Chi-squared test | Test H₀: the two categories are purchased independently |
| Cramér's V | Quantify the strength of significant associations |
| Odds Ratio | Measure the magnitude of the commercial effect |

> **Methodological note**: With large samples (n = 10,000), the chi-squared 
> test tends to reject H₀ for virtually all pairs, a well-known limitation. 
> For this reason, Cramér's V is the primary effect size measure used to 
> compare association strength across time slots, rather than relying solely 
> on p-values.

---

## Key Findings

- **Dairy products + Snacks** show strongest association in Afternoon (V = 0.1357)
- **Fruits & Vegetables + Meats** peak in Evening (V = 0.1512), dinner preparation pattern
- **Home Cleaning + Snacks** association is strongest in Morning (V = 0.1271)
- All 15 category pairs are statistically significant (p < 0.05)
- Temporal segmentation reveals actionable patterns invisible in global analysis

---

## Dataset

Synthetic dataset generated to reflect Ecuadorian supermarket purchasing behavior.

| Column | Description |
|---|---|
| transaction_id | Unique transaction identifier |
| date | Transaction date (2024) |
| time | Transaction time |
| day_of_week | Day of the week |
| time_slot | Morning / Afternoon / Evening |
| categories | Product categories purchased (2–4 per transaction) |
| city | Quito / Guayaquil / Cuenca |
| customer_type | Regular / New |
| payment_method | Cash / Credit card / Debit card |

---

## Repository Structure
```
├── data/
│   ├── retail_ecuador.db          ← SQLite database
│   ├── transactions_clean.csv     ← Clean transaction dataset
│   └── category_pairs.csv         ← Expanded category pairs
├── notebooks/
│   ├── 00_generate_dataset.ipynb  ← Synthetic data generation
│   ├── 01_data_preparation.ipynb  ← SQL extraction and cleaning
│   ├── 02_exploratory_analysis.ipynb
│   └── 03_statistical_analysis.ipynb
├── outputs/
│   ├── figures/                   ← Exported charts
│   └── tables/                    ← Result tables
└── reports/
    └── business_insights.md       ← Business recommendations
```

---

## Limitations and Future Work

**Sample size and significance**: With 10,000 transactions, chi-squared rejects 
H₀ for virtually all pairs, a known limitation with large samples. Cramér's V 
is used as the primary measure for this reason.

**Synthetic data**: Results should be validated with real POS transaction data 
from actual supermarket chains.

**Future extensions**:
- Apply Market Basket Analysis (Support, Confidence, Lift) to complement 
  the formal statistical testing approach used here
- Validate findings with real transaction data
- Extend temporal segmentation to seasonal patterns (holidays, school season)
- Build a recommendation engine based on identified associations

---

## How to Reproduce
```bash
git clone https://github.com/paulmosq/retail-product-association-analysis.git
cd retail-product-association-analysis
pip install -r requirements.txt
jupyter notebook notebooks/00_generate_dataset.ipynb
```

---

## Author

**Paul Mosquera Intriago** 
GitHub: [@paulmosq](https://github.com/paulmosq)

---
