import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.streaming.readwriter import DataStreamReader

from .config import Config
from .spark import build_kafka_read_stream
from .schema import raw_message_schema


def init_propaganda_normalizer(spark: SparkSession) -> None:    
    kafka_url = f"{Config.KAFKA_HOST}:{Config.KAFKA_PORT}"
    input_stream = build_input_stream(spark, kafka_url)
    
    processed_stream = apply_stream_transformation(input_stream)
    write_stream_to_topic(processed_stream, kafka_url, Config.KAFKA_PREPARED_TOPIC)

def build_input_stream(spark: SparkSession, kafka_url: str) -> DataStreamReader:
    base_stream = build_kafka_read_stream(spark, kafka_url, Config.KAFKA_RAW_TOPIC)
    return (base_stream
        .selectExpr("CAST(value AS STRING)")
        .select(F.from_json(F.col("value"), raw_message_schema).alias("data"))
        .select("data.*")
    )

def apply_stream_transformation(input_stream: DataStreamReader) -> DataStreamReader:
    # TODO: implement translation
    return input_stream

def write_stream_to_topic(input_stream: DataStreamReader, kafka_url: str, topic: str) -> None:
    (input_stream
        .writeStream
        .format("console")
        .outputMode("update")
        .start()
        .awaitTermination()
    )
    # (input_stream
    #     .writeStream
    #     .outputMode("update")
    #     .format("kafka")
    #     .option("kafka.bootstrap.servers", kafka_url)
    #     .option("checkpointLocation", "/tmp/checkpoint")
    #     .option("topic", topic)
    #     .start()
    #     .awaitTermination()
