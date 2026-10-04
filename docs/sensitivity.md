# Sensitivity — sign survives; magnitude depends on calendar window

All amounts are **S$**, equal exercise weights. Values are differences of median paired B−A gaps, **not policy effects**. Source: [sensitivity.csv](../outputs/sensitivity.csv); each underlying distribution's levels/min/max/counts remain in [gap_summary.csv](../outputs/gap_summary.csv).

| Window | Variant | n pre / post | Median gap pre | Median gap post | Change |
|---|---|---:|---:|---:|---:|
| Structural | All rounds | 98 / 106 | 6,190.50 | 18,198.50 | +12,008 |
| Structural | R1 only | 49 / 53 | 6,000 | 18,398 | +12,398 |
| Structural | Exclude transition | 96 / 104 | 6,050.50 | 17,943 | +11,892.50 |
| Tight | All rounds | 24 / 24 | 21,745.50 | 24,081.50 | +2,336 |
| Tight | R1 only | 12 / 12 | 21,650 | 24,442.50 | +2,792.50 |
| Tight | Exclude transition | 22 / 22 | 21,249 | 24,081.50 | +2,832.50 |

Structural = 2018-01–2022-04 vs 2022-05–2026-09 R2. Tight = fixed 2021-05–2022-04 vs 2022-05–2023-04. Ex-transition drops **two pre (Apr-2022 R1/R2), two post (May-2022 R1/R2)**; not two per side after restricting rounds. R1 and ex-transition are separate variants, not a combined variant.

## How to read it

Every specified variant has a positive median-gap difference, but the long pre period includes much smaller early gaps. The tight pre median is already 21,745.50. Round choice and transition exclusion do not erase the sign; they do not remove quota cycles, basket changes, anticipation or interference. No selected-window significance test, confidence interval or causal claim is implied. Gap min/max overlap in both windows; observed overlap does not prove no effect. No additional windows were searched for a preferred story.
