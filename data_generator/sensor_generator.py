import json
import time
import random
import logging
from datetime import datetime, timezone
from storage.influx_writer import InfluxWriter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class SensorDataGenerator:
    def __init__(
        self,
        num_sensors=5,
        interval_seconds=1,
        anomaly_probability=0.02,
        output_file="sensor_stream.jsonl"
    ):
        self.num_sensors = num_sensors
        self.interval = interval_seconds
        self.anomaly_probability = anomaly_probability
        self.output_file = output_file
        self.anomaly_counter = 0

        self.sensor_metadata = {
            "sensor_1": {
                "location": "Floor_1",
                "temp": 24.5,
                "hum": 55.0,
                "cpu": 45.0,
                "energy": 110.0
            },
            "sensor_2": {
                "location": "Floor_1",
                "temp": 26.0,
                "hum": 60.0,
                "cpu": 52.0,
                "energy": 125.0
            },
            "sensor_3": {
                "location": "Floor_2",
                "temp": 23.8,
                "hum": 52.0,
                "cpu": 38.0,
                "energy": 98.0
            },
            "sensor_4": {
                "location": "Floor_2",
                "temp": 25.2,
                "hum": 58.0,
                "cpu": 48.0,
                "energy": 115.0
            },
            "sensor_5": {
                "location": "Server_Room",
                "temp": 27.1,
                "hum": 63.0,
                "cpu": 55.0,
                "energy": 130.0
            }
        }

    def generate_anomaly(self, value, anomaly_type):
        if anomaly_type == "spike":
            return value + random.uniform(15, 35)

        if anomaly_type == "drop":
            return max(0, value - random.uniform(15, 30))

        return value

    def generate_sensor_data(self):
        sensor_id = f"sensor_{random.randint(1, self.num_sensors)}"
        sensor = self.sensor_metadata[sensor_id]

        temperature = sensor["temp"] + random.gauss(0, 1.2)
        humidity = sensor["hum"] + random.gauss(0, 2.5)
        cpu_usage = sensor["cpu"] + random.gauss(0, 4)
        energy = sensor["energy"] + random.gauss(0, 3)

        is_anomaly = False
        anomaly_type = None
        affected_metric = None

        self.anomaly_counter += 1

        if (
            random.random() < self.anomaly_probability
            or self.anomaly_counter >= 45
        ):
            is_anomaly = True
            anomaly_type = random.choice(["spike", "drop"])

            affected_metric = random.choice(
                ["temperature", "cpu_usage"]
            )

            if affected_metric == "temperature":
                temperature = self.generate_anomaly(
                    temperature,
                    anomaly_type
                )
            else:
                cpu_usage = self.generate_anomaly(
                    cpu_usage,
                    anomaly_type
                )

            logging.warning(
                f"ANOMALY GENERATED | "
                f"Sensor={sensor_id} | "
                f"Metric={affected_metric} | "
                f"Type={anomaly_type}"
            )

            self.anomaly_counter = 0

        status = "normal"

        if random.random() < 0.005:
            status = "offline"

        if is_anomaly:
            status = "warning"

        temperature = round(max(15.0, min(45.0, temperature)), 2)
        humidity = round(max(20.0, min(85.0, humidity)), 1)
        cpu_usage = round(max(0.0, min(100.0, cpu_usage)), 1)
        energy = round(max(50.0, min(200.0, energy)), 2)

        return {
            "sensor_id": sensor_id,
            "location": sensor["location"],
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),

            "temperature": temperature,
            "humidity": humidity,
            "cpu_usage": cpu_usage,
            "energy_consumption": energy,

            "status": status,

            # Ground-truth labels for evaluation
            "is_anomaly": is_anomaly,
            "anomaly_type": anomaly_type,
            "affected_metric": affected_metric
        }

    def save_to_file(self, data):
        with open(self.output_file, "a") as file:
            file.write(json.dumps(data) + "\n")

    def stream_data(self, writer,max_records=None):
        count = 0

        logging.info(
            f"Starting sensor stream "
            f"(interval={self.interval}s)"
        )

        while True:
            data = self.generate_sensor_data()
            writer.write_sensor_data(data)

            print(json.dumps(data))

            self.save_to_file(data)

            count += 1

            if max_records and count >= max_records:
                break

            time.sleep(self.interval)

        logging.info(f"Generated {count} records.")


if __name__ == "__main__":

    writer = InfluxWriter()

    generator = SensorDataGenerator(
        num_sensors=5,
        interval_seconds=1,
        anomaly_probability=0.02
    )

    try:
        generator.stream_data(writer)

    except KeyboardInterrupt:
        logging.info("Sensor data generator stopped.")
