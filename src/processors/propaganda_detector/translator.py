import json
from datetime import datetime
import translators as ts
import pyspark.sql.functions as F
from pyspark.sql import Row
from pyspark.sql.streaming.readwriter import DataStreamReader
from pyspark.sql.types import StringType

from src.config import Config
from src.spark import (
    build_kafka_read_stream, build_spark_context, 
    parse_kafka_stream_by_schema, write_stream_to_kafka
)
from src.schema import raw_message_schema

spark = build_spark_context(Config.SPARK_HOST, Config.SPARK_PORT)


def init_propaganda_translator() -> None:    
    kafka_url = f"{Config.KAFKA_HOST}:{Config.KAFKA_PORT}"
    input_stream = build_stream(kafka_url)
    prepared_stream = prepare_stream(input_stream)
    write_stream_to_kafka(prepared_stream, kafka_url, Config.KAFKA_TRANSLATED_TOPIC, "translator")


def build_stream(kafka_url: str) -> DataStreamReader:
    raw_stream =  build_kafka_read_stream(spark, kafka_url, Config.KAFKA_RAW_TOPIC)
    return parse_kafka_stream_by_schema(raw_stream, raw_message_schema)


def prepare_stream(stream: DataStreamReader) -> DataStreamReader:
    return (stream
        .withColumn("value", prepare_message(F.col("value")))
    )


@F.udf(returnType=StringType())
def prepare_message(message_row: Row) -> str:
    import spacy
    import spacy_fastlang
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("language_detector")

    message_dict = message_row.asDict()
    message_dict["translated_at"] = datetime.now().isoformat()
    message_dict["language"] = nlp(message_dict["text"])._.language
    message_dict["original_text"] = message_dict["text"]
    if message_dict["language"] != "en":
        message_dict["text"] = ts.translate_text(message_dict["text"], translator='google', to_language='en')
    return json.dumps(message_dict)


if __name__ == '__main__':
    init_propaganda_translator()
