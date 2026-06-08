import json
import os

from dotenv import load_dotenv
from influxdb_client import InfluxDBClient

from cache.redis_cache import RedisCache

load_dotenv()

TOKEN = os.getenv("INFLUX_TOKEN")
ORG = os.getenv("INFLUX_ORG")
BUCKET = os.getenv("INFLUX_BUCKET")


class QueryService:

    def __init__(self):

        self.cache = RedisCache()

        self.client = InfluxDBClient(
            url="http://localhost:8086",
            token=TOKEN,
            org=ORG
        )

        self.query_api = self.client.query_api()

    def get_latest_sensor_metrics(self, sensor_id):

        cache_key = f"metrics:{sensor_id}"

        cached = self.cache.get(cache_key)

        if cached:
            print("CACHE HIT")
            return json.loads(cached)

        print("CACHE MISS")

        query = f'''
        from(bucket: "{BUCKET}")
          |> range(start: -24h)
          |> filter(fn: (r) => r.sensor_id == "{sensor_id}")
          |> filter(fn: (r) =>
                r._field == "temperature" or
                r._field == "humidity" or
                r._field == "cpu_usage" or
                r._field == "energy_consumption"
          )
          |> pivot(
                rowKey: ["_time"],
                columnKey: ["_field"],
                valueColumn: "_value"
          )
          |> sort(columns: ["_time"], desc: true)
          |> limit(n: 1)
        '''

        # tables = self.query_api.query(query)
        try:
            tables = self.query_api.query(query)
        except Exception as e:
            print("InfluxDB connection failed:", e)
            return []

        result = None

        for table in tables:
            for record in table.records:

                result = {
                    "sensor_id": sensor_id,
                    "temperature": record.values.get("temperature"),
                    "humidity": record.values.get("humidity"),
                    "cpu_usage": record.values.get("cpu_usage"),
                    "energy_consumption": record.values.get("energy_consumption"),
                    "timestamp": str(record.get_time())
                }

        if result:

            self.cache.set(
                cache_key,
                result,
                ttl=60
            )

        return result

    def get_all_latest_metrics(self):

        sensors = [
            "sensor_1",
            "sensor_2",
            "sensor_3",
            "sensor_4",
            "sensor_5"
        ]

        results = []

        for sensor_id in sensors:

            data = self.get_latest_sensor_metrics(sensor_id)

            if data:
                results.append(data)

        return results

    def close(self):
        self.client.close()
