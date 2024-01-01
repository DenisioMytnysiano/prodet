import json
from datetime import datetime
import pyspark.sql.functions as F
from pyspark.sql import Row
from pyspark.sql.streaming.readwriter import DataStreamReader
from pyspark.sql.types import StringType

from .config import Config
from .spark import build_kafka_read_stream, build_spark_context, parse_kafka_stream_by_schema
from .schema import raw_message_schema


spark = build_spark_context(Config.SPARK_HOST, Config.SPARK_PORT)


def init_propaganda_normalizer() -> None:    
    kafka_url = f"{Config.KAFKA_HOST}:{Config.KAFKA_PORT}"
    input_stream = build_stream(kafka_url)
    prepared_stream = prepare_stream(input_stream)
    write_stream_to_topic(prepared_stream, kafka_url, Config.KAFKA_PREPARED_TOPIC)

def build_stream(kafka_url: str) -> DataStreamReader:
    raw_stream =  build_kafka_read_stream(spark, kafka_url, Config.KAFKA_RAW_TOPIC)
    return parse_kafka_stream_by_schema(raw_stream, raw_message_schema)

def prepare_stream(stream: DataStreamReader) -> DataStreamReader:
    return (stream
        .withColumn("value", prepare_message(F.col("value")))
    )

@F.udf(returnType=StringType())
def prepare_message(message_row: Row) -> str:
    message_dict = message_row.asDict()
    message_dict["prepared_at"] = datetime.now().isoformat()
    # TODO: implement translation
    return json.dumps(message_dict)

def write_stream_to_topic(input_stream: DataStreamReader, kafka_url: str, topic: str) -> None:
    (input_stream
        .writeStream
        .outputMode("update")
        .format("kafka")
        .option("kafka.bootstrap.servers", kafka_url)
        .option("checkpointLocation", "/tmp/checkpoint/kafka")
        .option("topic", topic)
        .start()
        .awaitTermination()
    )
