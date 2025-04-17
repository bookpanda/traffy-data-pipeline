from pyspark.sql import DataFrame
from pyspark.sql.functions import col, regexp_replace, split, to_timestamp


def extract_lat_long(df: DataFrame) -> DataFrame:
    df_with_lat_long = (
        df.withColumn("longitude", split(col("coords"), ",")[0].cast("double"))
        .withColumn("latitude", split(col("coords"), ",")[1].cast("double"))
        .drop("coords")  # drop the original coords column
    )

    return df_with_lat_long.filter(
        (col("latitude").isNotNull())
        & (col("longitude").isNotNull())
        & (col("latitude") >= -90)
        & (col("latitude") <= 90)
        & (col("longitude") >= -180)
        & (col("longitude") <= 180)
    )


def convert_timestamp(df: DataFrame) -> DataFrame:
    df = df.withColumn("timestamp", to_timestamp(col("timestamp")))
    df = df.withColumn("last_activity", to_timestamp(col("last_activity")))

    return df


def convert_type_to_list(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "type", split(regexp_replace(col("type"), "[{}]", ""), ",")  # remove { and }
    )
