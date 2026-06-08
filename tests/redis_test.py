from storage.query_service import QueryService

service = QueryService()

print(service.get_latest_temperature("sensor_1"))
print(service.get_latest_temperature("sensor_1"))
print(service.get_latest_temperature("sensor_1"))