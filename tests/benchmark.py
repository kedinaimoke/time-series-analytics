import time

from storage.query_service import QueryService


def benchmark(sensor_id="sensor_1", runs=50):

    service = QueryService()

    print("\nPERFORMANCE TEST\n")

    # Cache Miss
    start = time.time()

    result = service.get_latest_sensor_metrics(
        sensor_id
    )

    cold_latency = time.time() - start

    print("COLD START (CACHE MISS)")
    print(result)
    print(f"Latency: {cold_latency:.6f} seconds\n")

    # Cache Hits
    warm_latencies = []

    for _ in range(runs):

        start = time.time()

        service.get_latest_sensor_metrics(
            sensor_id
        )

        warm_latencies.append(
            time.time() - start
        )

    avg_warm_latency = (
        sum(warm_latencies)
        / len(warm_latencies)
    )

    improvement = (
        (cold_latency - avg_warm_latency)
        / cold_latency
    ) * 100

    print("WARM START (CACHE HIT)")
    print(f"Runs: {runs}")
    print(
        f"Average Latency: "
        f"{avg_warm_latency:.6f} seconds\n"
    )

    print("FINAL RESULTS")
    print(
        f"Cold Latency: "
        f"{cold_latency:.6f}s"
    )

    print(
        f"Warm Latency: "
        f"{avg_warm_latency:.6f}s"
    )

    print(
        f"Performance Improvement: "
        f"{improvement:.2f}%"
    )

    service.close()


if __name__ == "__main__":
    benchmark()
