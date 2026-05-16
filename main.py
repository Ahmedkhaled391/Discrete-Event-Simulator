from src.lcg import generate_times
from src.metrics import calculate_metrics
from src.queues import FCFS, LCFS, normalize_discipline
from src.simulation import run_multi_server_simulation, run_single_server_simulation
from src.warmup import run_simulation_with_warmup
from charts.gantt import plot_gantt_chart, plot_waiting_bar_chart

LINE = "=" * 61
SMALL_LINE = "-" * 61


def run_simulation(inter_arrival_times, service_times, server_count, discipline=FCFS):
    if server_count == 1:
        results = run_single_server_simulation(
            inter_arrival_times,
            service_times,
            discipline
        )
    else:
        results = run_multi_server_simulation(
            inter_arrival_times,
            service_times,
            server_count,
            discipline
        )

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
    print("Customers rejected           = 0")


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
        f"{'Queue Wait':<14}"
        f"{'Q (queue)':<12}"
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
            f"{round(average_queue_wait(results), 3):<14}"
            f"{round(Q, 3):<12}"
            f"{format_utilizations(utilizations):<35}"
            f"{comparison_comment(server_count)}"
        )


def average_queue_wait(results):
    if len(results) == 0:
        return 0

    total_queue_wait = sum(row["queue_wait"] for row in results)
    return total_queue_wait / len(results)


def queue_discipline_comment(discipline, fcfs_W, discipline_W):
    if discipline == FCFS:
        return "Baseline fairness"

    if discipline_W < fcfs_W:
        wait_text = "Lower W"
    elif discipline_W > fcfs_W:
        wait_text = "Higher W"
    else:
        wait_text = "Same W"

    return wait_text + ", less fair"


def print_queue_discipline_comparison(inter_arrival_times, service_times, server_count):
    print(SMALL_LINE)
    print("\nQUEUE DISCIPLINE COMPARISON")
    print(
        f"{'Discipline':<12}"
        f"{'Avg Wait W':<14}"
        f"{'Q (queue)':<12}"
        f"{'Avg QWait':<14}"
        f"Comment"
    )

    fcfs_results, fcfs_W, fcfs_Q, _fcfs_utilizations, _fcfs_total_time = run_simulation(
        inter_arrival_times,
        service_times,
        server_count,
        FCFS
    )

    for discipline in [FCFS, LCFS]:
        if discipline == FCFS:
            results = fcfs_results
            W = fcfs_W
            Q = fcfs_Q
        else:
            results, W, Q, _utilizations, _total_time = run_simulation(
                inter_arrival_times,
                service_times,
                server_count,
                discipline
            )

        print(
            f"{discipline:<12}"
            f"{round(W, 3):<14}"
            f"{round(Q, 3):<12}"
            f"{round(average_queue_wait(results), 3):<14}"
            f"{queue_discipline_comment(discipline, fcfs_W, W)}"
        )

    print(
        "LCFS uses a stack: newest waiting customer is served first, "
        "so older waiting customers can wait longer."
    )


def print_header():
    print(LINE)
    print("DISCRETE EVENT SIMULATION - QUEUEING SYSTEM")
    print(LINE)


def print_configuration(n, seed, server_count, discipline=FCFS, warm_up_count=0):
    print("Configuration:")
    print(f"{'Customers (n)':<22}: {n}")
    print(f"{'Seed':<22}: {seed}")
    print(f"{'Servers':<22}: {server_count}")
    print(f"{'Discipline':<22}: {discipline}")
    print(f"{'Distribution':<22}: Uniform [1,10]")
    print(f"{'Warm-up (k)':<22}: {warm_up_count}")  # Now dynamically uses warm_up_count
    print(f"{'Max queue length':<22}: Unlimited")


def print_generated_sequences(inter_arrival_times, service_times):
    print(SMALL_LINE)
    print("Inter-arrival times :", inter_arrival_times)
    print("Service times       :", service_times)


def input_discipline():
    while True:
        discipline = input("Enter queue discipline (FCFS/LCFS): ").strip()

        if discipline == "":
            return FCFS

        try:
            return normalize_discipline(discipline)
        except ValueError:
            print("Please enter FCFS or LCFS.")


def main():
    n = int(input("Enter number of customers: "))
    seed = int(input("Enter seed: "))
    server_count = int(input("Enter number of servers: "))
    discipline = input_discipline()
    
    # --- 2. ADD WARMUP INPUT ---
    warmup_count = int(input("Enter warm-up count (k) [0 for none]: "))

    # Generate times for ALL customers (n + warmup)
    inter_arrival_times, service_times = generate_times(n + warmup_count, seed)

    # --- 3. RUN SIMULATION USING WARMUP LOGIC ---
    # This automatically flags warmup rows and calculates metrics properly
    sim_data = run_simulation_with_warmup(
        inter_arrival_times,
        service_times,
        server_count,
        discipline,
        warmup_count
    )

    # Extract standard variables from the warm-up result dictionary
    results = sim_data["results"]
    W = sim_data["W"]
    Q = sim_data["Q"]
    utilizations = sim_data["utilizations"]
    total_time = sim_data["total_time"]

    print_header()
    print_configuration(n, seed, server_count, discipline, warmup_count)
    print_generated_sequences(inter_arrival_times, service_times)
    
    # Optional: If you want to show which ones are warmup in the table
    print(SMALL_LINE)
    print("EVENT TABLE (* = warm-up customer)")
    print(f"{'#':<5}{'Arrive':<8}{'Begin':<8}{'End':<8}{'Server':<8}{'SysWait':<9}{'QWait':<7}")
    for row in results:
        marker = "*" if row.get("is_warmup", False) else " "
        print(
            f"{str(row['customer']) + marker:<5}"
            f"{row['arrival']:<8}"
            f"{row['begin']:<8}"
            f"{row['end']:<8}"
            f"{row['server']:<8}"
            f"{row['system_wait']:<9}"
            f"{row['queue_wait']:<7}"
        )

    print_results(W, Q, utilizations, total_time)
    print_queue_discipline_comparison(inter_arrival_times, service_times, server_count)
    print_comparison_table(inter_arrival_times, service_times)
    print(LINE)

    # --- 4. TRIGGER CHARTS AT THE END ---
    print("Generating charts...")
    plot_gantt_chart(results)
    plot_waiting_bar_chart(results)


if __name__ == "__main__":
    main()
