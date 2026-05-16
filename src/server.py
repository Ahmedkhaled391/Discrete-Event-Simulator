class Server:
    def __init__(self, server_number):
        self.server_number = server_number
        self.name = "S" + str(server_number)
        self.available_time = 0
        self.busy_time = 0
        self.current_customer = None

    def is_available(self):
        return self.current_customer is None

    def start_service(self, customer, current_time):
        begin_service = current_time
        end_service = begin_service + customer.service_time

        # The server becomes busy until this customer's service ends.
        self.current_customer = customer
        self.available_time = end_service
        self.busy_time += customer.service_time
        customer.start_service(begin_service, end_service, self.name)

        return begin_service, end_service

    def finish_service(self):
        finished_customer = self.current_customer
        self.current_customer = None
        return finished_customer


def create_servers(server_count):
    if server_count <= 0:
        raise ValueError("server_count must be at least 1")

    servers = []

    for i in range(server_count):
        servers.append(Server(i + 1))

    return servers


def find_available_server(servers):
    for server in servers:
        if server.is_available():
            return server

    return None


def has_available_server(servers):
    return find_available_server(servers) is not None


def find_next_departure_server(servers):
    next_server = None

    # Among busy servers, find the one whose service ends first.
    for server in servers:
        if not server.is_available():
            if next_server is None or server.available_time < next_server.available_time:
                next_server = server

    return next_server


def get_next_departure_time(servers):
    next_server = find_next_departure_server(servers)

    if next_server is None:
        return None

    return next_server.available_time


def has_busy_server(servers):
    return find_next_departure_server(servers) is not None


def finish_next_departure(servers):
    server = find_next_departure_server(servers)

    if server is None:
        return None, None

    # A departure event frees the server at its recorded available time.
    departure_time = server.available_time
    server.finish_service()

    return server, departure_time


def assign_customer_to_server(servers, customer, current_time):
    server = find_available_server(servers)

    if server is None:
        raise ValueError("No available server")

    begin_service, end_service = server.start_service(customer, current_time)

    return server, begin_service, end_service
