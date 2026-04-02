# Business Insights Report
## Retail Product Association Analysis — Ecuador Supermarket Context

**Dataset**: 10,000 synthetic transactions based on Ecuadorian supermarket 
purchasing patterns (Supermaxi / Mi Comisariato context)  
**Period**: January 2024 – December 2024  
**Analysis**: Chi-squared test, Cramér's V, Odds Ratio — segmented by time slot

---

## Methodological Note

All 15 category pairs tested were statistically significant (p < 0.05). 
With a sample of 10,000 transactions, the chi-squared test has very high 
statistical power and will reject H₀ for virtually any non-zero association, 
this is a known limitation of the test with large samples.

For this reason, p-values are not used as the primary decision criterion. 
Instead, Cramér's V is the main measure for comparing association strength, 
and temporal variation in Cramér's V across time slots is the core analytical 
focus of this project.

---

## Key Finding 1 — Dairy + Snacks peak in the Afternoon

**Statistical result**:  
Dairy products and eggs + Snacks and drinks show their strongest association 
during Afternoon (Cramér's V = 0.1357), significantly weaker in Evening 
(V = 0.0759) and Morning (V = 0.1117).

**Interpretation**:  
Afternoon shoppers appear to combine routine grocery runs with impulse snack 
purchases. This is consistent with post-lunch or after-school shopping behavior 
common in Ecuadorian households a time when both dairy staples and snack 
products are purchased together as part of a broader basket.

**Business recommendations**:
- Schedule cross-promotions between dairy and snack products specifically 
  during afternoon hours (12:00–18:00)
- Example: combo discount valid only between 12:00–17:00
- Ensure snack shelves are fully stocked before the afternoon rush
- Consider placing dairy and snack sections within visual proximity

---

## Key Finding 2 — Fruits & Vegetables + Meats peak in the Evening

**Statistical result**:  
Fruits and vegetables + Meats and sausages association is strongest in 
Evening (Cramér's V = 0.1512) compared to Morning (V = 0.1216) and 
Afternoon (V = 0.0987).

**Interpretation**:  
This pattern reflects a fundamentally different purchase intent from other 
time slots. Evening shoppers are not doing routine household runs they are 
purchasing ingredients for dinner preparation. The co-purchase of fresh produce 
and meat in the evening is driven by meal planning behavior, not general 
restocking. This distinction has direct implications for how promotions should 
be designed and timed.

**Business recommendations**:
- Place produce and meat sections in adjacent aisles to reduce friction 
  for dinner-planning shoppers
- Run evening promotions (18:00–21:00) combining fresh produce with 
  meat products
- Consider "dinner bundle" promotions exclusively valid during evening hours
- Prioritize restocking both categories before 17:00 to capture peak demand

---

## Key Finding 3 — Home Cleaning + Snacks vary by time slot

**Statistical result**:  
Home cleaning + Snacks and drinks association is stronger in Morning 
(Cramér's V = 0.1271) than Afternoon (V = 0.0831) and Evening (V = 0.1064).

**Interpretation**:  
Morning shoppers tend to do full household runs combining cleaning products 
with snack purchases suggests a single comprehensive shopping trip rather than 
a targeted visit. This is consistent with the behavior of the primary household 
shopper who organizes weekly purchases in the morning.

**Business recommendations**:
- Bundle cleaning products with snack promotions specifically in morning hours
- Consider loyalty points for morning purchases combining both categories
- Morning is the best window for cross-category promotions targeting the 
  primary household shopper

---

## Summary — Priority Pairs for Commercial Action

| Pair | Best Time Slot | Cramér's V | Recommended Action |
|---|---|---|---|
| Fruits & Veg + Meats | Evening | 0.1512 | Dinner bundle promotion 18–21h |
| Dairy + Snacks | Afternoon | 0.1357 | Combo discount 12–17h |
| Home Cleaning + Snacks | Morning | 0.1271 | Morning loyalty bundle |
| Dairy + Home Cleaning | Afternoon | 0.1236 | Adjacent aisle placement |
| Dairy + Fruits & Veg | Afternoon | 0.1236 | Fresh products cross-promotion |

---

## General Conclusion

The temporal segmentation approach reveals that association strength between 
product categories is not static it shifts meaningfully across time slots, 
reflecting distinct shopping behaviors at different hours of the day.

A global analysis without temporal segmentation would have identified the same 
15 significant pairs but would have missed the behavioral interpretation behind 
each pattern. The actionable insight is not just that these pairs are associated, 
but when and why which is what makes the difference between a 
descriptive report and a decision-support tool.