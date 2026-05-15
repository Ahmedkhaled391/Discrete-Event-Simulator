def calculate_metrics(results):
    total_system_wait = 0
    total_queue_wait = 0
    total_service_time = 0

    for row in results:
        total_system_wait += row["system_wait"]
        total_queue_wait += row["queue_wait"]
        total_service_time += row["end"] - row["begin"]

    n = len(results)
    total_simulation_time = results[-1]["end"] if n > 0 else 0

    W = total_system_wait / n
    Q = total_queue_wait / total_simulation_time if total_simulation_time > 0 else 0
    U = (total_service_time / total_simulation_time) * 100 if total_simulation_time > 0 else 0

    return W, Q, U, total_simulation_time