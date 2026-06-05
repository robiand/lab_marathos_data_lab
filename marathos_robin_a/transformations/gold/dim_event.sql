CREATE OR REFRESH MATERIALIZED VIEW marathos.gold.dim_event
COMMENT "Dim table for events" AS
SELECT DISTINCT
    event_id,
    event_name,
    event_type,
    event_unit,
    year_of_event,
    event_distance_length
FROM marathos.silver.cleaned_marathon_obt;