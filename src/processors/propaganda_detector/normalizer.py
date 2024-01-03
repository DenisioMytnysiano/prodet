import json
import re
from datetime import datetime
import uuid
import pyspark.sql.functions as F
from pyspark.sql import Row
from pyspark.sql.streaming.readwriter import DataStreamReader
from pyspark.sql.types import StringType

from src.config import Config
from src.spark import (
    build_kafka_read_stream, build_spark_context, 
    parse_kafka_stream_by_schema, write_stream_to_kafka
)
from src.schema import translated_message_schema


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
    message_dict["text"] = normalize_line(message_dict["text"])
    message_dict["text_words"] = message_dict["text"].split(" ")
    return json.dumps(message_dict)

def normalize_line(p: str) -> str:
    if not p:
        return p
    if p.startswith('"'):
        p = p[1:-2]
    p = p.lower()
    p = re.sub(r'http\S+', '', p)
    p = p.replace("\n", "")
    p = p.replace("&nbsp;", "")
    p = p.replace("\xa0", " ")
    p = p.replace("\u200b", " ")
    p = p.replace('""', '"')
    p = p.replace("/", "")
    p = p.replace("...", "")
    p = p.replace("[...]", "")
    p = p.replace("[---]", "")
    p = p.replace("[--]", "")
    p = p.replace("[]", "")
    p = p.replace("[", "")
    p = p.replace("]", "") 
    p = p.replace("(", "")
    p = p.replace(")", "") 
    p = p.replace("**", "")
    p = re.sub(" +", " ", p)
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    p = emoji_pattern.sub(r'', p)
    p = p.strip()
    return p

if __name__ == '__main__':
    init_propaganda_normalizer()
