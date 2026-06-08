import time
from storage.query_service import QueryService


def benchmark(sensor_id="sensor_1", runs=50):

    service = QueryService()

    print("\n--- PERFORMANCE TEST START ---\n")

    start = time.time()
    result = service.get_latest_temperature(sensor_id)
    end = time.time()

    cold_latency = end - start

    print(f"\nCOLD START (Cache MISS)")
    print(f"Result: {result}")
    print(f"Latency: {cold_latency:.6f} seconds\n")

    warm_latencies = []

    for i in range(runs):
        start = time.time()
        result = service.get_latest_temperature(sensor_id)
        end = time.time()

        warm_latencies.append(end - start)

    avg_warm_latency = sum(warm_latencies) / len(warm_latencies)

    print(f"\nWARM START (Cache HIT)")
    print(f"Runs: {runs}")
    print(f"Average Latency: {avg_warm_latency:.6f} seconds\n")

    improvement = ((cold_latency - avg_warm_latency) / cold_latency) * 100

    print("--- FINAL RESULTS ---")
    print(f"Cold Latency: {cold_latency:.6f}s")
    print(f"Warm Latency: {avg_warm_latency:.6f}s")
    print(f"Performance Improvement: {improvement:.2f}%\n")


if __name__ == "__main__":
    benchmark()