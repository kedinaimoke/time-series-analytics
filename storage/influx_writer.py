from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("INFLUX_TOKEN")
ORG = os.getenv("INFLUX_ORG")
BUCKET = os.getenv("INFLUX_BUCKET")


class InfluxWriter:

    def __init__(self):
        self.url = "http://localhost:8086"
        self.token = TOKEN
        self.org = ORG
        self.bucket = BUCKET

        self.client = InfluxDBClient(
            url=self.url,
            token=self.token,
            org=self.org
        )

        self.write_api = self.client.write_api(
            write_options=SYNCHRONOUS
        )

        print("Connected to InfluxDB")

    def write_sensor_data(self, data):

        try:
            point = (
                Point("sensor_metrics")
                .tag("sensor_id", data["sensor_id"])
                .tag("location", data["location"])

                .field("temperature", data["temperature"])
                .field("humidity", data["humidity"])
                .field("cpu_usage", data["cpu_usage"])
                .field("energy_consumption", data["energy_consumption"])

                .field("is_anomaly", int(data["is_anomaly"]))
                .field("anomaly_type", data["anomaly_type"] or "")
                .field("affected_metric", data["affected_metric"] or "")

                .time(data["timestamp"])
            )

            self.write_api.write(
                bucket=self.bucket,
                org=self.org,
                record=point
            )

        except Exception as e:
            print(f"InfluxDB write error: {e}")

    def close(self):
        self.client.close()
