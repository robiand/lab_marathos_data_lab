#Get data and volume as usual
VOLUME_PATH = "/Volumes/marathos/default/raw"

df = (
    spark.read.options(header=True, inferSchema=True)
    .csv(f"{VOLUME_PATH}/data/TWO_CENTURIES_OF_UM_RACES.csv")
)

# test print to show that df works in this script
#display(df.take(6))

# before cleaning, column names can be checked here
#print(df.columns)

#df columns now need to be cleaned as they can not be written to table
for c in df.columns:
    print(c)
    cleaned_c = (
        c.lower()
        .replace("/", "_")
        .replace(" ", "_")
        .replace("-", "_")
        .replace("(", "")
        .replace(")", "")
    )
    df = df.withColumnRenamed(c, cleaned_c)

# this print can be used to compare column names before and after cleaning
print(df.columns)

# Write to bronze layer
df.write.format("delta").mode("overwrite").saveAsTable("marathos.bronze.raw_marathon_results")

# now we can try displaying the data written to marathos.bronze!
display(spark.table("marathos.bronze.raw_marathon_results").take(6))