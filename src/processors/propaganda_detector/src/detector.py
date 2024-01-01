import json
import pyspark.sql.functions as F
from pyspark.sql.streaming.readwriter import DataStreamReader
from pyspark.sql.types import FloatType

from .config import Config
from .spark import build_kafka_read_stream, build_spark_context, parse_kafka_stream_by_schema
from .schema import prepared_message_schema


spark = build_spark_context(Config.SPARK_HOST, Config.SPARK_PORT)

def init_propaganda_detector() -> None:
    kafka_url = f"{Config.KAFKA_HOST}:{Config.KAFKA_PORT}"
    input_stream = build_stream(kafka_url)
    processed_stream = process_stream(input_stream)
    processed_stream.printSchema()

    elastic_url = f"{Config.ELASTIC_HOST}:{Config.ELASTIC_PORT}"
    write_stream_to_elastic(processed_stream, elastic_url, Config.ELASTIC_INDEX)

def build_stream(kafka_url: str) -> None:
    raw_stream = build_kafka_read_stream(spark, kafka_url, Config.KAFKA_PREPARED_TOPIC)
    return parse_kafka_stream_by_schema(raw_stream, prepared_message_schema)

def process_stream(stream: DataStreamReader) -> None:
    return (stream
        .selectExpr("value.*", "key")
        .withColumn("propaganda", predict_propaganda(F.col("text")))
    )

@F.udf(returnType=FloatType())
def predict_propaganda(text: str) -> float:
    return len(text) / 100

def write_stream_to_elastic(stream: DataStreamReader, elastic_url: str, resource: str) -> None:
    (stream
        .writeStream
        .outputMode("update")
        .format("org.elasticsearch.spark.sql")
        .option("es.nodes", elastic_url)
        .option("es.index.auto.create", "true")
        .option("es.resource", resource)
        .option("es.mapping.id", "key")
        .option("checkpointLocation", "/tmp/checkpoint/elastic")
        .start()
        .awaitTermination()
    )
