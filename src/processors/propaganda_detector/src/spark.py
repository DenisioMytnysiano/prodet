from pyspark.sql import SparkSession
from pyspark.sql.streaming.readwriter import DataStreamReader, DataStreamWriter


def build_spark_context(host: str, port: str) -> SparkSession:
    return (SparkSession.builder.remote(f"sc://{host}:{port}")
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5")
        .config("spark.executorEnv.PYSPARK_PYTHON", "/opt/bitnami/python/bin/python3")
        .getOrCreate()
    )

def build_kafka_read_stream(spark: SparkSession, kafka_url: str, topic: str) -> DataStreamReader:
    return (spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", kafka_url)
        .option("subscribe", topic)
        .load()
    )
