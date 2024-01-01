from pyspark.sql import SparkSession
from pyspark.sql.streaming.readwriter import DataStreamReader


def build_spark_context(host: str, port: str) -> SparkSession:
    return (SparkSession.builder
        .appName("PropagandaDetector")
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
