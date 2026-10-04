# Raw snapshot — immutable bytes, vendored for offline reproduction

Source: **LTA COE Bidding Results / Prices**, [data.gov.sg](https://data.gov.sg/datasets/d_69b3380ad7e51aff3a7dcc84eba52b8a/view), `d_69b3380ad7e51aff3a7dcc84eba52b8a`.
Data © Land Transport Authority, [Singapore Open Data Licence](https://data.gov.sg/open-data-licence), permits distribution with attribution. Independent unofficial analysis; no endorsement. Code licence does not relicense the data.

Own live pull: **2026-10-04T00:04:11+00:00**, public v1 initiate-download → poll-download → signed URL. Raw `coe-bidding-results.csv`: **78,695 bytes, 1,980 rows, 396 exercises**, 2010-01 R1–2026-09 R2. SHA-256 **361d5ae2ba641be1e834ca822e4cb66a91f42b6f7663847f42fcc4a4062b4bac**, exact FILE BYTES; manifest records lineage. `.gitattributes -text` preserves those bytes.

`python src/download.py` validates cached bytes/manifest and coverage offline. `--force` downloads and structurally validates before replacing both CSV and manifest, with ordinary-error rollback. A later pull requires prose and lock review. Never manually edit the snapshot or regenerate provenance to bless changed bytes.

Same official source as coe-quota-premium; each repository downloads independently. The seed metadata JSON stays ignored and is not fresh metadata. See [audit](../../docs/data_audit.md) for pairing, suspension and provenance limits.