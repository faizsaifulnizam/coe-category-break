# Data audit — fixed live official snapshot

2026-10-04 · Source: [LTA COE Bidding Results / Prices](https://data.gov.sg/datasets/d_69b3380ad7e51aff3a7dcc84eba52b8a/view), `d_69b3380ad7e51aff3a7dcc84eba52b8a`.

## Acquisition and byte integrity

Own live API request, independent of repo 03: `python src/download.py --force`, initiate → poll → signed CSV. Retrieval **2026-10-04T00:04:11+00:00** (08:04:11 Singapore). Exact bytes **78,695**, SHA-256 **361d5ae2ba641be1e834ca822e4cb66a91f42b6f7663847f42fcc4a4062b4bac**. [Manifest](../data/raw/pull_manifest.json) matches file bytes; `-text` prevents git newline transformation. Source metadata seed JSON remains local/ignored, not asserted as a freshly downloaded dictionary.

[Singapore Open Data Licence](https://data.gov.sg/open-data-licence) permits copying/distribution/adaptation with conspicuous attribution and no official-endorsement claim; raw snapshot is small and vendored accordingly. Code MIT; data © LTA. The source remains as-is and revisionable.

## Profile and exclusions

| Check | Receipt |
|---|---|
| Schema | 7 named fields: month, bidding_no, vehicle_class, quota, bids_success, bids_received, premium |
| Rows / exercise / category | 1,980 / 396 / five A–E per exercise |
| Coverage | 2010-01 R1 through 2026-09 R2 |
| Round rows | 990 R1, 990 R2; 198 complete exercises per round |
| Blank cells / duplicate keys | 0 / 0 for month+round+category |
| Missing A/B or partial latest | 0; every exercise has both A/B and all five categories |
| Scheduled suspension | Six exercises Apr–Jun 2020 absent; 0 raw suspension rows, no zeros imputed |
| Other missing scheduled auctions | 0 after accounting for known pause |
| A/B full-source premium ranges | A 18,502–133,009; B 19,190–150,001 (S$) |

Reconciliation (exclusive reasons): **1,980 = 960 pre-2018 + 612 C/D/E in 2018+ + 408 retained A/B rows**. 408 rows pair into **204** genuine exercises, 98 pre and 106 post. No additional trimming or row deduplication. The downloader rejects malformed/missing fields rather than dropping them silently. Suspended rows, if a future source emits all-zero placeholders, are identified separately and excluded; nonzero observations in the declared suspension are rejected.

## All-round analysis distributions (S$)

| Window / side | n | A median [min, max] | B median [min, max] | Gap median [min, max] |
|---|---:|---|---|---|
| Structural pre: 2018-01–2022-04 | 98 | 36,619 [23,568, 72,996] | 40,005 [30,012, 98,889] | 6,190.50 [−1,198, 30,590] |
| Structural post: 2022-05–2026-09 R2 | 106 | 96,103 [65,010, 133,009] | 115,051.50 [85,010, 150,001] | 18,198.50 [−2,009, 50,335] |
| Tight pre: 2021-05–2022-04 | 24 | 53,209 [41,801, 72,996] | 78,650.50 [56,001, 98,889] | 21,745.50 [8,211, 30,590] |
| Tight post: 2022-05–2023-04 | 24 | 86,000 [68,001, 103,721] | 108,028.50 [92,090, 120,889] | 24,081.50 [15,355, 31,104] |

[Full summary](../outputs/gap_summary.csv) also contains both robustness variants and round counts. Gap is paired B−A per exercise; its median need not equal median B minus median A. Negative gaps are retained, not labelled erroneous. Min/max are not confidence intervals.

## Boundary and coverage decisions

Verified before analysis: [LTA circular 8 March 2022, VRL/04/2022, pp 1, 4–5](https://onemotoring.lta.gov.sg/content/dam/onemotoring/pdf/Circulars%20to%20ESAs/2022/VRL_04_2022.pdf), and [May–July quota release](https://www.lta.gov.sg/content/ltagov/en/newsroom/2022/4/news-releases/certificate-of-entitlement-quota-for-may-2022-to-july-2022.html): eligibility begins **May 2022 first exercise, 4–6 May**. Fully electric A threshold **≤110kW**, formerly 97kW; non-fully-electric A remains ≤1,600cc AND ≤97kW. Newly eligible EVs are not an invariant basket; anticipation can begin at March announcement.

Suspension source: [LTA, 18 June 2020](https://www.lta.gov.sg/content/ltagov/en/newsroom/2020/6/news-releases/resumption-of-coe-bidding-exercises-from-6-july.html). Bidding resumes from 6 July and accumulated quota returns over July 2020–June 2021: additional reason the structural pre sample spans different supply regimes.

The raw file gives month and round, not closing date; chart x positions are display conventions. Latest complete exercise can be R1; a partly populated latest exercise is rejected. Window bounds and sensitivity rules were fixed in the external build sheet before interpreting numbers. Three-exercise smoothing is intentionally `ROWS` with full/consecutive-slot guards, null at first two and after suspension. Tight windows are date-filtered and frozen through Apr-2023 even under future extension.

## Re-runnable evidence and failure limits

`python src/download.py` validates cached byte hash and schema. `python src/build_dataset.py` executes 5 SQL checks before parquet replacement. `python -m unittest discover -s tests -v` recomputes all 12 summary rows from raw CSV with stdlib medians/min/max/counts; calendar fixtures test suspension reset, transition selection, complete latest R1 and future extension. HTTP schema failure leaves old raw+manifest untouched. Valid-but-tampered cached bytes are rejected by every raw-backed production stage. Filesystem replace failure regression verifies ordinary batch rollback. Figure tests render twice and compare six hashes; pixel margins measured 64px minimum in the tested render. Figure source dates derive from UTC manifest converted to Singapore (+08), not a hardcoded local date.

Atomic replacement is per file; ordinary-error batch rollback is not power-loss safe or multiwriter safe, and running four stages does not provide pipeline-wide rollback. No timeout/OS-crash fault injection or cross-platform PNG byte equivalence is claimed. Structural checks do not settle disputed historical source cells; unrelated category anomalies are preserved in raw and do not enter A/B gap analysis.

## Originality re-check (2026-10-04): MEDIUM adjacency, keep the question

- GitHub `coe bidding` repository search: [yongjun21/coe-bidding](https://github.com/yongjun21/coe-bidding), [zawanahs/sg-coe-bidding](https://github.com/zawanahs/sg-coe-bidding), [maxyap/MachineLearningCOE_bidding](https://github.com/maxyap/MachineLearningCOE_bidding), each 0 stars at lookup. General auctions/dashboard/prediction adjacency; no exact open declared-window treatment found in this bounded search.
- GitHub code search `"May 2022" "gap" COE` returned no matches. Absence is not exhaustive proof.
- Kaggle mirrors exist: [woonel, 2011–Feb2022](https://www.kaggle.com/datasets/woonel/singapore-coe-certificate-of-entitlement-prices) and [garykx, 2002–2026](https://www.kaggle.com/datasets/garykx/singapore-coe-bidding-results-20022026-lta). Dataset is not novel.
- Closest question overlap: [Straits Times 2022 review](https://www.straitstimes.com/singapore/transport/coe-premiums-at-all-time-highs-in-2022-buyers-could-get-slight-reprieve-in-later-half-of-2023) connects EV reclassification and A/B gap commentary, comparing first/last 2022 percentage gaps. Therefore the earlier spec's “no prior work” guard was too strong and was corrected. This repo adds fixed structural/tight **S$ paired-gap distributions**, explicit robustness, reproducible licensed snapshot, independent checks and refusal of causal identification—not novelty of the subject or data. Commercial archives such as COEwatch are adjacent context, not a claimed discovery.

## What this file cannot say

Not a causal policy estimate, zero-effect test, EV-adoption/welfare analysis, source-cell certification or forecast. No microdata/assignment/control market; composition, quota cycles, demand, macro conditions and anticipation remain confounded.
