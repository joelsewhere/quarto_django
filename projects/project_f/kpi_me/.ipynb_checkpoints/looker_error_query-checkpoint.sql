WITH cohort_start_short_range AS (select *, dense_rank() over(order by cohort_start_date desc) = 1 next_cohort
    from inference.cohort_start_short_range)
SELECT * FROM (
SELECT *, DENSE_RANK() OVER (ORDER BY z___min_rank) as z___pivot_row_rank, RANK() OVER (PARTITION BY z__pivot_col_rank ORDER BY z___min_rank) as z__pivot_col_ordering, CASE WHEN z___min_rank = z___rank THEN 1 ELSE 0 END AS z__is_highest_ranked_cell FROM (
SELECT *, MIN(z___rank) OVER (PARTITION BY "deterministic_short_range.days_until_start") as z___min_rank FROM (
SELECT *, RANK() OVER (ORDER BY "deterministic_short_range.days_until_start" DESC, z__pivot_col_rank) AS z___rank FROM (
SELECT *, DENSE_RANK() OVER (ORDER BY "deterministic_short_range.cohort_start_date" NULLS LAST) AS z__pivot_col_rank FROM (
SELECT
    (DATE(deterministic_short_range.cohort_start_date )::varchar) AS "deterministic_short_range.cohort_start_date",
    deterministic_short_range.days_until_start  AS "deterministic_short_range.days_until_start",
    COALESCE(SUM(deterministic_short_range.matriculations ), 0) AS "deterministic_short_range.matriculations",
    COALESCE(SUM(deterministic_short_range.pw_progress_projection ), 0) AS "deterministic_short_range.pw_progress_projection",
    nullif(sum(distinct cohort_start_short_range.static_prediction), 0)  AS "cohort_start_short_range.static_prediction",
    COALESCE(SUM(deterministic_short_range.weighted_roster_projection ), 0) AS "deterministic_short_range.weighted_roster_projection",
    COALESCE(SUM(deterministic_short_range.on_roster_projection ), 0) AS "deterministic_short_range.on_roster_projection",
    COALESCE(SUM(deterministic_short_range.peak_commit_projection ), 0) AS "deterministic_short_range.peak_commit_projection"
FROM inference.deterministic_short_range  AS deterministic_short_range
LEFT JOIN cohort_start_short_range ON (DATE(cohort_start_short_range.cohort_start_date )) = (DATE(deterministic_short_range.cohort_start_date ))
      and cohort_start_short_range.days_till_start = deterministic_short_range.days_until_start
WHERE ((( deterministic_short_range.cohort_start_date  ) >= ((DATE(DATEADD(day,-89, DATE_TRUNC('day',GETDATE()) )))) AND ( deterministic_short_range.cohort_start_date  ) < ((DATE(DATEADD(day,90, DATEADD(day,-89, DATE_TRUNC('day',GETDATE()) ) )))))) AND (((( deterministic_short_range.days_until_start  ) >= 0 AND ( deterministic_short_range.days_until_start  ) <= 60)))
GROUP BY
    1,
    2) ww
) bb WHERE z__pivot_col_rank <= 16384
) aa
) xx
) zz
 WHERE (z__pivot_col_rank <= 50 OR z__is_highest_ranked_cell = 1) AND (z___pivot_row_rank <= 500 OR z__pivot_col_ordering = 1) ORDER BY z___pivot_row_rank