import os

from pyspark.sql import SparkSession

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
    .load()
)

df.selectExpr("CAST(value AS STRING)").writeStream.format(
    "console"
).start().awaitTermination()
