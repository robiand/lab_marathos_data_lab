CREATE OR REFRESH MATERIALIZED VIEW marathos.gold.dim_athlete
COMMENT "Dim table for athletes" AS
SELECT DISTINCT
    athlete_id,
    athlete_country,
    athlete_gender,
    athlete_age,
    athlete_year_of_birth
FROM marathos.silver.cleaned_marathon_obt;