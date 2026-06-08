from influxdb_client import InfluxDBClient
import pandas as pd
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
  |> range(start: -24h)
'''

tables = query_api.query(query)

data = []

for table in tables:
    for record in table.records:
        data.append(record.values)

df = pd.DataFrame(data)

df.to_csv("sensor_data.csv", index=False)

print("Export complete: sensor_data.csv")