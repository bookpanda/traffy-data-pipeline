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


def write_to_elasticsearch(batch_df: DataFrame, epoch_id):
    try:
        (
            batch_df.write.format("org.elasticsearch.spark.sql")
            .option("es.resource", "tickets/_doc")
            .option("es.nodes", "localhost")
            .option("es.port", "9200")
            .option("es.net.http.auth.user", "elastic")
            .option("es.net.http.auth.pass", "elasticpassword")
            .option("es.nodes.wan.only", "true")
            .mode("append")
            .save()
        )
    except Exception as e:
        print(f"[ERROR] Failed to write to Elasticsearch: {e}")
        raise
