# Verification receipts — pre-gate

**2026-10-04 · private build only; gate/publication not performed.**

## Local actual execution

Own live download succeeded at 2026-10-04T00:04:11+00:00. Exact raw SHA-256 is in [pull_manifest.json](../data/raw/pull_manifest.json), matches file bytes; 1,980 rows / 396 complete exercises, latest 2026-09 R2.

The README four-stage pipeline completed. `env -u TMPDIR .venv/Scripts/python.exe -m unittest discover -s tests -v` returned **15 tests, OK**, followed by smoke PASS and compileall exit 0. Independent stdlib recomputation covers all 12 summary rows. Two-render test compared **four PNG and two SVG hashes**, equal in the tested Windows/Python3.12 environment. Producer-boundary regressions include invalid HTTP schema preserving prior raw+manifest, valid-but-tampered cache rejection, missing/unpaired A/B including latest, duplicates, missing whole scheduled auction, latest complete R1, future growth, transition selections, suspension reset and ordinary batch replacement rollback.

Red/green receipts during development: missing byte validator, batch publication seam, SQL metrics seam, analysis CLI and figure CLI each failed before implementation and passed afterward. Valid-but-manifest-mismatched bytes initially passed staging; new regression failed, manifest enforcement fixed it and the full suite passed. Figure pixel assertions caught title/subtitle overlap and banner footer placement; corrected and repeated. Shared styles/assets reused; no new tools installed.

Visual review covered all four light/dark figure combinations. It prompted naming the 110kW EV change, expanding first/second exercise terminology and increasing pre-window shade contrast. Numeric QA measures **64px minimum** title/subtitle/footer horizontal margins, checks all visible text inside canvas, figure-text/annotation overlaps and legend-observation clearance. No claim of SVG font equivalence across viewers or pixel equality across OSs.

Full local command log (workspace receipt, not a portable repo input):
`C:/Users/Faiz/AppData/Local/hermes/cache/scratch/coe05-receipts/local-final.log`.

## Scope and checks

Originality re-check in [audit](data_audit.md): medium adjacency; corrected earlier no-prior-work claim because press already discusses the EV rule/gap. No topic/data novelty claim. Build sheet, spec and learning pack stay outside the repo. Shared hub/design/learn00, sibling repos, publish/, planning and skills were not modified.

Settings read back: private, no Pages, wiki/projects off; Dependabot alerts HTTP204 and automated security fixes enabled/unpaused. No settings change required.

## Fresh clone, exact README commands

Branch snapshot **b3a19b69ce787c81828d1d34b25039e720dade55** was cloned into a new native-path scratch directory. The fresh README bash block supplied uv venv (`--seed`), platform-aware activation, **hash-locked pip install**, four pipeline commands, all tests and smoke—unchanged after the equivalent authorized clone line (explicit branch ref). With TMPDIR absent, exit **0**; **15 tests OK**, smoke PASS; **9/9 artifact SHA-256 values identical** (3 CSV, 4 PNG, 2 SVG), `git diff` empty and `git status` clean. Relative-link scan: **25 distinct local targets, 0 missing**. [Machine receipt and exact hashes](artifact_receipt.json).

Workspace logs and reusable verifier: `C:/Users/Faiz/AppData/Local/hermes/cache/scratch/coe05-receipts/branch-stranger-gitbash.log`, `.json`, and `verify_coe05.py`. Initial scratch harness selected Windows' WSL `bash` and could not start it; discovered the actual Git Bash executable and re-ran in a second genuinely fresh clone. This was a harness path issue, not fabricated successful output or a bypass of README setup.

The receipt's branch hash precedes this documentation-only receipt commit. PR/main CI state is verified externally and recorded in the workspace build sheet after actual runs; this file does not stand in for green CI. No CI claim before the checks execute.
