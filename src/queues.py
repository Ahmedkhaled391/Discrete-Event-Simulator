try:
    from src.server import (
        assign_customer_to_server,
        find_available_server,
        finish_next_departure,
    )
except ModuleNotFoundError:
    from server import (
        assign_customer_to_server,
        find_available_server,
        finish_next_departure,
    )


FCFS = "FCFS"
LCFS = "LCFS"
SUPPORTED_DISCIPLINES = (FCFS, LCFS)


def normalize_discipline(discipline):
    normalized = discipline.upper()

    if normalized not in SUPPORTED_DISCIPLINES:
        raise ValueError("Unsupported queue discipline: " + discipline)

    return normalized


def add_waiting_customer(waiting_customers, customer):
    waiting_customers.append(customer)


def pop_next_waiting_customer(waiting_customers, discipline):
    if len(waiting_customers) == 0:
        return None

    discipline = normalize_discipline(discipline)

    if discipline == LCFS:
        return waiting_customers.pop()

    return waiting_customers.pop(0)


class LCFS_Simulation:
    def __init__(self, servers):
        self.servers = servers
        self.waiting_stack = []
        self.results = []

    def handle_arrival(self, customer):
        available_server = find_available_server(self.servers)

        if available_server and len(self.waiting_stack) == 0:
            available_server.start_service(customer, customer.arrival_time)
            self.results.append(customer.to_result_row())
        else:
            self.waiting_stack.append(customer)

    def handle_departure(self, current_time=None):
        _server, departure_time = finish_next_departure(self.servers)

        if departure_time is None:
            return None

        if len(self.waiting_stack) > 0:
            next_customer = self.waiting_stack.pop()
            assign_customer_to_server(self.servers, next_customer, departure_time)
            self.results.append(next_customer.to_result_row())

        return departure_time


def calculate_average_queue_wait(customers):
    served_customers = [
        customer for customer in customers if customer.begin_service is not None
    ]

    if len(served_customers) == 0:
        return 0

    total_wait = sum(customer.queue_wait() for customer in served_customers)
    return total_wait / len(served_customers)


def calculate_part4_metrics(customers):
    return calculate_average_queue_wait(customers)


def calculate_metrics(customers):
    return calculate_average_queue_wait(customers)
