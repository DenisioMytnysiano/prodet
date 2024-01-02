import json
from datetime import datetime
import uuid
import pyspark.sql.functions as F
from pyspark.sql import Row
from pyspark.sql.streaming.readwriter import DataStreamReader
from pyspark.sql.types import StringType

from .config import Config
from .spark import (
    build_kafka_read_stream, build_spark_context, 
    parse_kafka_stream_by_schema, write_stream_to_kafka
)
from .schema import translated_message_schema


spark = build_spark_context(Config.SPARK_HOST, Config.SPARK_PORT)


def init_propaganda_normalizer() -> None:
    kafka_url = f"{Config.KAFKA_HOST}:{Config.KAFKA_PORT}"
    input_stream = build_stream(kafka_url)
    prepared_stream = prepare_stream(input_stream)
    write_stream_to_kafka(prepared_stream, kafka_url, Config.KAFKA_PREPARED_TOPIC, "normalizer")

def build_stream(kafka_url: str) -> DataStreamReader:
    raw_stream =  build_kafka_read_stream(spark, kafka_url, Config.KAFKA_TRANSLATED_TOPIC)
    return parse_kafka_stream_by_schema(raw_stream, translated_message_schema)

def prepare_stream(stream: DataStreamReader) -> DataStreamReader:
    return (stream
        .withColumn("value", prepare_message(F.col("value")))
    )

@F.udf(returnType=StringType())
def prepare_message(message_row: Row) -> str:
    message_dict = message_row.asDict()
    message_dict["message_id"] = message_dict["id"]
    message_dict["id"] = str(uuid.uuid4())
    message_dict["prepared_at"] = datetime.now().isoformat()
    return json.dumps(message_dict)
