from src.lcg import prepare_simulation_inputs
from src.simulation import run_single_server_simulation
from src.metrics import calculate_metrics

n = int(input("Enter number of customers: "))
seed = int(input("Enter seed: "))

inter_arrival_times, service_times = prepare_simulation_inputs(n, seed)

results = run_single_server_simulation(inter_arrival_times, service_times)

print("\nSingle Server FCFS Results:")
print("#  Arrival  Begin  End  Server  SysWait  QWait")

for row in results:
    print(
        row["customer"],
        row["arrival"],
        row["begin"],
        row["end"],
        row["server"],
        row["system_wait"],
        row["queue_wait"]
)
    W, Q, U, total_time = calculate_metrics(results)

print("\nRESULTS")
print("Average system waiting time W =", round(W, 3))
print("Average queue length Q =", round(Q, 3))
print("Server utilization U =", round(U, 1), "%")
print("Total simulation time =", total_time)