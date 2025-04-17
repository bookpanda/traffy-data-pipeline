from pyspark.sql.types import (
    FloatType,
    IntegerType,
    StringType,
    StructType,
    TimestampType,
)

schema = (
    StructType()
    .add("ticket_id", StringType())
    .add("type", StringType())
    .add("organization", StringType())
    .add("comment", StringType())
    .add("photo", StringType())
    .add("photo_after", StringType())
    .add("coords", StringType())
    .add("address", StringType())
    .add("subdistrict", StringType())
    .add("district", StringType())
    .add("province", StringType())
    .add("timestamp", StringType())
    .add("state", StringType())
    .add("star", FloatType())
    .add("count_reopen", IntegerType())
    .add("last_activity", StringType())
)
