import psutil
import time
import matplotlib.pyplot as plt
from nqueens.sequential import SequentialNQueensSolver
from nqueens.parallel import ParallelNQueensSolver

def measure_resource_usage(func, *args, **kwargs):
    process = psutil.Process()

    start_cpu_percent = psutil.cpu_percent(interval=None)
    start_ram = process.memory_info().rss / 1024 / 1024  # Convert to MB
    start_time = time.time()

    result = func(*args, **kwargs)

    end_time = time.time()
    end_cpu_percent = psutil.cpu_percent(interval=None)
    end_ram = process.memory_info().rss / 1024 / 1024  # Convert to MB

    elapsed_time = end_time - start_time
    avg_cpu_percent = (start_cpu_percent + end_cpu_percent) / 2
    ram_usage = end_ram - start_ram

    return result, elapsed_time, avg_cpu_percent, ram_usage

def plot_overhead(n_values, seq_times, par_times):
    fig, ax = plt.subplots(figsize=(12, 6))

    # Calculate overhead
    overhead = [par - seq for par, seq in zip(par_times, seq_times)]

    # Create bar chart
    x = range(len(n_values))
    width = 0.35

    ax.bar([i - width/2 for i in x], seq_times, width, label='Sequential', alpha=0.7, color='skyblue')
    ax.bar([i + width/2 for i in x], par_times, width, label='Parallel', alpha=0.7, color='orange')

    # Add a line for overhead
    ax.plot(x, overhead, color='red', marker='o', linestyle='-', linewidth=2, label='Overhead')

    ax.set_xlabel('N (Board Size)')
    ax.set_ylabel('Execution Time (seconds)')
    ax.set_title('Process Overhead: Sequential vs Parallel')
    ax.legend()
    ax.grid(True)

    # Set x-axis ticks to N values
    ax.set_xticks(x)
    ax.set_xticklabels(n_values)

    # Add text label for average overhead
    avg_overhead = sum(overhead) / len(overhead)
    ax.text(len(n_values) / 2, max(max(seq_times), max(par_times)), f'Average Overhead: {avg_overhead:.2f}s',
            ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig('nqueens_overhead.png')
    plt.close()

def main():
    n_values = [4, 5, 6, 7, 8, 9, 10, 11, 12]
    seq_times = []
    par_times = []
    seq_cpu_usage = []
    par_cpu_usage = []
    seq_ram_usage = []
    par_ram_usage = []

    for n in n_values:
        print(f"\nSolving {n}-Queens problem:")

        # Sequential Solution
        seq_solver = SequentialNQueensSolver(n)
        (seq_solutions, seq_time), measured_time, seq_cpu_percent, seq_ram = measure_resource_usage(seq_solver.solve)
        seq_times.append(seq_time)
        seq_cpu_usage.append(seq_cpu_percent)
        seq_ram_usage.append(seq_ram)
        print(f"Sequential: {len(seq_solutions)} solutions found in {seq_time:.4f} seconds")
        print(f"CPU Usage (Sequential): {seq_cpu_percent:.2f}%")
        print(f"RAM Usage (Sequential): {seq_ram:.2f} MB")

        # Parallel Solution
        par_solver = ParallelNQueensSolver(n)
        (par_solutions, par_time), measured_time, par_cpu_percent, par_ram = measure_resource_usage(par_solver.solve)
        par_times.append(par_time)
        par_cpu_usage.append(par_cpu_percent)
        par_ram_usage.append(par_ram)
        print(f"Parallel: {len(par_solutions)} solutions found in {par_time:.4f} seconds")
        print(f"CPU Usage (Parallel): {par_cpu_percent:.2f}%")
        print(f"RAM Usage (Parallel): {par_ram:.2f} MB")

        # Calculate speedup
        speedup = seq_time / par_time
        print(f"Speedup: {speedup:.2f}x")

    # Plot the overhead graph
    plot_overhead(n_values, seq_times, par_times)

    # Plot resource usage
    plot_resource_usage(n_values, seq_cpu_usage, par_cpu_usage, seq_ram_usage, par_ram_usage)

def plot_resource_usage(n_values, seq_cpu_usage, par_cpu_usage, seq_ram_usage, par_ram_usage):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

    # Plot CPU usage
    ax1.plot(n_values, seq_cpu_usage, marker='o', label='Sequential')
    ax1.plot(n_values, par_cpu_usage, marker='s', label='Parallel')
    ax1.set_xlabel('N (Board Size)')
    ax1.set_ylabel('CPU Usage (%)')
    ax1.set_title('CPU Usage: Sequential vs Parallel')
    ax1.legend()
    ax1.grid(True)

    # Plot RAM usage
    ax2.plot(n_values, seq_ram_usage, marker='o', label='Sequential')
    ax2.plot(n_values, par_ram_usage, marker='s', label='Parallel')
    ax2.set_xlabel('N (Board Size)')
    ax2.set_ylabel('RAM Usage (MB)')
    ax2.set_title('RAM Usage: Sequential vs Parallel')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig('nqueens_resource_usage.png')
    plt.close()

if __name__ == "__main__":
    main()