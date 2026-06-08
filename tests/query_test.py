from influxdb_client import InfluxDBClient
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("INFLUX_TOKEN")
ORG = os.getenv("INFLUX_ORG")
BUCKET = os.getenv("INFLUX_BUCKET")

client = InfluxDBClient(
    url="http://localhost:8086",
    token=TOKEN,
    org=ORG
)

query_api = client.query_api()

query = f'''
from(bucket: "{BUCKET}")
  |> range(start: -1h)
'''

tables = query_api.query(query)

count = 0

for table in tables:
    for record in table.records:
        print(record.values)
        count += 1

print(f"\nRetrieved {count} records")