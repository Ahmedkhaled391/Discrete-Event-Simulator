import matplotlib.pyplot as plt

def plot_gantt_chart(results):
    if not results:
        return

    # Extract server numbers from strings like 'S1', 'S2'
    servers = sorted(set(int(row["server"][1:]) for row in results))
    total_time = max(row["end"] for row in results)

    plt.figure(figsize=(10, 5))
    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]

    for row in results:
        customer = row["customer"]
        begin = row["begin"]
        end = row["end"]
        server = int(row["server"][1:])
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
            begin + duration / 2, server, f"C{customer}",
            ha="center", va="center", color="white", fontsize=9
        )

    plt.xlabel("Simulation Time")
    plt.ylabel("Servers")
    plt.title("Gantt Chart")
    plt.xlim(0, total_time)
    plt.yticks(servers, [f"Server {s}" for s in servers])
    plt.grid(axis="x", linestyle="--", alpha=0.5)
    plt.show()


def plot_waiting_bar_chart(results):
    if not results:
        return

    # Filter out warm-up customers so the chart only shows valid statistics
    valid_results = [row for row in results if not row.get("is_warmup", False)]
    
    customer_numbers = [row["customer"] for row in valid_results]
    waits = [row["system_wait"] for row in valid_results]

    plt.figure(figsize=(10, 5))
    plt.bar(customer_numbers, waits, edgecolor="black")

    plt.xlabel("Customer Number")
    plt.ylabel("System Wait Time")
    plt.title("Waiting Time Bar Chart (Excluding Warm-up)")

    for c, w in zip(customer_numbers, waits):
        plt.text(c, w, str(round(w, 2)), ha="center", va="bottom")

    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.show()