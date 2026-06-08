from storage.query_service import QueryService

service = QueryService()

data = service.get_all_latest_temperatures()

for row in data:
    print(row)

service.close()
