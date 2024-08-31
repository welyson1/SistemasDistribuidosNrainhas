import time
from n_queens_solver import solve_n_queens


def sequencial_solve(number_of_queens):

    """
        start_time -> inicia a contagem do tempo
        
        all_solution -> chama a função principal
        
        end_time -> finaliza a contagem do tempo a contagem do tempo
        
        *Obs: Foi optado por utilizar perf_counter pois é mais indicado para benchmarks
        porém não foi observado grandes diferenças entre outros métodos de medição de tempo
        de execução como o time() e o process_time()
    """

    start_time_sequencial = time.perf_counter()
    all_solutions_sequencial = solve_n_queens(number_of_queens)
    end_time_sequencial = time.perf_counter()
    exec_time_sequencial = end_time_sequencial - start_time_sequencial

    return all_solutions_sequencial, exec_time_sequencial
