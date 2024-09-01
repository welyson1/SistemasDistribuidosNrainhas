from nqueens.sequential import SequentialNQueensSolver
from nqueens.parallel import ParallelNQueensSolver
import matplotlib.pyplot as plt
import platform
import os
import multiprocessing

def main():
    # Lista de tamanhos de tabuleiro a serem testados
    n_values = [4, 8, 10, 12]
    
    # Listas para armazenar os resultados
    seq_times = []
    par_times = []
    speedups = []
    efficiencies = []
    num_processes_list = []

    # Para cada Tamanho da Lista, faça:
    for n in n_values:
        print(f"\nResolvendo o problema das {n}-Rainhas:")  # Tamanho do problema atual
        # Instância do solucionador sequencial
        seq_solver = SequentialNQueensSolver(n)
        seq_solutions, seq_time = seq_solver.solve()
        seq_times.append(seq_time)  # Armazena o tempo sequencial
        print(f"Sequencial: {len(seq_solutions)} soluções encontradas em {seq_time:.4f} segundos")

        # Cria uma instância do solucionador paralelo
        par_solver = ParallelNQueensSolver(n)
        par_solutions, par_time = par_solver.solve()
        par_times.append(par_time)  # Armazena o tempo paralelo
        num_processes_list.append(par_solver.num_processes)  # Armazena o número de processos
        print(f"Paralelo: {len(par_solutions)} soluções encontradas em {par_time:.4f} segundos")

        # Calcula o speedup (ganho de desempenho da versão paralela)
        speedup = seq_time / par_time
        speedups.append(speedup)
        print(f"Speedup: {speedup:.2f}x")

        # Calcula a eficiência
        efficiency = speedup / par_solver.num_processes
        efficiencies.append(efficiency)
        print(f"Eficiência: {efficiency:.2f}")

    # Informações do sistema
    system_info = (f"CPU: {platform.processor()}\n"
                   f"Núcleos: {multiprocessing.cpu_count()}\n"
                   f"SO: {platform.system()} {platform.release()}\n"
                   f"Python: {platform.python_version()}\n"
                   f"IDE: {os.getenv('IDE', 'Visual Studio Code')}")

    # Gera o primeiro conjunto de gráficos (Speedup e Eficiência)
    plt.figure(figsize=(12, 8))

    # Título principal com informações do sistema
    plt.suptitle("" + system_info, fontsize=12)

    # Gráfico de Speedup
    plt.subplot(2, 1, 1)
    plt.plot(n_values, speedups, marker='o', label='Speedup', color='blue')
    plt.title('Speedup da Solução Paralela')
    plt.xlabel('Tamanho do Tabuleiro (N)')
    plt.ylabel('Speedup')
    plt.xticks(n_values)
    plt.grid(True)
    plt.legend()

    # Adiciona anotações com o número de processos usados
    for i, n in enumerate(n_values):
        plt.annotate(f"{num_processes_list[i]} processos", (n, speedups[i]), textcoords="offset points", xytext=(0, 10), ha='center')

    # Gráfico de Eficiência
    plt.subplot(2, 1, 2)
    plt.plot(n_values, efficiencies, marker='o', label='Eficiência', color='green')
    plt.title('Eficiência da Solução Paralela')
    plt.xlabel('Tamanho do Tabuleiro (N)')
    plt.ylabel('Eficiência')
    plt.xticks(n_values)
    plt.grid(True)
    plt.legend()

    # Exibe o primeiro conjunto de gráficos
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Ajusta o layout para incluir o título principal
    plt.show()

    # Após fechar o primeiro gráfico, gera o segundo conjunto de gráficos (Comparação de tempos)
    plt.figure(figsize=(12, 6))

    # Gráfico comparando os tempos sequencial e paralelo
    plt.plot(n_values, seq_times, marker='o', label='Sequencial', color='red')
    plt.plot(n_values, par_times, marker='o', label='Paralelo', color='blue')
    plt.title('Comparação dos Tempos de Execução')
    plt.xlabel('Tamanho do Tabuleiro (N)')
    plt.ylabel('Tempo de Execução (segundos)')
    plt.xticks(n_values)
    plt.grid(True)
    plt.legend()

    # Exibe o segundo gráfico
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
