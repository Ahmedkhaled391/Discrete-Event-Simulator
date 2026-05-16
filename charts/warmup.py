"""
Part 5 — Warm-up Period
=======================
Discrete Event Simulation — Single/Multi-Server Queue with Warm-up Support.

This module can run standalone OR be imported by your main project file.

Usage (standalone):
    python part5_warmup.py

Integration with your project:
    from part5_warmup import run_simulation_with_warmup, print_warmup_comparison
"""

# ─────────────────────────────────────────────
# PART 1 — LCG Random Number Generator
# (kept here so this file is self-contained)
# ─────────────────────────────────────────────

def lcg(seed, n):
    """
    Linear Congruential Generator.
    Returns a list of n values in range [1, 10].
    Formula: X_(n+1) = (a * X_n + c) mod m
    """
    a = 1664525
    c = 1013904223
    m = 2**32

    values = []
    x = seed
    for _ in range(n):
        x = (a * x + c) % m
        values.append((x % 10) + 1)   # scale to [1, 10]
    return values


# ─────────────────────────────────────────────
# CORE SIMULATION ENGINE (Single-Server FCFS)
# Supports warm-up: first k customers are
# simulated but excluded from W, Q, U stats.
# ─────────────────────────────────────────────

def run_simulation_with_warmup(inter_arrivals, service_times, num_servers=1,
                                discipline="FCFS", warmup_k=0):
    """
    Run a multi-server FCFS/LCFS simulation with optional warm-up period.

    Parameters
    ----------
    inter_arrivals : list[int]   — inter-arrival times for ALL customers (including warm-up)
    service_times  : list[int]   — service times for ALL customers (including warm-up)
    num_servers    : int         — number of parallel servers
    discipline     : str         — "FCFS" or "LCFS"
    warmup_k       : int         — number of warm-up customers (excluded from stats)

    Returns
    -------
    dict with keys:
        events        — list of event dicts (all customers)
        W             — avg system wait (post-warmup only)
        Q             — avg queue length (post-warmup only)
        U             — server utilization list per server (post-warmup only)
        total_time    — total simulation end time
        warmup_k      — the k value used
    """
    n_total = len(inter_arrivals)

    # ── Build arrival times from inter-arrival times ──
    arrival_times = []
    t = 0
    for ia in inter_arrivals:
        t += ia
        arrival_times.append(t)

    # ── Server state: when each server becomes free ──
    server_free_at = [0] * num_servers   # time when server s becomes free

    # ── Queue (list of customer indices waiting) ──
    waiting_queue = []   # holds customer indices

    # ── Event records ──
    events = []

    # ── Busy time per server (for utilization, post-warmup only) ──
    busy_time = [0] * num_servers

    # ── Process customers one by one ──
    # We simulate ALL customers but only record stats for index >= warmup_k
    for i in range(n_total):
        arr = arrival_times[i]
        svc = service_times[i]
        is_warmup = (i < warmup_k)

        # Find the earliest free server at or after arrival
        earliest_free = min(server_free_at)
        earliest_server = server_free_at.index(earliest_free)

        begin = max(arr, earliest_free)
        end   = begin + svc
        queue_wait  = begin - arr          # time spent waiting in queue
        system_wait = end   - arr          # total time in system

        # Update server free time
        server_free_at[earliest_server] = end

        # Accumulate busy time only for post-warmup customers
        if not is_warmup:
            busy_time[earliest_server] += svc

        events.append({
            "customer":    i + 1,
            "arrive":      arr,
            "begin":       begin,
            "end":         end,
            "server":      earliest_server + 1,
            "sys_wait":    system_wait,
            "queue_wait":  queue_wait,
            "is_warmup":   is_warmup,
        })

    # ── Compute metrics (post-warmup customers only) ──
    post_events = [e for e in events if not e["is_warmup"]]

    if not post_events:
        return {"events": events, "W": 0, "Q": 0, "U": [0]*num_servers,
                "total_time": max(e["end"] for e in events), "warmup_k": warmup_k}

    total_time = max(e["end"] for e in events)

    # W — average system wait
    W = sum(e["sys_wait"] for e in post_events) / len(post_events)

    # Q — average queue length (Little's Law: Q = λ * Wq)
    # Wq = avg queue wait among post-warmup customers
    Wq = sum(e["queue_wait"] for e in post_events) / len(post_events)
    # Effective observation window (from first post-warmup arrival to end)
    obs_start = post_events[0]["arrive"]
    obs_window = total_time - obs_start if total_time > obs_start else total_time
    n_post = len(post_events)
    lambda_eff = n_post / obs_window if obs_window > 0 else 0
    Q = lambda_eff * Wq

    # U — per-server utilization over observation window
    U = [(bt / obs_window) * 100 if obs_window > 0 else 0
         for bt in busy_time]

    return {
        "events":     events,
        "W":          W,
        "Q":          Q,
        "U":          U,
        "total_time": total_time,
        "warmup_k":   warmup_k,
    }

# PRETTY PRINTING HELPERS

def print_event_table(result, show_warmup_marker=True):
    """Print the full event table, marking warm-up rows with (*)."""
    events    = result["events"]
    warmup_k  = result["warmup_k"]

    print(f"\n{'#':>4}  {'Arrive':>7}  {'Begin':>6}  {'End':>5}  "
          f"{'Server':>6}  {'SysWait':>8}  {'QWait':>7}")
    print("-" * 58)
    for e in events:
        marker = " *" if e["is_warmup"] and show_warmup_marker else "  "
        print(f"{e['customer']:>4}{marker}  {e['arrive']:>7}  {e['begin']:>6}  "
              f"{e['end']:>5}  {'S'+str(e['server']):>6}  "
              f"{e['sys_wait']:>8}  {e['queue_wait']:>7}")
    if warmup_k > 0:
        print("  (* = warm-up customer, excluded from statistics)")


def print_results(result):
    """Print W, Q, U summary."""
    U_avg = sum(result["U"]) / len(result["U"])
    print(f"\n  Avg system wait      W  = {result['W']:.3f} time units")
    print(f"  Avg queue length     Q  = {result['Q']:.3f} customers")
    print(f"  Server utilization   U  = {U_avg:.1f} %")
    print(f"  Total simulation time   = {result['total_time']} time units")
    print(f"  Warm-up customers   (k) = {result['warmup_k']}")


def print_warmup_comparison(result_no_warmup, result_with_warmup):
    """
    Print the comparison table required by Part 5.
    """
    k = result_with_warmup["warmup_k"]
    U0 = sum(result_no_warmup["U"]) / len(result_no_warmup["U"])
    Uk = sum(result_with_warmup["U"]) / len(result_with_warmup["U"])

    diff_W = result_with_warmup["W"] - result_no_warmup["W"]
    diff_Q = result_with_warmup["Q"] - result_no_warmup["Q"]
    diff_U = Uk - U0

    header = f"{'Metric':<28} {'Without warm-up':>16} {'With warm-up (k='+str(k)+')':>18} {'Difference':>12}"
    sep    = "-" * len(header)
    print(f"\n{sep}")
    print(header)
    print(sep)
    print(f"{'Avg System Wait  W':<28} {result_no_warmup['W']:>16.3f} {result_with_warmup['W']:>18.3f} {diff_W:>+12.3f}")
    print(f"{'Avg Queue Length Q':<28} {result_no_warmup['Q']:>16.3f} {result_with_warmup['Q']:>18.3f} {diff_Q:>+12.3f}")
    print(f"{'Server Utilization U (%)':<28} {U0:>16.1f} {Uk:>18.1f} {diff_U:>+12.1f}")
    print(sep)
    print("\n  Observation:")
    print("  W and Q are slightly higher with warm-up because the artificially")
    print("  low initial measurements (empty system at t=0) are excluded.")
    print("  The effect is more pronounced with small n.")


# MAIN — Standalone demo

def main():
    print("=" * 65)
    print("  DISCRETE EVENT SIMULATION — PART 5: WARM-UP PERIOD")
    print("=" * 65)

    # ── User inputs ──
    try:
        n    = int(input("\n  Enter number of customers (n)  [default 20]: ") or 20)
        seed = int(input("  Enter random seed              [default 42]: ") or 42)
        s    = int(input("  Enter number of servers (s)    [default 1 ]: ") or 1)
        k    = int(input("  Enter warm-up count (k)        [default 3 ]: ") or 3)
    except ValueError:
        print("  Invalid input. Using defaults: n=20, seed=42, s=1, k=3")
        n, seed, s, k = 20, 42, 1, 3

    # ── Generate random values (n + k customers total) ──
    total_customers = n + k
    inter_arrivals = lcg(seed,        total_customers)
    service_times  = lcg(seed + 1,    total_customers)   # different seed for service

    print(f"\n  Inter-arrival times : {inter_arrivals}")
    print(f"  Service times       : {service_times}")

    # Run 1 — WITHOUT warm-up (k = 0)
    print("\n" + "=" * 65)
    print(f"  RUN A — No warm-up (k = 0), using first {n} customers")
    print("=" * 65)

    result_k0 = run_simulation_with_warmup(
        inter_arrivals[:n], service_times[:n],
        num_servers=s, warmup_k=0
    )
    print_event_table(result_k0)
    print_results(result_k0)

    # Run 2 — WITH warm-up (k customers skipped)

    print("\n" + "=" * 65)
    print(f"  RUN B — With warm-up (k = {k}), {n} stat customers + {k} warm-up")
    print("=" * 65)

    result_kN = run_simulation_with_warmup(
        inter_arrivals, service_times,
        num_servers=s, warmup_k=k
    )
    print_event_table(result_kN)
    print_results(result_kN)

    # Comparison Table
    print("\n" + "=" * 65)
    print("  PART 5 — WARM-UP COMPARISON TABLE")
    print("=" * 65)
    print_warmup_comparison(result_k0, result_kN)

    print("\n" + "=" * 65)


if __name__ == "__main__":
    main()