from src.lcg import generate_times
from src.metrics import calculate_metrics
from src.simulation import run_multi_server_simulation, run_single_server_simulation


LINE = "=" * 61
SMALL_LINE = "-" * 61


def run_simulation(inter_arrival_times, service_times, server_count):
    if server_count == 1:
        results = run_single_server_simulation(inter_arrival_times, service_times)
    else:
        results = run_multi_server_simulation(inter_arrival_times, service_times, server_count)

    W, Q, utilizations, total_time = calculate_metrics(results, server_count)

    return results, W, Q, utilizations, total_time


def print_event_table(results):
    print(SMALL_LINE)
    print(f"{'#':<4}{'Arrive':<8}{'Begin':<8}{'End':<8}{'Server':<8}{'SysWait':<9}{'QWait':<7}")

    for row in results:
        print(
            f"{row['customer']:<4}"
            f"{row['arrival']:<8}"
            f"{row['begin']:<8}"
            f"{row['end']:<8}"
            f"{row['server']:<8}"
            f"{row['system_wait']:<9}"
            f"{row['queue_wait']:<7}"
        )


def print_results(W, Q, utilizations, total_time):
    print(SMALL_LINE)
    print("\nRESULTS")
    print("Average system waiting time W =", round(W, 3), "min")
    print("Average queue length        Q =", round(Q, 3), "customers")

    for i in range(len(utilizations)):
        print("Server", i + 1, "utilization       U =", round(utilizations[i], 1), "%")

    print("Total simulation time        =", total_time, "time units")


def format_utilizations(utilizations):
    text_parts = []

    for i in range(len(utilizations)):
        text_parts.append("S" + str(i + 1) + "=" + str(round(utilizations[i], 1)) + "%")

    return ", ".join(text_parts)


def server_label(server_count):
    if server_count == 1:
        return "1 server"

    return str(server_count) + " servers"


def comparison_comment(server_count):
    if server_count == 1:
        return "Baseline"
    if server_count == 2:
        return "Better"

    return "Best, diminishing returns"


def print_comparison_table(inter_arrival_times, service_times):
    print(SMALL_LINE)
    print("\nMULTI-SERVER COMPARISON")
    print(
        f"{'Servers':<10}"
        f"{'Avg Wait W':<14}"
        f"{'Queue Q':<12}"
        f"{'Utilization':<35}"
        f"Comment"
    )

    for server_count in [1, 2, 3]:
        results, W, Q, utilizations, total_time = run_simulation(
            inter_arrival_times,
            service_times,
            server_count
        )

        print(
            f"{server_label(server_count):<10}"
            f"{round(W, 3):<14}"
            f"{round(Q, 3):<12}"
            f"{format_utilizations(utilizations):<35}"
            f"{comparison_comment(server_count)}"
        )


def print_header():
    print(LINE)
    print("DISCRETE EVENT SIMULATION - QUEUEING SYSTEM")
    print(LINE)


def print_configuration(n, seed, server_count):
    print("Configuration:")
    print(f"{'Customers (n)':<22}: {n}")
    print(f"{'Seed':<22}: {seed}")
    print(f"{'Servers':<22}: {server_count}")
    print(f"{'Discipline':<22}: FCFS")
    print(f"{'Distribution':<22}: Uniform [1,10]")
    print(f"{'Max queue length':<22}: Unlimited")


def print_generated_sequences(inter_arrival_times, service_times):
    print(SMALL_LINE)
    print("Inter-arrival times :", inter_arrival_times)
    print("Service times       :", service_times)


n = int(input("Enter number of customers: "))
seed = int(input("Enter seed: "))
server_count = int(input("Enter number of servers: "))

inter_arrival_times, service_times = generate_times(n, seed)

results, W, Q, utilizations, total_time = run_simulation(
    inter_arrival_times,
    service_times,
    server_count
)

print_header()
print_configuration(n, seed, server_count)
print_generated_sequences(inter_arrival_times, service_times)
print_event_table(results)
print_results(W, Q, utilizations, total_time)
print_comparison_table(inter_arrival_times, service_times)
print(LINE)
