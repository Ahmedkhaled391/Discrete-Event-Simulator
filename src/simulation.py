def calculate_arrival_times(inter_arrival_times):
    arrival_times = []
    current_time = 0

    for time in inter_arrival_times:
        current_time += time
        arrival_times.append(current_time)

    return arrival_times


def run_single_server_simulation(inter_arrival_times, service_times):
    arrival_times = calculate_arrival_times(inter_arrival_times)

    results = []
    server_available_time = 0

    for i in range(len(arrival_times)):
        arrival_time = arrival_times[i]
        service_time = service_times[i]

        begin_service = max(arrival_time, server_available_time)
        end_service = begin_service + service_time

        queue_wait = begin_service - arrival_time
        system_wait = end_service - arrival_time

        server_available_time = end_service

        customer_result = {
            "customer": i + 1,
            "arrival": arrival_time,
            "begin": begin_service,
            "end": end_service,
            "server": "S1",
            "system_wait": system_wait,
            "queue_wait": queue_wait
        }

        results.append(customer_result)

    return results