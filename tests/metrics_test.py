from storage.query_service import QueryService

service = QueryService()

data = service.get_all_latest_metrics()

for sensor in data:
    print(sensor)

service.close()