import json
from datetime import datetime
import pyspark.sql.functions as F
from pyspark.sql.streaming.readwriter import DataStreamReader


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
        # .withColumn("prediction", process_message(F.col("value"))) # TODO: use pandas_udf
    )

# @F.pandas_udf(StringType(), PandasUDFType.SCALAR)
@F.udf()
def process_message(message_row: str) -> str:
    import time
    start = time.time()
    from keras.models import load_model
    import tensorflow_hub as hub

    if not process_message.model:
       process_message.model = load_model("/etc/propaganda-model.keras", custom_objects={
        'KerasLayer': hub.KerasLayer
    })

    message = message_row.asDict()
    prediction = process_message.model.predict([message["text"]])
    print("PREDICTION_TEST_NEW", prediction)

    message["propaganda"] = str(prediction[0][0])
    message["processed_at"] = datetime.now().isoformat()
    end = time.time()
    print("TIME_USED_TEST_NEW", end - start)  

    return json.dumps(message)
