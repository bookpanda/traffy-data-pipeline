from pyspark.sql import DataFrame

from pipeline.config import settings


def write_to_postgres(batch_df: DataFrame, batch_id):
    (
        batch_df.write.format("jdbc")
        .option("url", settings.POSTGRES_URL)
        .option("dbtable", settings.POSTGRES_TABLE)
        .option("user", settings.POSTGRES_USER)
        .option("password", settings.POSTGRES_PASSWORD)
        .option("driver", "org.postgresql.Driver")
        .mode("append")
        .save()
    )
