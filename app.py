"""
GUI Application for Discrete Event Simulation.

Provides a user-friendly interface for running simulations with configurable parameters,
viewing results, and generating visualizations.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from src.lcg import generate_times
from src.warmup import run_simulation_with_warmup, average_utilization
from src.queues import FCFS, LCFS


class DESSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Discrete Event Simulator")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        self.simulation_result = None
        self.is_running = False

        self.setup_ui()

    def setup_ui(self):
        """Create the main UI components."""
        # Title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(pady=10)
        title_label = ttk.Label(
            title_frame,
            text="Discrete Event Simulation",
            font=("Arial", 16, "bold"),
        )
        title_label.pack()

        # Input Frame
        input_frame = ttk.LabelFrame(self.root, text="Simulation Parameters", padding=10)
        input_frame.pack(padx=10, pady=10, fill="x")

        # Number of customers
        ttk.Label(input_frame, text="Customers for statistics:").grid(row=0, column=0, sticky="w")
        self.customers_var = tk.StringVar(value="100")
        ttk.Entry(input_frame, textvariable=self.customers_var, width=15).grid(row=0, column=1, padx=5)

        # Seed
        ttk.Label(input_frame, text="Random Seed:").grid(row=0, column=2, sticky="w")
        self.seed_var = tk.StringVar(value="42")
        ttk.Entry(input_frame, textvariable=self.seed_var, width=15).grid(row=0, column=3, padx=5)

        # Servers
        ttk.Label(input_frame, text="Number of Servers:").grid(row=1, column=0, sticky="w")
        self.servers_var = tk.StringVar(value="1")
        ttk.Entry(input_frame, textvariable=self.servers_var, width=15).grid(row=1, column=1, padx=5)

        # Warm-up count
        ttk.Label(input_frame, text="Warm-up Customers:").grid(row=1, column=2, sticky="w")
        self.warmup_var = tk.StringVar(value="10")
        ttk.Entry(input_frame, textvariable=self.warmup_var, width=15).grid(row=1, column=3, padx=5)

        # Queue discipline
        ttk.Label(input_frame, text="Queue Discipline:").grid(row=2, column=0, sticky="w")
        self.discipline_var = tk.StringVar(value="FCFS")
        discipline_combo = ttk.Combobox(
            input_frame,
            textvariable=self.discipline_var,
            values=["FCFS", "LCFS"],
            state="readonly",
            width=13,
        )
        discipline_combo.grid(row=2, column=1, padx=5)

        # Run button
        self.run_button = ttk.Button(input_frame, text="Run Simulation", command=self.run_simulation)
        self.run_button.grid(row=2, column=2, columnspan=2, padx=5, pady=10, sticky="ew")

        # Results Frame
        results_frame = ttk.LabelFrame(self.root, text="Simulation Results", padding=10)
        results_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Results text area with scrollbar
        scrollbar = ttk.Scrollbar(results_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.results_text = tk.Text(
            results_frame,
            height=20,
            width=100,
            yscrollcommand=scrollbar.set,
            font=("Courier", 9),
        )
        self.results_text.pack(fill="both", expand=True)
        scrollbar.config(command=self.results_text.yview)

        # Button Frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10, fill="x", padx=10)

        ttk.Button(button_frame, text="Clear", command=self.clear_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Results", command=self.save_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side=tk.RIGHT, padx=5)

    def run_simulation(self):
        """Run simulation in a separate thread to prevent UI freezing."""
        if self.is_running:
            messagebox.showwarning("Warning", "Simulation is already running!")
            return

        try:
            # Validate inputs
            n = int(self.customers_var.get())
            seed = int(self.seed_var.get())
            servers = int(self.servers_var.get())
            warmup = int(self.warmup_var.get())

            if n <= 0 or servers <= 0 or warmup < 0:
                messagebox.showerror("Error", "Invalid input values!")
                return

            if warmup > n:
                messagebox.showerror("Error", "Warm-up count cannot exceed customer count!")
                return

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
            return

        self.is_running = True
        self.run_button.config(state="disabled")
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Running simulation...\n")

        thread = threading.Thread(target=self._execute_simulation, args=(n, seed, servers, warmup))
        thread.daemon = True
        thread.start()

    def _execute_simulation(self, n, seed, servers, warmup):
        """Execute simulation and display results."""
        try:
            discipline = FCFS if self.discipline_var.get() == "FCFS" else LCFS

            total_customers = n + warmup
            inter_arrival_times, service_times = generate_times(total_customers, seed)

            # Run without warm-up
            result_no_warmup = run_simulation_with_warmup(
                inter_arrival_times[:n],
                service_times[:n],
                servers,
                discipline,
                0,
            )

            # Run with warm-up
            result_with_warmup = run_simulation_with_warmup(
                inter_arrival_times,
                service_times,
                servers,
                discipline,
                warmup,
            )

            self.simulation_result = {
                "no_warmup": result_no_warmup,
                "with_warmup": result_with_warmup,
            }

            self.display_results()

        except Exception as e:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Error: {str(e)}\n")
        finally:
            self.is_running = False
            self.run_button.config(state="normal")

    def display_results(self):
        """Display simulation results in the text area."""
        if not self.simulation_result:
            return

        result_no_warmup = self.simulation_result["no_warmup"]
        result_with_warmup = self.simulation_result["with_warmup"]

        output = []
        output.append("=" * 65)
        output.append("DES SIMULATION RESULTS")
        output.append("=" * 65)
        output.append("")

        # Parameters
        output.append("PARAMETERS:")
        output.append(f"  Customers (statistics): {result_no_warmup['results'].__len__()}")
        output.append(f"  Servers: {result_no_warmup['server_count']}")
        output.append(f"  Discipline: {result_no_warmup['discipline']}")
        output.append(f"  Warm-up count: {result_with_warmup['warmup_count']}")
        output.append("")

        # Results without warm-up
        output.append("-" * 65)
        output.append("RUN A - WITHOUT WARM-UP")
        output.append("-" * 65)
        self._append_metrics(output, result_no_warmup)
        output.append("")

        # Results with warm-up
        output.append("-" * 65)
        output.append("RUN B - WITH WARM-UP")
        output.append("-" * 65)
        self._append_metrics(output, result_with_warmup)
        output.append("")

        # Comparison
        output.append("-" * 65)
        output.append("WARM-UP COMPARISON")
        output.append("-" * 65)
        self._append_comparison(output, result_no_warmup, result_with_warmup)
        output.append("=" * 65)

        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "\n".join(output))

    def _append_metrics(self, output, result):
        """Append metrics to output."""
        output.append(f"  Avg System Wait Time W = {result['W']:.3f} time units")
        output.append(f"  Avg Queue Length Q = {result['Q']:.3f} customers")

        for i, utilization in enumerate(result["utilizations"], start=1):
            output.append(f"  Server {i} utilization U = {utilization:.1f} %")

        avg_util = average_utilization(result)
        output.append(f"  Average utilization U = {avg_util:.1f} %")
        output.append(f"  Total simulation time = {result['total_time']:.1f} time units")

    def _append_comparison(self, output, result_no_warmup, result_with_warmup):
        """Append comparison to output."""
        diff_W = result_with_warmup["W"] - result_no_warmup["W"]
        diff_Q = result_with_warmup["Q"] - result_no_warmup["Q"]
        diff_U = average_utilization(result_with_warmup) - average_utilization(result_no_warmup)

        output.append(f"  {'Metric':<25} {'Without':<15} {'With':<15} {'Difference':<12}")
        output.append(f"  {'-' * 65}")
        output.append(
            f"  {'Avg System Wait W':<25} {result_no_warmup['W']:>14.3f} {result_with_warmup['W']:>14.3f} {diff_W:>+11.3f}"
        )
        output.append(
            f"  {'Avg Queue Length Q':<25} {result_no_warmup['Q']:>14.3f} {result_with_warmup['Q']:>14.3f} {diff_Q:>+11.3f}"
        )
        output.append(
            f"  {'Avg Utilization U (%)':<25} {average_utilization(result_no_warmup):>14.1f} {average_utilization(result_with_warmup):>14.1f} {diff_U:>+11.1f}"
        )

    def clear_results(self):
        """Clear the results text area."""
        self.results_text.delete(1.0, tk.END)
        self.simulation_result = None

    def save_results(self):
        """Save results to a file."""
        if not self.simulation_result:
            messagebox.showwarning("Warning", "No results to save!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )

        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write(self.results_text.get(1.0, tk.END))
                messagebox.showinfo("Success", f"Results saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DESSimulatorApp(root)
    root.mainloop()
