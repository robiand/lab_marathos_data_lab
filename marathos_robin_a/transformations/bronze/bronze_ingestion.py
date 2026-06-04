from pyspark import pipelines as dp

#Get data and volume
VOLUME_PATH = "/Volumes/marathos/default/raw"

@dp.table(
    name="marathos.bronze.raw_marathon_results",
    comment="Raw data from the marathons dataset",
)
def raw_marathon_results():
    df = (spark.read.options(header=True, inferSchema=True).csv(f"{VOLUME_PATH}/data/TWO_CENTURIES_OF_UM_RACES.csv"))
    for c in df.columns:
        print(c)
        #clean column names to be compatible with spark
        cleaned_c = (
            c.lower()
            .replace("/", "_")
            .replace(" ", "_")
            .replace("-", "_")
            .replace("(", "")
            .replace(")", "")
        )
        df = df.withColumnRenamed(c, cleaned_c)

    return df