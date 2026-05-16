"""
Warm-up period logic for the DES project.

This module reuses the project's generator, simulation engine, queue
disciplines, and base metrics instead of carrying a second simulation copy.
"""

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.lcg import generate_times
from src.metrics import calculate_metrics
from src.queues import FCFS, normalize_discipline
from src.simulation import run_queue_simulation


LINE = "=" * 65
SMALL_LINE = "-" * 65


def mark_warmup_rows(results, warmup_count):
    marked_results = []

    for row in results:
        marked_row = row.copy()
        marked_row["is_warmup"] = row["customer"] <= warmup_count
        marked_results.append(marked_row)

    return marked_results


def post_warmup_rows(results):
    return [row for row in results if not row["is_warmup"]]


def observation_window(results):
    post_results = post_warmup_rows(results)

    if len(post_results) == 0:
        return 0, 0

    observation_start = min(row["arrival"] for row in post_results)
    total_time = max(row["end"] for row in results)
    window = total_time - observation_start

    if window <= 0:
        window = total_time

    return observation_start, window


def calculate_warmup_metrics(results, server_count):
    post_results = post_warmup_rows(results)

    if len(post_results) == 0:
        total_time = max((row["end"] for row in results), default=0)
        return 0, 0, [0] * server_count, total_time

    _observation_start, window = observation_window(results)
    total_time = max(row["end"] for row in results)
    total_system_wait = sum(row["system_wait"] for row in post_results)
    total_queue_wait = sum(row["queue_wait"] for row in post_results)
    server_busy_times = [0] * server_count

    for row in post_results:
        server_index = int(row["server"][1:]) - 1
        server_busy_times[server_index] += row["end"] - row["begin"]

    W = total_system_wait / len(post_results)
    Q = total_queue_wait / window if window > 0 else 0

    utilizations = []
    for busy_time in server_busy_times:
        utilization = (busy_time / window) * 100 if window > 0 else 0
        utilizations.append(utilization)

    return W, Q, utilizations, total_time


def run_simulation_with_warmup(
    inter_arrival_times,
    service_times,
    server_count=1,
    discipline=FCFS,
    warmup_count=0,
):
    discipline = normalize_discipline(discipline)

    if warmup_count < 0:
        raise ValueError("warmup_count must be non-negative")

    if warmup_count > len(inter_arrival_times):
        raise ValueError("warmup_count cannot exceed the number of customers")

    results = run_queue_simulation(
        inter_arrival_times,
        service_times,
        server_count,
        discipline,
    )
    marked_results = mark_warmup_rows(results, warmup_count)

    if warmup_count == 0:
        W, Q, utilizations, total_time = calculate_metrics(results, server_count)
    else:
        W, Q, utilizations, total_time = calculate_warmup_metrics(
            marked_results,
            server_count,
        )

    return {
        "results": marked_results,
        "W": W,
        "Q": Q,
        "utilizations": utilizations,
        "total_time": total_time,
        "warmup_count": warmup_count,
        "server_count": server_count,
        "discipline": discipline,
    }


def average_utilization(result):
    utilizations = result["utilizations"]

    if len(utilizations) == 0:
        return 0

    return sum(utilizations) / len(utilizations)


def print_event_table(result, show_warmup_marker=True):
    print(SMALL_LINE)
    print(
        f"{'#':<5}"
        f"{'Arrive':<8}"
        f"{'Begin':<8}"
        f"{'End':<8}"
        f"{'Server':<8}"
        f"{'SysWait':<9}"
        f"{'QWait':<7}"
    )

    for row in result["results"]:
        marker = "*" if row["is_warmup"] and show_warmup_marker else ""
        print(
            f"{str(row['customer']) + marker:<5}"
            f"{row['arrival']:<8}"
            f"{row['begin']:<8}"
            f"{row['end']:<8}"
            f"{row['server']:<8}"
            f"{row['system_wait']:<9}"
            f"{row['queue_wait']:<7}"
        )

    if result["warmup_count"] > 0 and show_warmup_marker:
        print("* = warm-up customer, excluded from statistics")


def print_results(result):
    print(SMALL_LINE)
    print("RESULTS")
    print("Average system waiting time W =", round(result["W"], 3), "min")
    print("Average queue length        Q =", round(result["Q"], 3), "customers")

    for i, utilization in enumerate(result["utilizations"], start=1):
        print("Server", i, "utilization       U =", round(utilization, 1), "%")

    print("Average utilization         U =", round(average_utilization(result), 1), "%")
    print("Total simulation time         =", result["total_time"], "time units")
    print("Warm-up customers             =", result["warmup_count"])


def print_warmup_comparison(result_no_warmup, result_with_warmup):
    diff_W = result_with_warmup["W"] - result_no_warmup["W"]
    diff_Q = result_with_warmup["Q"] - result_no_warmup["Q"]
    diff_U = average_utilization(result_with_warmup) - average_utilization(result_no_warmup)

    print(SMALL_LINE)
    print("WARM-UP COMPARISON")
    print(
        f"{'Metric':<28}"
        f"{'Without warm-up':>16}"
        f"{'With warm-up':>16}"
        f"{'Difference':>13}"
    )
    print(
        f"{'Avg System Wait W':<28}"
        f"{result_no_warmup['W']:>16.3f}"
        f"{result_with_warmup['W']:>16.3f}"
        f"{diff_W:>+13.3f}"
    )
    print(
        f"{'Avg Queue Length Q':<28}"
        f"{result_no_warmup['Q']:>16.3f}"
        f"{result_with_warmup['Q']:>16.3f}"
        f"{diff_Q:>+13.3f}"
    )
    print(
        f"{'Avg Utilization U (%)':<28}"
        f"{average_utilization(result_no_warmup):>16.1f}"
        f"{average_utilization(result_with_warmup):>16.1f}"
        f"{diff_U:>+13.1f}"
    )


def main():
    n = int(input("Enter number of customers used for statistics: "))
    seed = int(input("Enter seed: "))
    server_count = int(input("Enter number of servers: "))
    warmup_count = int(input("Enter warm-up count: "))

    total_customers = n + warmup_count
    inter_arrival_times, service_times = generate_times(total_customers, seed)

    print(LINE)
    print("DES WARM-UP PERIOD")
    print(LINE)
    print("Inter-arrival times :", inter_arrival_times)
    print("Service times       :", service_times)

    result_no_warmup = run_simulation_with_warmup(
        inter_arrival_times[:n],
        service_times[:n],
        server_count,
        FCFS,
        0,
    )
    result_with_warmup = run_simulation_with_warmup(
        inter_arrival_times,
        service_times,
        server_count,
        FCFS,
        warmup_count,
    )

    print(LINE)
    print("RUN A - WITHOUT WARM-UP")
    print_event_table(result_no_warmup)
    print_results(result_no_warmup)

    print(LINE)
    print("RUN B - WITH WARM-UP")
    print_event_table(result_with_warmup)
    print_results(result_with_warmup)

    print(LINE)
    print_warmup_comparison(result_no_warmup, result_with_warmup)
    print(LINE)


if __name__ == "__main__":
    main()
