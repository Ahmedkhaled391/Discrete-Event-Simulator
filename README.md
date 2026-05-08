# Discrete Event Simulation (DES) Project

This project implements a full queueing-system Discrete Event Simulation from scratch, following the lab description in report/Project Description.pdf. The simulation models customers arriving over time, waiting in a queue when needed, being served by one or more servers, and then leaving the system. The goal is to study system behavior using the core performance metrics W (average system wait), Q (average queue length), and U (server utilization).

Part 1 is represented by a dedicated generator module in src/generator.py. It is responsible for seed-based LCG random value generation, so runs are reproducible. Inter-arrival times and service times are generated from the same LCG rule and scaled to values in [1,10]. The required constants are a=1664525, c=1013904223, and m=2^32.

The simulation starts with FCFS single-server behavior, then extends to multi-server support where the number of servers s is user-configurable. Each customer record tracks key timestamps (arrival, begin service, end service), waiting times, and assigned server. For Part 4, FCFS is compared with one alternative discipline (LCFS or Priority), using Python built-in data structures rather than manual queue/stack/heap implementations.

Warm-up support is included in the structure design: the first k customers are simulated normally but excluded from reported statistics, which helps reduce transient-start bias. For reporting and visualization, the project includes a required Gantt chart and one additional chart script in charts.

## File Structure

```text
DES/
├── README.md
├── main.py
├── charts/
│   ├── gantt.py
│   └── waiting_bar.py
├── outputs/
│   └── .gitkeep              # Keeps the outputs directory tracked while it has no generated files.
├── report/
│   └── Project Description.pdf # Original assignment specification for the simulation.
└── src/
    ├── customer.py           # Planned customer data model for arrival/service timestamps;
    ├── generator.py          # Planned random input generator for arrivals and service times;
    ├── lcg.py                # Planned linear congruential generator implementation;
    ├── metrics.py            # Planned performance metrics calculations for W, Q, and U;
    ├── printer.py            # Planned formatting/output helpers for results;
    ├── queues.py             # Planned queue-discipline logic such as FCFS/LCFS/Priority;
    ├── server.py             # Planned server state and assignment logic;
    └── simulation.py         # Planned main simulation engine;




```
