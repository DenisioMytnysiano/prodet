import json
from datetime import datetime
import pyspark.sql.functions as F
from pyspark.sql.streaming.readwriter import DataStreamReader
from pyspark.sql.types import StringType, FloatType
from pyspark.sql import Row

from .config import Config
from .spark import (
    build_kafka_read_stream, build_spark_context, 
    parse_kafka_stream_by_schema, write_stream_to_kafka
)
from .schema import prepared_message_schema


spark = build_spark_context(Config.SPARK_HOST, Config.SPARK_PORT)


def init_propaganda_detector() -> None:
    kafka_url = f"{Config.KAFKA_HOST}:{Config.KAFKA_PORT}"
    input_stream = build_stream(kafka_url)
    processed_stream = process_stream(input_stream)
    write_stream_to_kafka(processed_stream, kafka_url, Config.KAFKA_PROCESSED_TOPIC, "detector")

def build_stream(kafka_url: str) -> None:
    raw_stream = build_kafka_read_stream(spark, kafka_url, Config.KAFKA_PREPARED_TOPIC)
    return parse_kafka_stream_by_schema(raw_stream, prepared_message_schema)

def process_stream(stream: DataStreamReader) -> None:
    return (stream
        .withColumn("value", process_message(F.col("value")))
    )

@F.udf(returnType=StringType())
def process_message(message_row: Row) -> str:
    message = message_row.asDict()
    message["propaganda"] = len(message["text"]) / 50
    message["processed_at"] = datetime.now().isoformat()
    return json.dumps(message)

@F.udf(returnType=FloatType())
def predict_propaganda(text: str) -> float:
    return len(text) / 100
