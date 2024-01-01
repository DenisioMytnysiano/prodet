from pyspark.sql.types import StructType, StructField, StringType

base_struct_fields = [
    StructField("id", StringType(), False),
    StructField("network_type", StringType(), False),
    StructField("user_id", StringType(), False),
    StructField("user_name", StringType(), False),
    StructField("chat_id", StringType(), False),
    StructField("chat_name", StringType(), False),
    StructField("text", StringType(), False),
    StructField("created_at", StringType(), False)
]

prepared_struct_fields = [
    *base_struct_fields,
    StructField("prepared_at", StringType(), False)
]

raw_message_schema = StructType(base_struct_fields)
prepared_message_schema = StructType(prepared_struct_fields)
