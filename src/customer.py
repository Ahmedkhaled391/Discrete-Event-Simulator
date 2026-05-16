class Customer:
    def __init__(self, customer_number, arrival_time, service_time):
        self.customer_number = customer_number
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.begin_service = None
        self.end_service = None
        self.server_name = None

    def start_service(self, begin_service, end_service, server_name):
        self.begin_service = begin_service
        self.end_service = end_service
        self.server_name = server_name

    def queue_wait(self):
        return self.begin_service - self.arrival_time

    def system_wait(self):
        return self.end_service - self.arrival_time

    def to_result_row(self):
        return {
            "customer": self.customer_number,
            "arrival": self.arrival_time,
            "begin": self.begin_service,
            "end": self.end_service,
            "server": self.server_name,
            "system_wait": self.system_wait(),
            "queue_wait": self.queue_wait()
        }
