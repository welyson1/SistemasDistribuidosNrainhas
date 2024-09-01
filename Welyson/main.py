# main.py
from nqueens.sequential import SequentialNQueensSolver
from nqueens.parallel import ParallelNQueensSolver
from nqueens.logger import NQueensLogger
from nqueens.image_generator import NQueensHeatmapGenerator

def main(generate_heatmaps=True):
    logger = NQueensLogger()
    n_values = [4, 8, 10, 12, 13]

    for n in n_values:
        print(f"\nResolvendo o problema das {n}-Rainhas:")

        # Solução Sequencial
        seq_solver = SequentialNQueensSolver(n)
        seq_solutions, seq_time = seq_solver.solve()
        print(f"Sequencial: {len(seq_solutions)} soluções encontradas em {seq_time:.4f} segundos")
        logger.log_result(n, "sequential", seq_solutions, seq_time)

        # Solução Paralela
        par_solver = ParallelNQueensSolver(n)
        par_solutions, par_time = par_solver.solve()
        print(f"Paralelo: {len(par_solutions)} soluções encontradas em {par_time:.4f} segundos")
        logger.log_result(n, "parallel", par_solutions, par_time)

        # Cálculo do speedup
        speedup = seq_time / par_time
        print(f"Speedup: {speedup:.2f}x")

    # Generate heatmaps after all solutions have been computed and logged
    if generate_heatmaps:
        heatmap_generator = NQueensHeatmapGenerator()
        log_file = logger.get_latest_log_file()
        heatmap_generator.generate_heatmaps(log_file)
        heatmap_generator.generate_combined_heatmap(log_file)

if __name__ == "__main__":
    main(generate_heatmaps=True)  # Set to False to disable heatmap generation