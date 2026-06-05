Table fct_results {
  result_id integer [pk]
  athlete_id integer [ref: > dim_athlete.athlete_id]
  event_id integer [ref: > dim_event.event_id]
  year_of_event integer
  performance_value float
  athlete_age integer
  athlete_country string
}

Table dim_event {
  event_id integer [pk]
  event_name string
  event_type string
  year_of_event integer
  event_distance_length string
  event_unit string
}

Table dim_athlete {
  athlete_id integer [pk]
  athlete_country string
  athlete_gender string
  athlete_age integer
  athlete_year_of_birth integer
}