import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, udf
from pyspark.sql.types import StringType

from pipeline.kafka_client import deserialize_avro
from pipeline.spark.schema import schema
from pipeline.spark.transforms import (
    convert_timestamp,
    convert_type_to_list,
    extract_lat_long,
)
from pipeline.spark.write import write_to_elasticsearch, write_to_postgres


def main():
    JAR_DIR = os.path.abspath("jars")
    JARS = ",".join([os.path.join(JAR_DIR, jar) for jar in os.listdir(JAR_DIR)])

    spark = (
        SparkSession.builder.appName("KafkaConsumer")
        .config("spark.jars", JARS)
        .getOrCreate()
    )

    df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "localhost:9092")
        .option("subscribe", "raw_data")
        # .option("startingOffsets", "earliest")  # Enable to consume old messages
        .option("failOnDataLoss", "false")
        .load()
    )

    deserialize_udf = udf(deserialize_avro, StringType())
    decoded_df = df.withColumn("value", deserialize_udf("value"))
    parsed_df = decoded_df.withColumn("parsed", from_json(col("value"), schema))
    structured_df = parsed_df.select("parsed.*")

    structured_df = extract_lat_long(structured_df)
    structured_df = convert_timestamp(structured_df)
    structured_df = convert_type_to_list(structured_df)
    # data impute/one-hot-encoding will be done in ML module as it is not appropriate for stream data

    structured_df.writeStream.foreachBatch(
        lambda df, epoch_id: write_to_postgres(df, epoch_id)
    ).outputMode("append").option("checkpointLocation", "./checkpoints/pg_sink").start()

    structured_df.writeStream.foreachBatch(
        lambda df, epoch_id: write_to_elasticsearch(df, epoch_id)
    ).outputMode("append").option("checkpointLocation", "./checkpoints/es_sink").start()

    spark.streams.awaitAnyTermination()


if __name__ == "__main__":
    main()
