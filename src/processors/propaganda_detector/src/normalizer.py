import json
from datetime import datetime
import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.streaming.readwriter import DataStreamReader
from pyspark.sql.types import StringType

from .config import Config
from .spark import build_kafka_read_stream, build_spark_context
from .schema import raw_message_schema


spark = build_spark_context(Config.SPARK_HOST, Config.SPARK_PORT)

def init_propaganda_normalizer() -> None:    
    kafka_url = f"{Config.KAFKA_HOST}:{Config.KAFKA_PORT}"
    input_stream = build_input_stream(spark, kafka_url)
    
    processed_stream = apply_stream_transformation(input_stream)
    write_stream_to_topic(processed_stream, kafka_url, Config.KAFKA_PREPARED_TOPIC)

def build_input_stream(spark: SparkSession, kafka_url: str) -> DataStreamReader:
    base_stream = build_kafka_read_stream(spark, kafka_url, Config.KAFKA_RAW_TOPIC)
    return (base_stream
        .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
        .select(F.from_json(F.col("value"), raw_message_schema).alias("data"), "value")
    )


def apply_stream_transformation(stream: DataStreamReader) -> DataStreamReader:
    return (stream
        .withColumn("value", prepare_message(F.col("value")))
    )

@F.udf(returnType=StringType())
def prepare_message(message_raw: str) -> str:
    message = json.loads(message_raw)
    message["prepared_at"] = datetime.now().isoformat()
    # TODO: implement translation
    return json.dumps(message)

def write_stream_to_topic(input_stream: DataStreamReader, kafka_url: str, topic: str) -> None:
    (input_stream
        .writeStream
        .outputMode("update")
        .format("kafka")
        .option("kafka.bootstrap.servers", kafka_url)
        .option("checkpointLocation", "/tmp/checkpoint")
        .option("topic", topic)
        .start()
        .awaitTermination()
    )
