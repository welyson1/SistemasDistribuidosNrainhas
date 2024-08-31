import time
import multiprocessing
from n_queens_solver import solve_n_queens


def worker(number_of_queens):
    return solve_n_queens(number_of_queens)


def paralelo_solver(number_of_queens):

    start_time_paralelo = time.perf_counter()
    with multiprocessing.Pool() as pool:
        all_solutions_paralelo = pool.apply(worker, (number_of_queens,))
    end_time_paralelo = time.perf_counter()
    exec_time_paralelo = end_time_paralelo - start_time_paralelo
    return all_solutions_paralelo, exec_time_paralelo
