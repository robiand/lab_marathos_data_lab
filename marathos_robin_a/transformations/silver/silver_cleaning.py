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
    df = df.withColumn("athlete_year_of_birth", F.col("athlete_year_of_birth").cast("int"))
    df = df.withColumn("athlete_age", F.year(F.current_date()) - F.col("athlete_year_of_birth"))
    df = df.withColumn("athlete_age", F.when(F.col("athlete_age") < 0, None).otherwise(F.col("athlete_age")))
    
    return df