from src.server import find_available_server, finish_next_departure, assign_customer_to_server

class LCFS_Simulation:
    def __init__(self, servers):
        self.servers = servers
        self.waiting_stack = [] 

    def handle_arrival(self, customer):
        available_server = find_available_server(self.servers)
        if available_server:
            available_server.start_service(customer, customer.arrival_time)
        else:
            self.waiting_stack.append(customer)

    def handle_departure(self, current_time):
        server, departure_time = finish_next_departure(self.servers)
        if self.waiting_stack:
            next_customer = self.waiting_stack.pop() 
            assign_customer_to_server(self.servers, next_customer, departure_time)

def calculate_part4_metrics(customers):
    total_wait = sum(c.queue_wait() for c in customers if c.begin_service is not None)
    avg_wait_W = total_wait / len(customers)
    return avg_wait_W