SELECT 'parsed_nonnull' AS check_name,count(*)=0 AS passed FROM staged
 WHERE month IS NULL OR round_no IS NULL OR premium IS NULL OR quota IS NULL
    OR bids_success IS NULL OR bids_received IS NULL
UNION ALL SELECT 'unique_keys',count(*)=0 FROM
 (SELECT month,round_no,category FROM staged GROUP BY ALL HAVING count(*)!=1)
UNION ALL SELECT 'five_categories',count(*)=0 FROM
 (SELECT month,round_no FROM retained GROUP BY ALL HAVING count(*)!=5)
UNION ALL SELECT 'positive_premiums',count(*)=0 FROM retained WHERE premium<=0 OR quota<=0
UNION ALL SELECT 'ab_pairing',count(*)=0 FROM
 (SELECT month,round_no FROM retained WHERE category IN ('Category A','Category B') GROUP BY ALL HAVING count(*)!=2);
