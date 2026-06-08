from pyspark.sql import SparkSession

# Create Spark Session
spark = SparkSession.builder \
    .appName("TimeSeriesProject") \
    .master("local[*]") \
    .getOrCreate()

# Test DataFrame
data = [
    (1, "2025-05-29 10:00:00", 45.6),
    (2, "2025-05-29 10:01:00", 47.1),
    (3, "2025-05-29 10:02:00", 52.3)
]

df = spark.createDataFrame(data, ["id", "timestamp", "value"])
df.show()

print("✅ PySpark is working successfully!")
spark.stop()