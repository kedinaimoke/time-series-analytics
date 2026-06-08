# Time-Series Analytics with Caching Layer

This is a project by:

- **Jane Kedina Imoke**
- **Ricardo Ramos Morales**

## Project Overview

This project implements a Big Data time-series analytics pipeline using a combination of the following technologies:

- INFLUXDB: Time-series database for sensor data storage.
- REDIS: Caching layer fo rfast query responses.
- APACHE SPARK (PYSPARK): Batch analytics engine.
- PYTHON: Data generation.

This system was built to simulate real-world IoT sensor data processing with:
- Real-time data ingestion.
- Query optimisation via caching.
- Historical batch analytics.
- Anomaly detection.

## Objectives

- Build a scalable time-series data pipeline.
- Demonstrate caching performance improvements.
- Perform batch analytics on historical data using Spark.
- Detect anomalies in sensor behaviour.
- Evaluate system performance via cache vs non-cache queries.

+----------------------+
| Sensor Generator     |
| (Python Streaming)   |
+----------+-----------+
|
v
+----------------------+
| InfluxDB            |
| Time-series storage |
+----------+-----------+
|
v
+----------------------+
| Redis Cache      |
| Fast query layer |
+----------+-----------+
|
v
+----------------------+
| Query Service      |
| (Python API layer) |
+----------+-----------+
|
v
+----------------------+
| Apache Spark    |
| Batch Analytics |
+----------------------+

## Project Structure
time-series-analytics-with-caching-layer/
│
├── data_generator/
│   └── sensor_generator.py
│
├── storage/
│   ├── influx_writer.py
│   └── query_service.py
│
├── cache/
│   └── redis_cache.py
│
├── analytics/
│   ├── export_data.py
│   └── spark_analysis.py
│
├── docker/
│   └── docker_compose.yml
│
├── tests/
│   ├── benchmark.py
│   └── redis_test.py
│
├── sensor_data.csv
└── README.md

## Technologies Used:

### Database(s)
- InfluxDB (Time-series Database)
- Redis (In-memory cache)

### Processing
- Apache Spark (PySpark)

### Programming
- Python 3.11.5

### Libaries
- `influxdb-client`
- `redis`
- `pyspark`
- `pandas`

## Features

### 1. Sensor Data Simulation
- Generates synthetic IoT sensor data.
- Includes:
    - temperature,
    - humidity,
    - CPU usage,
    - energy consumption
- Inject random anomalies.

### 2. Time-Series Storage (InfluxDB)
- Stores sensor data in real-time.
- Uses structured measurement and tags.
- Supports efficient time-based queries.

### 3. Redis Caching Layer
- Caches frequent entries
- Reduces database load.
- Improves response time significantly.

### 4. Spark Batch Analysis
Performs historical analysis of:
- Average sensor values per device.
- CPU usage filtering.
- Sensor performance summaries.
- **Hybrid** anomaly detection.

### 5. Anomaly detection

This takes 2 approaches:

#### Rule-Based:
- CPU usage threshold (>55%)
- Temperature threshold (>26C)

#### Statistical:
- Z-score based detection
- Uses mean & standard deviation

## How to Run Project

### 1. Start InfluxDB and Redis (Docker)
```
docker compose up -d
```

### 2. Run Sensor Generator (Python)
```
python data_generator.sensor_generator
```

### 3. Write the Data to InfluxDB
```
python -m storage.influx_writer
```

### 4. Export Data for Spark
```
python -m analytics/export_data
```

### 5. Run Spark
```
python -m analytics.spark_analytics
```

## THIS PROJECT IS FOR ACADEMIC PURPOSES>