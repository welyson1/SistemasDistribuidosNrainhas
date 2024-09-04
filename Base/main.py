from nqueens.sequential import SequentialNQueensSolver
from nqueens.parallel import ParallelNQueensSolver

def main():
    # Lista de tamanhos de tabuleiro a serem testados
    n_values = [4, 8, 10]

    # Para cada Tamanho da Lista, faça:
    for n in n_values:
        print(f"\nResolvendo o problema das {n}-Rainhas:") # Tamanho do problema atual
        # Instância do solucionador sequencial
        seq_solver = SequentialNQueensSolver(n)
        # O método solve() retorna uma tupla (soluções, tempo)
        seq_solutions, seq_time = seq_solver.solve()
        # Imprime os resultados da solução sequencial
        print(f"Sequencial: {len(seq_solutions)} soluções encontradas em {seq_time:.4f} segundos")
        # Cria uma instância do solucionador paralelo
        par_solver = ParallelNQueensSolver(n)
        # Executa a solução paralela e mede o tempo
        # O método solve() retorna uma tupla (soluções, tempo)
        par_solutions, par_time = par_solver.solve()
        # Imprime os resultados da solução paralela
        print(f"Paralelo: {len(par_solutions)} soluções encontradas em {par_time:.4f} segundos")

        # Calcula o speedup (ganho de desempenho da versão paralela)
        speedup = seq_time / par_time
        # SpeedUp
        print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    main()