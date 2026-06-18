from storage.query_service import QueryService

service = QueryService()

history = service.get_temperature_history(
    "sensor_1"
)

print(
    f"Records returned: {len(history)}"
)

print(
    history[:5]
)

service.close()
