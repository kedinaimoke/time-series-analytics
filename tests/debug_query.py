from influxdb_client import InfluxDBClient
import os
from dotenv import load_dotenv

load_dotenv()

client = InfluxDBClient(
    url="http://localhost:8086",
    token=os.getenv("INFLUX_TOKEN"),
    org=os.getenv("INFLUX_ORG")
)

query_api = client.query_api()

query = """
from(bucket: "sensor_data")
  |> range(start: -365d)
"""

tables = query_api.query(query)

fields = set()

for table in tables:
    for record in table.records:
        fields.add(record.get_field())

print("\nFIELDS FOUND:\n")

for field in sorted(fields):
    print(field)