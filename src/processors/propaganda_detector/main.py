from src.config import Config
from src.detector import init_propaganda_detector
from src.spark import build_spark_context
from src.normalizer import init_propaganda_normalizer


def main():
    spark = build_spark_context(Config.SPARK_HOST, Config.SPARK_PORT)
    init_propaganda_normalizer(spark)
    init_propaganda_detector(spark)

if __name__ == "__main__":
    main()
