# Verification receipts — publication layer and private-review provenance

**2026-10-04 · reviewed; publication approved.** Site/card preparation and checks below are local. Merge, public visibility, Pages deployment and manual social-preview upload are separate operations; this receipt does not claim they have happened.

## Clean-history context

This repository starts at clean noreply root **27b6a6711b4a8e4c5cc54d8b37e44a8237148cb1**. Its initial tree preserves the reviewed private-build artifacts. Prior implementation, independent reviews and PR/CI history are archived privately outside this clean repository's history, not presented as current public PRs or CI runs. Both author and committer of the clean root use the GitHub noreply identity.

The [artifact receipt](artifact_receipt.json) is explicitly a **historical private pre-publication receipt**. Its `head`, `ref`, workspace paths and 15-test result describe that earlier private clone, not execution from the clean root or this publication branch. They are retained as provenance; those commit identifiers are not promised to resolve in public history. Workspace paths in the historical sections below are non-portable evidence locations, not repository inputs.

## Local publication-layer checks (2026-10-04)

- The vendored download validation and staging ran successfully: **1,980 rows, 396 complete exercises; 204 paired analysis exercises; SQL 5/5**. No live repull or numerical-method change.
- `python -m unittest discover -s tests -v` using the already-installed Windows Python 3.12 environment returned **17 tests, OK**; smoke PASS. Added checks cover site metadata, both CSV-backed comparison anchors/counts, six series links, local assets/font targets and 1280×640 card dimensions. Figure tests confirm six site copies match their sources and inject a failure at the **last Pages replacement in the actual 12-file figure/banner batch**, restoring every prior byte and cleaning staged files.
- Four figures and two banners regenerated twice with equal same-environment hashes. `git diff --exit-code` for raw/manifest, numerical CSVs, original figure PNGs and banner SVGs returned **0** against the clean root; their reviewed bytes are unchanged. Six Pages copies use the existing validated publication seam, not a separate analysis path.
- Edge headless/CDP exercised **10 local browser cases**: site and GitHub-API-rendered README at 1280px and 390px in light/dark, plus both 1280×640 card themes. All three picture images loaded and selected the expected theme; no page-level horizontal overflow. Inter and Source Serif 4 loaded. Card text boxes were in bounds with no overlap; repeated captures were byte-identical in this run.
- `gh api markdown` supplied GitHub's current sanitized README HTML: three standalone pictures survived with one source and one image each. Browser media QA served that HTML with local assets and minimal preview CSS; external badges were excluded. This is **not a logged-in github.com DOM or deployed Pages receipt**.
- Markdown/local-media scan: **27 distinct local targets, zero missing**. Static site checks validate asset/font confinement under `docs/`, canonical URL, absolute Pages Open Graph image, dimensions and Twitter large-image metadata. The canonical Pages target is intentionally not treated as a live deployment check.
- Visual inspection covered the light card and mobile dark site, then both final card themes. A suspected dark-card contrast issue was checked numerically: body/footer **7.175:1** (normal-text threshold 4.5:1); 22px semibold disclaimer **4.347:1** (large-text threshold 3:1). No clipping or overlap remained. Windows/Edge rendering is the measured scope, not cross-browser pixel equivalence.

Workspace QA logs/screenshots: `C:/Users/Faiz/AppData/Local/hermes/cache/scratch/coe05-publication-qa/` (`tests.log`, `readme-api.html`, `browser-receipt.json`, theme screenshots); reusable local browser check: sibling `coe05-publication-qa.py`. This publication layer adds no installed dependency and changes no external settings. Final fresh-clone setup and deployed-site checks belong to the publication coordinator.

## Prior private build — actual execution (historical)

Own live download succeeded at 2026-10-04T00:04:11+00:00. Exact raw SHA-256 is in [pull_manifest.json](../data/raw/pull_manifest.json), matches file bytes; 1,980 rows / 396 complete exercises, latest 2026-09 R2.

The README four-stage pipeline completed. `env -u TMPDIR .venv/Scripts/python.exe -m unittest discover -s tests -v` returned **15 tests, OK**, followed by smoke PASS and compileall exit 0. Independent stdlib recomputation covers all 12 summary rows. Two-render test compared **four PNG and two SVG hashes**, equal in the tested Windows/Python3.12 environment. Producer-boundary regressions include invalid HTTP schema preserving prior raw+manifest, valid-but-tampered cache rejection, missing/unpaired A/B including latest, duplicates, missing whole scheduled auction, latest complete R1, future growth, transition selections, suspension reset and ordinary batch replacement rollback.

Red/green receipts during development: missing byte validator, batch publication seam, SQL metrics seam, analysis CLI and figure CLI each failed before implementation and passed afterward. Valid-but-manifest-mismatched bytes initially passed staging; new regression failed, manifest enforcement fixed it and the full suite passed. Figure pixel assertions caught title/subtitle overlap and banner footer placement; corrected and repeated. Shared styles/assets reused; no new tools installed.

Visual review covered all four light/dark figure combinations. It prompted naming the 110kW EV change, expanding first/second exercise terminology and increasing pre-window shade contrast. Numeric QA measures **64px minimum** title/subtitle/footer horizontal margins, checks all visible text inside canvas, figure-text/annotation overlaps and legend-observation clearance. No claim of SVG font equivalence across viewers or pixel equality across OSs.

Full local command log (workspace receipt, not a portable repo input):
`C:/Users/Faiz/AppData/Local/hermes/cache/scratch/coe05-receipts/local-final.log`.

## Prior private build — scope and checks (historical)

Originality re-check in [audit](data_audit.md): medium adjacency; corrected earlier no-prior-work claim because press already discusses the EV rule/gap. No topic/data novelty claim. Build sheet, spec and learning pack stay outside the repo. Shared hub/design/learn00, sibling repos, publish/, planning and skills were not modified.

Settings read back: private, no Pages, wiki/projects off; Dependabot alerts HTTP204 and automated security fixes enabled/unpaused. No settings change required.

## Prior private build — fresh clone, exact README commands (historical)

Branch snapshot **b3a19b69ce787c81828d1d34b25039e720dade55** was cloned into a new native-path scratch directory. The fresh README bash block supplied uv venv (`--seed`), platform-aware activation, **hash-locked pip install**, four pipeline commands, all tests and smoke—unchanged after the equivalent authorized clone line (explicit branch ref). With TMPDIR absent, exit **0**; **15 tests OK**, smoke PASS; **9/9 artifact SHA-256 values identical** (3 CSV, 4 PNG, 2 SVG), `git diff` empty and `git status` clean. Relative-link scan: **25 distinct local targets, 0 missing**. [Machine receipt and exact hashes](artifact_receipt.json).

Workspace logs and reusable verifier: `C:/Users/Faiz/AppData/Local/hermes/cache/scratch/coe05-receipts/branch-stranger-gitbash.log`, `.json`, and `verify_coe05.py`. Initial scratch harness selected Windows' WSL `bash` and could not start it; discovered the actual Git Bash executable and re-ran in a second genuinely fresh clone. This was a harness path issue, not fabricated successful output or a bypass of README setup.

The historical receipt's branch hash preceded its private documentation-only receipt commit. Historical PR/main CI state was recorded outside the public history after actual runs. Current branch CI must be read from its own PR checks; neither historical evidence nor local tests stand in for green CI or a new fresh-clone setup receipt.
