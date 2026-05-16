try:
    from src.customer import Customer
    from src.queues import (
        FCFS,
        LCFS,
        add_waiting_customer,
        normalize_discipline,
        pop_next_waiting_customer,
    )
    from src.server import (
        assign_customer_to_server,
        create_servers,
        finish_next_departure,
        get_next_departure_time,
        has_available_server,
        has_busy_server,
    )
except ModuleNotFoundError:
    from customer import Customer
    from queues import (
        FCFS,
        LCFS,
        add_waiting_customer,
        normalize_discipline,
        pop_next_waiting_customer,
    )
    from server import (
        assign_customer_to_server,
        create_servers,
        finish_next_departure,
        get_next_departure_time,
        has_available_server,
        has_busy_server,
    )


def calculate_arrival_times(inter_arrival_times):
    arrival_times = []
    current_time = 0

    for time in inter_arrival_times:
        current_time += time
        arrival_times.append(current_time)

    return arrival_times


def start_customer_service(servers, customer, current_time, results):
    assign_customer_to_server(
        servers,
        customer,
        current_time
    )

    # Store the row after the customer has begin/end/server values.
    results.append(customer.to_result_row())


def run_queue_simulation(inter_arrival_times, service_times, server_count, discipline=FCFS):
    if len(inter_arrival_times) != len(service_times):
        raise ValueError("inter_arrival_times and service_times must have the same length")

    discipline = normalize_discipline(discipline)
    arrival_times = calculate_arrival_times(inter_arrival_times)

    results = []
    servers = create_servers(server_count)
    waiting_customers = []
    next_arrival_index = 0

    # Next-event loop: stop only when no arrivals remain and all servers are idle.
    while next_arrival_index < len(arrival_times) or has_busy_server(servers):
        if next_arrival_index < len(arrival_times):
            next_arrival_time = arrival_times[next_arrival_index]
        else:
            next_arrival_time = None

        next_departure_time = get_next_departure_time(servers)

        # If the next departure happens before the next arrival, process it first.
        if next_departure_time is not None and (
            next_arrival_time is None or next_departure_time <= next_arrival_time
        ):
            _finished_server, current_time = finish_next_departure(servers)

            # A free server takes the next waiting customer according to the discipline.
            next_customer = pop_next_waiting_customer(waiting_customers, discipline)

            if next_customer is not None:
                start_customer_service(servers, next_customer, current_time, results)
        else:
            # Otherwise, process the next arriving customer.
            current_time = next_arrival_time
            customer = Customer(
                next_arrival_index + 1,
                next_arrival_time,
                service_times[next_arrival_index]
            )

            next_arrival_index += 1

            # New arrivals only start immediately if no one is already waiting.
            if has_available_server(servers) and len(waiting_customers) == 0:
                start_customer_service(servers, customer, current_time, results)
            else:
                add_waiting_customer(waiting_customers, customer)

    results.sort(key=lambda row: row["customer"])

    return results


def run_fcfs_simulation(inter_arrival_times, service_times, server_count):
    return run_queue_simulation(inter_arrival_times, service_times, server_count, FCFS)


def run_lcfs_simulation(inter_arrival_times, service_times, server_count):
    return run_queue_simulation(inter_arrival_times, service_times, server_count, LCFS)


def run_single_server_simulation(inter_arrival_times, service_times, discipline=FCFS):
    return run_queue_simulation(inter_arrival_times, service_times, 1, discipline)


def run_multi_server_simulation(inter_arrival_times, service_times, server_count, discipline=FCFS):
    return run_queue_simulation(
        inter_arrival_times,
        service_times,
        server_count,
        discipline
    )
