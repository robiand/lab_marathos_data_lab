from pyspark import pipelines as dp
from pyspark.sql.functions import dense_rank
from pyspark.sql.window import Window
from pyspark.sql import functions as F

@dp.table(
    name="marathos.silver.cleaned_marathon_obt",
    comment="Cleaned OBT marathon results"
)
def cleaned_marathon_obt():
    # load the data written in the bronze layer
    df = spark.sql("SELECT * FROM marathos.bronze.raw_marathon_results")

    #start cleaning the data
    df = df.filter(~F.col("event_distance_length").contains("d"))
    df = df.filter(F.col("athlete_year_of_birth").isNotNull())
    df = df.filter(F.col("event_name").isNotNull())
    df = df.filter(F.col("athlete_performance").isNotNull())
    df = df.filter(F.col("athlete_country").isNotNull())
    df = df.withColumn("athlete_year_of_birth", F.col("athlete_year_of_birth").cast("int"))
    df = df.withColumn("athlete_age", F.year(F.current_date()) - F.col("athlete_year_of_birth"))
    df = df.withColumn("athlete_age", F.when(
            (F.col("year_of_event") - F.col("athlete_year_of_birth") < 5) |
            (F.col("year_of_event") - F.col("athlete_year_of_birth") > 100), None).otherwise(
            F.col("year_of_event") - F.col("athlete_year_of_birth")
    )
)
    #create event ids
    W = Window.orderBy("event_name")
    df = df.withColumn("event_id",
        F.dense_rank().over(W)
    )

    #add time or distance event type to events so athlete performance can be compared
    df = df.withColumn("event_type",
        F.when(F.col("event_distance_length").contains("km"), "distance")
        .when(F.col("event_distance_length").contains("mi"), "distance")
        .when(F.col("event_distance_length").contains("h"), "time")    
    )

    #assign unit to event (km, mi, h)
    df = df.withColumn(
        "event_unit",
        F.regexp_extract("event_distance_length", "(km|mi|h)", 1)
    )

    #match event distance and hours with athlete performance
    df = df.withColumn(
        "performance_value",
        F.when(
            F.col("event_type") == "distance",
            F.regexp_extract("athlete_performance", r"([0-9.]+)", 1)
        ).otherwise(
            F.regexp_extract("athlete_performance", r"([0-9:]+)", 1)
        )
    )

    return df