import os
from dotenv import load_dotenv

load_dotenv()

print("TOKEN:", bool(os.getenv("INFLUX_TOKEN")))
print("ORG:", os.getenv("INFLUX_ORG"))
print("BUCKET:", os.getenv("INFLUX_BUCKET"))