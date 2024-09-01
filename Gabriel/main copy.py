import matplotlib.pyplot as plt
import multiprocessing
from nqueens.sequential import SequentialNQueensSolver
from nqueens.parallel import ParallelNQueensSolver

def run_nqueens_and_collect_data(n_values):
    """
    Executa o solucionador de N-Rainhas para vários tamanhos de tabuleiro e coleta dados de desempenho.
    
    :param n_values: Lista de tamanhos de tabuleiro a serem testados
    :return: Listas de speedups e eficiências
    """
    speedups = []
    efficiencies = []
    num_processors = multiprocessing.cpu_count()

    for n in n_values:
        print(f"\nResolvendo o problema das {n}-Rainhas:")
        
        # Resolver usando o método sequencial
        seq_solver = SequentialNQueensSolver(n)
        seq_solutions, seq_time = seq_solver.solve()
        print(f"Sequencial: {len(seq_solutions)} soluções encontradas em {seq_time:.4f} segundos")
        
        # Resolver usando o método paralelo
        par_solver = ParallelNQueensSolver(n)
        par_solutions, par_time = par_solver.solve()
        print(f"Paralelo: {len(par_solutions)} soluções encontradas em {par_time:.4f} segundos")

        # Calcular speedup e eficiência
        speedup = seq_time / par_time
        efficiency = speedup / num_processors
        
        print(f"Speedup: {speedup:.2f}x")
        print(f"Eficiência: {efficiency:.2f}")
        
        speedups.append(speedup)
        efficiencies.append(efficiency)
    
    return speedups, efficiencies

def plot_results(n_values, speedups, efficiencies):
    """
    Gera gráficos de Speedup e Eficiência.
    
    :param n_values: Lista de tamanhos de tabuleiro testados
    :param speedups: Lista de speedups correspondentes
    :param efficiencies: Lista de eficiências correspondentes
    """
    plt.figure(figsize=(12, 5))
    
    # Gráfico de Speedup
    plt.subplot(1, 2, 1)
    plt.plot(n_values, speedups, 'bo-')
    plt.title('Speedup vs. Tamanho do Tabuleiro')
    plt.xlabel('Tamanho do Tabuleiro (N)')
    plt.ylabel('Speedup')
    plt.grid(True)
    
    # Gráfico de Eficiência
    plt.subplot(1, 2, 2)
    plt.plot(n_values, efficiencies, 'ro-')
    plt.title('Eficiência vs. Tamanho do Tabuleiro')
    plt.xlabel('Tamanho do Tabuleiro (N)')
    plt.ylabel('Eficiência')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

def main():
    # Lista de tamanhos de tabuleiro a serem testados
    n_values = [4, 8, 10, 12]
    
    # Executar o solucionador e coletar dados
    speedups, efficiencies = run_nqueens_and_collect_data(n_values)
    
    # Gerar gráficos
    plot_results(n_values, speedups, efficiencies)

if __name__ == "__main__":
    main()