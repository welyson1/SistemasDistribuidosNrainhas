from nqueens.sequential import SequentialNQueensSolver
from nqueens.parallel import ParallelNQueensSolver
import matplotlib.pyplot as plt

def main():
    # Lista de tamanhos de tabuleiro a serem testados
    n_values = [4, 8, 10, 12]
    seq_times = []
    par_times = []
    speedups = []
    efficiencies = []

    # Para cada tamanho da lista, faça:
    for n in n_values:
        print(f"\nResolvendo o problema das {n}-Rainhas:")
        seq_solver = SequentialNQueensSolver(n)
        seq_solutions, seq_time = seq_solver.solve()
        print(f"Sequencial: {len(seq_solutions)} soluções encontradas em {seq_time:.4f} segundos")
        
        par_solver = ParallelNQueensSolver(n)
        par_solutions, par_time = par_solver.solve()
        print(f"Paralelo: {len(par_solutions)} soluções encontradas em {par_time:.4f} segundos")

        speedup = seq_time / par_time
        print(f"Speedup: {speedup:.2f}x")

        efficiency = (speedup / par_solver.num_processes) * 100
        print(f"Eficiência: {efficiency:.2f}%")

        seq_times.append(seq_time)
        par_times.append(par_time)
        speedups.append(speedup)
        efficiencies.append(efficiency)

    # Visualizando os gráficos
    plt.figure(figsize=(14, 8))

    # Gráfico de Tempos de Execução
    plt.subplot(2, 2, 1)
    plt.plot(n_values, seq_times, marker='o', label='Sequencial', color='blue')
    plt.plot(n_values, par_times, marker='o', label='Paralelo', color='green')
    plt.title('Tempos de Execução')
    plt.xlabel('Tamanho do Tabuleiro (N)')
    plt.ylabel('Tempo (segundos)')
    plt.legend()
    plt.grid(True)

    # Gráfico de Speedup
    plt.subplot(2, 2, 2)
    plt.plot(n_values, speedups, marker='o', color='purple')
    plt.title('Speedup')
    plt.xlabel('Tamanho do Tabuleiro (N)')
    plt.ylabel('Speedup')
    plt.grid(True)

    # Gráfico de Eficiência
    plt.subplot(2, 2, 4)
    plt.plot(n_values, efficiencies, marker='o', color='orange')
    plt.title('Eficiência')
    plt.xlabel('Tamanho do Tabuleiro (N)')
    plt.ylabel('Eficiência (%)')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
