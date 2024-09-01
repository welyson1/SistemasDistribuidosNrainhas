from nqueens.sequential import SequentialNQueensSolver
from nqueens.parallel import ParallelNQueensSolver

def main():
    n_values = [4, 5, 6, 7, 8, 9, 10, 11, 12]

    for n in n_values:
        print(f"\nResolvendo o problema das {n}-Rainhas:")

        # Solução Sequencial
        seq_solver = SequentialNQueensSolver(n)
        seq_solutions, seq_time = seq_solver.solve()
        print(f"Sequencial: {len(seq_solutions)} soluções encontradas em {seq_time:.4f} segundos")

        # Solução Paralela
        par_solver = ParallelNQueensSolver(n)
        par_solutions, par_time = par_solver.solve()
        print(f"Paralelo: {len(par_solutions)} soluções encontradas em {par_time:.4f} segundos")

        # Cálculo do speedup
        speedup = seq_time / par_time
        print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    main()
