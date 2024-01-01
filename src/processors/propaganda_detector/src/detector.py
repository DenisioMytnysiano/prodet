import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.streaming.readwriter import DataStreamReader

from .config import Config
from .spark import build_kafka_read_stream, build_spark_context

spark = build_spark_context(Config.SPARK_HOST, Config.SPARK_PORT)

def init_propaganda_detector() -> None:
    kafka_url = f"{Config.KAFKA_HOST}:{Config.KAFKA_PORT}"
    input_stream = build_input_stream(spark, kafka_url)
    process_input_stream(input_stream)

def build_input_stream(spark: SparkSession, kafka_url: str) -> None:
    base_stream = build_kafka_read_stream(spark, kafka_url, Config.KAFKA_PREPARED_TOPIC)
    return base_stream

def process_input_stream(input_stream: DataStreamReader) -> None:
    (input_stream
        .writeStream
        .outputMode("append")
        .format("console")
        .start()
        .awaitTermination()
    )

@F.udf()
def predict_propaganda() -> bool:
    return False
