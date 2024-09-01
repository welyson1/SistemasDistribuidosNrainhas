# main.py
from nqueens.sequential import SequentialNQueensSolver
from nqueens.parallel import ParallelNQueensSolver
from nqueens.logger import NQueensLogger
from nqueens.image_generator import NQueensHeatmapGenerator

def main(generate_heatmaps=True):
    logger = NQueensLogger()
    n_values = [4, 6, 8, 10, 12, 13] # Tamanhos do tabuleiro para resolver o problema das N-Rainhas [4, 6, 8, 10, 12, 13]

    for n in n_values:
        print(f"\nResolvendo o problema das {n}-Rainhas:") 

        # Solução Sequencial
        seq_solver = SequentialNQueensSolver(n) # Instancia o solver sequencial
        seq_solutions, seq_time = seq_solver.solve() # Resolve o problema e mede o tempo de execução
        print(f"Sequencial: {len(seq_solutions)} soluções encontradas em {seq_time:.4f} segundos") 
        logger.log_result(n, "Sequencial", seq_solutions, seq_time) # Registra os resultados no arquivo de log

        # Solução Paralela
        par_solver = ParallelNQueensSolver(n) # Instancia o solver paralelo
        par_solutions, par_time = par_solver.solve() # Resolve o problema e mede o tempo de execução
        print(f"Paralelo: {len(par_solutions)} soluções encontradas em {par_time:.4f} segundos")
        logger.log_result(n, "Paralelo", par_solutions, par_time) # Registra os resultados no arquivo de log

        # Cálculo do speedup
        speedup = seq_time / par_time # Calcula o speedup como a razão entre o tempo sequencial e o tempo paralelo
        print(f"Speedup: {speedup:.2f}x")

    # Gerar mapas de calor depois que todas as soluções forem computadas e registradas
    if generate_heatmaps:
        heatmap_generator = NQueensHeatmapGenerator() # Instancia o gerador de mapas de calor
        log_file = logger.get_latest_log_file() # Obtém o caminho do arquivo de log mais recente
        heatmap_generator.generate_heatmaps(log_file) # Gera mapas de calor para cada entrada no arquivo de log
        heatmap_generator.generate_combined_heatmap(log_file) # Gera um mapa de calor combinado para todas as entradas

if __name__ == "__main__":
    main(generate_heatmaps=True)  # Defina como False para desabilitar a geração de mapa de calor