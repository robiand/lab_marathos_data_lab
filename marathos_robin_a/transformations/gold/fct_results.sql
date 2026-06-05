CREATE OR REFRESH MATERIALIZED VIEW marathos.gold.fct_results
COMMENT "Fact table for event/marathon results" AS
SELECT
    athlete_id,
    event_id,
    year_of_event,
    performance_value,
    athlete_age,
    athlete_country
FROM marathos.silver.cleaned_marathon_obt;