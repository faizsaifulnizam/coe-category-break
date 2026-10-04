-- Raw bytes validated before SQL. TRY parsers retain a separate SQL check seam.
CREATE TABLE staged AS
SELECT try_cast(month || '-01' AS DATE) AS month,
       try_cast(bidding_no AS INTEGER) AS round_no, vehicle_class AS category,
       try_cast(replace(quota, ',', '') AS BIGINT) AS quota,
       try_cast(replace(bids_success, ',', '') AS BIGINT) AS bids_success,
       try_cast(replace(bids_received, ',', '') AS BIGINT) AS bids_received,
       try_cast(replace(premium, ',', '') AS BIGINT) AS premium
FROM raw;
CREATE VIEW retained AS
SELECT * FROM staged WHERE NOT (month BETWEEN DATE '2020-04-01' AND DATE '2020-06-01');
