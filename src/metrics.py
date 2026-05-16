def calculate_metrics(results, server_count):
    total_system_wait = 0
    total_queue_wait = 0
    server_busy_times = [0] * server_count

    for row in results:
        total_system_wait += row["system_wait"]
        total_queue_wait += row["queue_wait"]

        server_number = int(row["server"][1:])
        server_index = server_number - 1
        service_time = row["end"] - row["begin"]
        server_busy_times[server_index] += service_time

    n = len(results)
    total_simulation_time = results[-1]["end"] if n > 0 else 0

    W = total_system_wait / n if n > 0 else 0
    Q = total_queue_wait / total_simulation_time if total_simulation_time > 0 else 0

    utilizations = []
    for busy_time in server_busy_times:
        if total_simulation_time > 0:
            utilization = (busy_time / total_simulation_time) * 100
        else:
            utilization = 0

        utilizations.append(utilization)

    return W, Q, utilizations, total_simulation_time
