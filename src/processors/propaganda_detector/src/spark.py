import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.streaming.readwriter import DataStreamReader
from pyspark.sql.types import StructType


def build_spark_context(host: str, port: str) -> SparkSession:
    return (SparkSession.builder
        .appName("Prodet")
        .remote(f"sc://{host}:{port}")
        .config("spark.executorEnv.PYSPARK_PYTHON", "/opt/bitnami/python/bin/python3")
        .getOrCreate()
    )

def build_kafka_read_stream(spark: SparkSession, kafka_url: str, topic: str) -> DataStreamReader:
    return (spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", kafka_url)
        .option("subscribe", topic)
        .option("startingOffsets", "earliest")
        .load()
    )

def parse_kafka_stream_by_schema(stream: DataStreamReader, schema: StructType) -> DataStreamReader:
    return (stream
        .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
        .select(F.from_json(F.col("value"), schema).alias("value"), "key")
    )

def write_stream_to_kafka(stream: DataStreamReader, kafka_url: str, topic: str, checkpoint_idx: str) -> None:
    (stream
        .writeStream
        .outputMode("update")
        .format("kafka")
        .option("kafka.bootstrap.servers", kafka_url)
        .option("checkpointLocation", f"/tmp/checkpoint/kafka-{checkpoint_idx}")
        .option("topic", topic)
        .start()
        .awaitTermination()
    )
