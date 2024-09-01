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


def plot_resource_usage(n_values, seq_cpu_usage, par_cpu_usage, seq_ram_usage, par_ram_usage):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

    # Plot CPU
    ax1.plot(n_values, seq_cpu_usage, marker='o', label='Sequencial')
    ax1.plot(n_values, par_cpu_usage, marker='s', label='Paralelo')
    ax1.set_xlabel('N (Tabuleiro)')
    ax1.set_ylabel('Uso de CPU (%)')
    ax1.set_title('Uso de CPU: Sequencial e Paralelo')
    ax1.legend()
    ax1.grid(True)

    # Plot RAM
    ax2.plot(n_values, seq_ram_usage, marker='o', label='Sequencial')
    ax2.plot(n_values, par_ram_usage, marker='s', label='Paralelo')
    ax2.set_xlabel('N (Tabuleiro)')
    ax2.set_ylabel('Uso de RAM (MB)')
    ax2.set_title('Uso de RAM: Sequencial e Paralelo')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig('nqueens_resource_usage.png')
    plt.close()


def main():
    n_values = [4, 5, 6, 7, 8, 9, 10, 11, 12]
    seq_cpu_usage = []
    par_cpu_usage = []
    seq_ram_usage = []
    par_ram_usage = []

    for n in n_values:
        print(f"\nResolvendo o problema das {n}-Rainhas:")

        # Solução Sequencial
        seq_solver = SequentialNQueensSolver(n)
        (seq_solutions, seq_time), measured_time, seq_cpu_percent, seq_ram = measure_resource_usage(seq_solver.solve)
        seq_cpu_usage.append(seq_cpu_percent)
        seq_ram_usage.append(seq_ram)
        print(f"Sequencial: {len(seq_solutions)} soluções encontradas em {seq_time:.4f} segundos")
        print(f"Uso de CPU (Sequencial): {seq_cpu_percent:.2f}%")
        print(f"Uso de RAM (Sequencial): {seq_ram:.2f} MB")

        # Solução Paralela
        par_solver = ParallelNQueensSolver(n)
        (par_solutions, par_time), measured_time, par_cpu_percent, par_ram = measure_resource_usage(par_solver.solve)
        par_cpu_usage.append(par_cpu_percent)
        par_ram_usage.append(par_ram)
        print(f"Paralelo: {len(par_solutions)} soluções encontradas em {par_time:.4f} segundos")
        print(f"Uso de CPU (Paralelo): {par_cpu_percent:.2f}%")
        print(f"Uso de RAM (Paralelo): {par_ram:.2f} MB")

        # Cálculo do speedup
        speedup = seq_time / par_time
        print(f"Speedup: {speedup:.2f}x")

    # print("\nResource Usage Summary:")
    # for i, n in enumerate(n_values):
    #     print(
    #         f"{n}-Queens: Sequential CPU: {seq_cpu_usage[i]:.2f}%, RAM: {seq_ram_usage[i]:.2f} MB | Parallel CPU: {par_cpu_usage[i]:.2f}%, RAM: {par_ram_usage[i]:.2f} MB")

    # Plota o uso de recurso
    plot_resource_usage(n_values, seq_cpu_usage, par_cpu_usage, seq_ram_usage, par_ram_usage)



if __name__ == "__main__":
    main()