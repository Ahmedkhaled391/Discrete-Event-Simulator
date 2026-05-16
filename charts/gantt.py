import matplotlib.pyplot as plt

customers = [
    (1, 0, 0, 3, 1),
    (2, 1, 3, 7, 1),
    (3, 2, 2, 5, 2),
    (4, 4, 7, 9, 1),
    (5, 6, 6, 10, 2),
    (6, 8, 10, 13, 2)
]

servers = sorted(set(row[4] for row in customers))

total_time = max(row[3] for row in customers)

waiting_times = {
    customer: end - arrival
    for customer, arrival, begin, end, server in customers
}

plt.figure(figsize=(10, 5))

colors = [
    "tab:blue",
    "tab:orange",
    "tab:green",
    "tab:red",
    "tab:purple"
]

for customer, arrival, begin, end, server in customers:

    duration = end - begin

    plt.barh(
        y=server,
        width=duration,
        left=begin,
        height=0.5,
        color=colors[(server - 1) % len(colors)],
        edgecolor="black"
    )

    plt.text(
        begin + duration / 2,
        server,
        f"C{customer}",
        ha="center",
        va="center",
        color="white",
        fontsize=9
    )

plt.xlabel("Simulation Time")

plt.ylabel("Servers")

plt.title("Gantt Chart")

plt.xlim(0, total_time)

plt.yticks(
    servers,
    [f"Server {s}" for s in servers]
)

plt.grid(
    axis="x",
    linestyle="--",
    alpha=0.5
)

plt.show()

plt.figure(figsize=(10, 5))

customer_numbers = list(waiting_times.keys())

waits = list(waiting_times.values())

plt.bar(
    customer_numbers,
    waits,
    edgecolor="black"
)

plt.xlabel("Customer Number")

plt.ylabel("System Wait Time")

plt.title("Waiting Time Bar Chart")

for c, w in zip(customer_numbers, waits):

    plt.text(
        c,
        w,
        str(w),
        ha="center",
        va="bottom"
    )

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.5
)

plt.show()