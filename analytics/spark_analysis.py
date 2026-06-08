from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, avg, mean, stddev, abs as spark_abs
)

spark = SparkSession.builder \
    .appName("SensorAnalytics") \
    .getOrCreate()

df = spark.read.csv(
    "sensor_data.csv",
    header=True,
    inferSchema=True
)

print("\nRAW DATA SAMPLE")
df.show(5)
df.printSchema()

df = df.filter(col("_field").isNotNull())
df = df.filter(col("_value").isNotNull())

df = df.withColumn("_value", col("_value").cast("double"))

df = df.filter(col("_field") != "affected_metric")

pivot_df = df.groupBy("sensor_id").pivot("_field").avg("_value")

print("\nPIVOTED DATA")
pivot_df.show()

print("\nAverage Temperature per Sensor")

avg_temp = pivot_df.groupBy("sensor_id") \
    .agg(avg("temperature").alias("avg_temperature"))

avg_temp.show()

print("\nHigh CPU Usage (>55%)")

high_cpu = pivot_df.filter(col("cpu_usage") > 55)

high_cpu.show()

print("\nStatistical & Rule-Based Anomaly Detection")

stats = pivot_df.select(
    mean("temperature").alias("mean_temp"),
    stddev("temperature").alias("std_temp")
).collect()[0]

mean_temp = stats["mean_temp"]
std_temp = stats["std_temp"]

anomalies = pivot_df.filter(
    (col("cpu_usage") > 55) |
    (col("temperature") > 26) |
    (spark_abs(col("temperature") - mean_temp) > 1.5 * std_temp)
)

anomalies.show()

print("\nSensor Performance Summary")

summary = pivot_df.select(
    "sensor_id",
    "temperature",
    "cpu_usage",
    "humidity",
    "energy_consumption"
)

summary.show()

spark.stop()