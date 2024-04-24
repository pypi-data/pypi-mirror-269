import random
class LoadBalancer:
    def __init__(self, servers):
        self.servers = servers

    def random_selection(self):
        return random.choice(self.servers)
def simulate_client_requests(load_balancer, num_requests):
    for i in range(num_requests):
        print(f"Request {i+1}: ", end="")
        # Using Random algorithm for load balancing
        server_random = load_balancer.random_selection()
        print(f"Random - Server {server_random}")
servers = ["Server A", "Server B", "Server C"]
# Create a LoadBalancer instance
load_balancer = LoadBalancer(servers)
# Simulate 10 client requests
simulate_client_requests(load_balancer, 10)
