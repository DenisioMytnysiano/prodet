from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from config import PropagandaDetectorConfig

@F.udf
def predict_propaganda(text: str) -> bool:
    return False


def main():
    
    kafka_url = f"{PropagandaDetectorConfig.KAFKA_HOST}:{PropagandaDetectorConfig.KAFKA_PORT}"

    spark = (SparkSession.builder
        .remote("sc://localhost:15002")
        .config("spark.executorEnv.PYSPARK_PYTHON", "/opt/bitnami/python/bin/python3")
        .getOrCreate())

    input_stream = (spark.readStream
                    .format("kafka")
                    .option("kafka.bootstrap.servers", kafka_url)
                    .options("subscribe", PropagandaDetectorConfig.KAFKA_TOPIC)
                    .select(F.from_json(F.col("value").cast("string"), ).alias("data"), "timestamp")
                    .select("data.*", "timestamp")
                    .withColumn("is_propaganda", predict_propaganda(F.col("text"))))

    output_stream =  (input_stream.writeStream
            .format("console")
            .outputMode("append")
            .start()
            .awaitTermination())
    
if __name__ == "__main__":
    main()
