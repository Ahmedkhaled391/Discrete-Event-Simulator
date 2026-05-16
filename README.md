# Discrete Event Simulation (DES) Project

A comprehensive queueing-system Discrete Event Simulation implementation that models customers arriving, waiting, being served, and leaving a system. This project studies system behavior using core performance metrics: **W** (average system wait time), **Q** (average queue length), and **U** (server utilization).

## Overview

This project implements a full DES from scratch following the lab specification in `report/Project Description.pdf`. Key features include:

- **Reproducible Results**: Seed-based Linear Congruential Generator (LCG) for deterministic random number generation
- **Multi-Server Support**: Configurable number of servers with load balancing
- **Queue Disciplines**: FCFS (First-Come-First-Served), LCFS (Last-Come-First-Served), and Priority-based scheduling
- **Warm-up Period**: Exclude initial transient customers from statistics to reduce start-up bias
- **Performance Metrics**: Automatic calculation of W, Q, and U for system analysis
- **Visualizations**: Gantt charts and waiting time bar charts for result analysis

## Project Structure

```
DES/
├── README.md                          # Project documentation
├── main.py                            # CLI entry point for simulations
├── app.py                             # GUI application (tkinter-based)
├── charts/
│   ├── gantt.py                       # Gantt chart visualization
│   └── waiting_bar.py                 # Waiting time distribution chart
├── outputs/
│   └── .gitkeep                       # Directory for generated charts
├── report/
│   └── Project Description.pdf        # Original assignment specification
└── src/
    ├── customer.py                    # Customer data model
    ├── generator.py                   # Random input generator
    ├── lcg.py                         # Linear congruential generator
    ├── metrics.py                     # Performance metrics calculations
    ├── printer.py                     # Output formatting utilities
    ├── queues.py                      # Queue discipline implementations
    ├── server.py                      # Server state management
    ├── simulation.py                  # Main simulation engine
    └── warmup.py                      # Warm-up period logic
```

## How It Works

### 1. Random Number Generation
The project uses an LCG (Linear Congruential Generator) with constants specified by the assignment:
- **a** = 1664525
- **c** = 1013904223
- **m** = 2³²

This generates reproducible sequences of inter-arrival times and service times in the range [1, 10].

### 2. Simulation Engine
The simulation processes events in chronological order:
1. Customers arrive at the system
2. If a server is free, service begins immediately
3. Otherwise, customers join the queue
4. When a server finishes, the next queued customer is served
5. Process continues until all customers are served

### 3. Performance Metrics
After simulation:
- **W**: Average time customers spend in the system (queue + service)
- **Q**: Average number of customers in the queue (excluding those being served)
- **U**: Server utilization percentage (time busy / total time)

### 4. Warm-up Period
To reduce transient start-up bias:
- Simulate k "warm-up" customers before the observation window
- These customers are processed normally but excluded from final statistics
- This stabilizes queue behavior before measurements begin

## Usage

### GUI Application (Recommended)
```bash
python app.py
```

The graphical interface provides:
- **Easy Parameter Input**: Set customers, seed, servers, warm-up count, and queue discipline
- **Real-time Results**: View simulation metrics with warm-up comparison
- **Background Processing**: Simulation runs without freezing the UI
- **Result Export**: Save results to a text file for further analysis
- **Multiple Disciplines**: Switch between FCFS and LCFS queue disciplines

**GUI Features:**
- Interactive input fields for all simulation parameters
- Live results display with detailed metrics
- Side-by-side comparison of simulations with and without warm-up
- Save results to file functionality
- Non-blocking simulation execution (runs in background thread)

### CLI Application Usage
```bash
python main.py
```

The command-line interface will prompt for:
- Number of servers
- Warm-up customer count

### Example Session
```
Enter number of customers used for statistics: 100
Enter seed: 42
Enter number of servers: 2
Enter warm-up count: 10
```

Output includes:
- Event table showing each customer's timestamps and wait times
- Performance metrics (W, Q, U)
- Comparison between runs with and without warm-up

### Running Specific Scripts

**Gantt Chart Visualization:**
```bash
python charts/gantt.py
```

**Waiting Time Chart:**
```bash
python charts/waiting_bar.py
```

## Key Modules

### `app.py`
Tkinter-based GUI application for running simulations interactively:
- User-friendly input interface for all simulation parameters
- Real-time results display with metrics comparison
- Background thread execution to prevent UI freezing
- Save results to file functionality
- Support for multiple queue disciplines (FCFS, LCFS)

### `src/lcg.py`
Implements the Linear Congruential Generator for reproducible random number generation.

### `src/simulation.py`
Core simulation engine that processes arrival and departure events in chronological order.

### `src/warmup.py`
Handles warm-up period logic:
- Marks warm-up customers vs. observation window customers
- Calculates metrics excluding warm-up period
- Compares results with and without warm-up

### `src/queues.py`
Queue discipline implementations:
- FCFS: First-Come-First-Served (default)
- LCFS: Last-Come-First-Served
- Priority: Priority-based scheduling

### `src/metrics.py`
Calculates W, Q, and U from simulation results.

## Example Output

```
=================================================================
DES WARM-UP PERIOD
=================================================================
Inter-arrival times : [2.5, 3.1, 1.8, ...]
Service times       : [4.2, 2.9, 3.5, ...]

=================================================================
RUN A - WITHOUT WARM-UP
...
RESULTS
Average system waiting time W = 5.234 min
Average queue length        Q = 2.156 customers
Server 1 utilization       U = 85.3 %
Average utilization        U = 85.3 %

=================================================================
RUN B - WITH WARM-UP
...
WARM-UP COMPARISON
Metric                   Without warm-up  With warm-up  Difference
Avg System Wait W              5.234          4.891        -0.343
Avg Queue Length Q             2.156          1.923        -0.233
Avg Utilization U (%)         85.3          84.1           -1.2
```

## Installation

No external dependencies required. Uses Python 3.6+ standard library only.

```bash
git clone https://github.com/Ahmedkhaled391/Discrete-Event-Simulator.git
cd Discrete-Event-Simulator

pip install -r requirements.txt

streamlit run app.py

```

## Features

✅ Reproducible results via seed-based RNG  
✅ Multi-server queue system  
✅ Multiple queue disciplines (FCFS, LCFS, Priority)  
✅ Warm-up period support  
✅ Comprehensive performance metrics  
✅ Event-driven simulation engine  
✅ Visualization tools (Gantt chart, waiting time distribution)  
✅ Clean, modular code structure  

## Contributing

To extend this project:
1. Add new queue disciplines in `src/queues.py`
2. Implement additional metrics in `src/metrics.py`
3. Create new visualizations in `charts/`
4. Improve simulation features in `src/simulation.py`

## License

Academic project for discrete event simulation study.
