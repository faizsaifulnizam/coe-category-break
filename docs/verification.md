# Public verification — 2026-10-04

The public baseline at [`4d969f2`](https://github.com/faizsaifulnizam/coe-category-break/commit/4d969f2b326cdbd9bbeea5402b9d44c003a15779) passed the README block on Python 3.12: hash-locked pip install, download/build/analysis/figures, **17 tests OK**, smoke PASS and byte-identical `outputs/*.csv`. [CI on that SHA passed](https://github.com/faizsaifulnizam/coe-category-break/actions/runs/37187059883).

The Grok-review corrections retain the same raw snapshot and all three numerical CSVs. Local Python 3.12 verification returned **19 tests OK**, smoke PASS and an empty CSV diff. New regressions check the actual rendered gap title/dark window alpha and recompute the annual medians, quota sums and tight-window opposite-sign distinction from raw-backed data. The existing transition test still selects Apr/May 2022 R1/R2. Run the [README commands](../README.md#reproduce) to repeat these checks; [current CI](https://github.com/faizsaifulnizam/coe-category-break/actions/workflows/ci.yml) is a separate public record, not inferred from local tests.

Refresh-boundary verification on Python 3.12 returned **23 tests OK**, smoke PASS and an empty numerical-CSV/raw-snapshot diff. New [refresh tests](../tests/test_refresh.py) execute the real download entry point with only HTTP/CLI/path boundaries substituted: malformed quoting and overflow in all four numeric columns preserve prior raw/manifest bytes; valid imported refresh publishes the exact source bytes and matching manifest. A real DuckDB check rejects NULL bid fields. Full producer runs retain the same raw snapshot and all numerical CSVs. Existing ordinary-error rollback and same-environment render-hash tests still pass.

The [artifact receipt](artifact_receipt.json) contains current nine-artifact SHA-256 values. Same-environment figure renders repeat byte-for-byte. PNG bytes can differ across machines: compare decoded pixels before calling a change compression/metadata-only. An empty CSV diff does not prove image equivalence.

Private-machine paths and pre-publication commit identifiers are not used as public verification evidence.
