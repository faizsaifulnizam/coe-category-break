-- Equal weight per paired exercise. Date label is month-start, NOT actual auction date.
CREATE TABLE exercise AS
WITH paired AS (
 SELECT month, round_no,
        max(premium) FILTER (WHERE category='Category A') AS premium_a,
        max(premium) FILTER (WHERE category='Category B') AS premium_b,
        year(month)*24+(month(month)-1)*2+round_no AS slot
 FROM retained WHERE month >= DATE '2018-01-01' AND category IN ('Category A','Category B')
 GROUP BY month,round_no
), gaps AS (
 SELECT *,premium_b-premium_a AS gap,
        CASE WHEN month < DATE '2022-05-01' THEN 'pre' ELSE 'post' END AS period,
        slot BETWEEN 2022*24+8-1 AND 2022*24+8+2 AS transition
 FROM paired
)
SELECT *,CASE WHEN count(*) OVER w=3 AND slot-min(slot) OVER w=2
              THEN median(gap) OVER w END AS rolling_gap
FROM gaps
WINDOW w AS (ORDER BY month,round_no ROWS BETWEEN 2 PRECEDING AND CURRENT ROW);

CREATE TABLE gap_summary AS
WITH selected AS (
 SELECT e.*,v.variant,w."window"
 FROM exercise e
 CROSS JOIN (VALUES ('all'),('round1'),('exclude_transition')) v(variant)
 CROSS JOIN (VALUES ('structural'),('tight')) w("window")
 WHERE (v.variant!='round1' OR round_no=1)
   AND (v.variant!='exclude_transition' OR NOT transition)
   AND (w."window"='structural' OR month BETWEEN DATE '2021-05-01' AND DATE '2023-04-01')
)
SELECT "window",variant,period,min(month) AS start_month,max(month) AS end_month,
       min(round_no) FILTER (WHERE month=(SELECT min(month) FROM selected s2 WHERE s2."window"=selected."window" AND s2.variant=selected.variant AND s2.period=selected.period)) AS start_round,
       max(round_no) FILTER (WHERE month=(SELECT max(month) FROM selected s2 WHERE s2."window"=selected."window" AND s2.variant=selected.variant AND s2.period=selected.period)) AS end_round,
       count(*) AS n_exercises,count(*) FILTER (WHERE round_no=1) AS n_round1,
       count(*) FILTER (WHERE round_no=2) AS n_round2,
       median(premium_a) AS median_a,min(premium_a) AS min_a,max(premium_a) AS max_a,
       median(premium_b) AS median_b,min(premium_b) AS min_b,max(premium_b) AS max_b,
       median(gap) AS median_gap,min(gap) AS min_gap,max(gap) AS max_gap
FROM selected GROUP BY "window",variant,period ORDER BY "window",variant,period;
CREATE TABLE sensitivity AS
SELECT p."window",p.variant,b.n_exercises AS n_pre,p.n_exercises AS n_post,
       b.median_gap AS pre_median_gap,p.median_gap AS post_median_gap,
       p.median_gap-b.median_gap AS change_median_gap,
       p.median_a-b.median_a AS change_median_a,
       p.median_b-b.median_b AS change_median_b
FROM gap_summary p JOIN gap_summary b USING("window",variant)
WHERE p.period='post' AND b.period='pre' ORDER BY "window",variant;
