import time
import threading
from queue import Queue
import multiprocessing

def is_safe(board, row, col, n):
    for i in range(col):
        if board[row][i] == 1:
            return False
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    for i, j in zip(range(row, n, 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    return True

def solve_n_queens_util(board, col, n, solutions):
    if col >= n:
        solutions.append([row[:] for row in board])
        return
    for i in range(n):
        if is_safe(board, i, col, n):
            board[i][col] = 1
            solve_n_queens_util(board, col + 1, n, solutions)
            board[i][col] = 0

def solve_n_queens_sequential(n):
    board = [[0 for _ in range(n)] for _ in range(n)]
    solutions = []
    solve_n_queens_util(board, 0, n, solutions)
    return solutions

def solve_n_queens_worker(start_row, n, result_queue):
    board = [[0 for _ in range(n)] for _ in range(n)]
    board[start_row][0] = 1
    solutions = []
    solve_n_queens_util(board, 1, n, solutions)
    result_queue.put(solutions)

def solve_n_queens_threaded(n, num_threads):
    threads = []
    result_queue = Queue()
    solutions = []

    for i in range(min(n, num_threads)):
        thread = threading.Thread(target=solve_n_queens_worker, args=(i, n, result_queue))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    while not result_queue.empty():
        solutions.extend(result_queue.get())

    return solutions

def print_solutions(solutions):
    if solutions:
        for idx, solution in enumerate(solutions):
            print(f"Solução {idx + 1}:")
            for row in solution:
                print(" ".join(map(str, row)))
            print()
    else:
        print("Nenhuma solução encontrada")

def benchmark(func, n, num_runs=5, **kwargs):
    total_time = 0
    for _ in range(num_runs):
        start_time = time.perf_counter()
        solutions = func(n, **kwargs)
        end_time = time.perf_counter()
        total_time += end_time - start_time
    
    avg_time = total_time / num_runs
    return solutions, avg_time

def main():
    n = int(input("Digite o valor de N para o problema das N-Rainhas: "))
    num_threads = multiprocessing.cpu_count()
    
    print(f"\nComparação entre Implementações Sequencial e Threaded (usando {num_threads} threads)")
    print("=" * 80)
    
    # Versão Sequencial
    seq_solutions, seq_time = benchmark(solve_n_queens_sequential, n)
    print(f"Tempo médio (Sequencial): {seq_time:.6f} segundos")
    
    # Versão Threaded
    thread_solutions, thread_time = benchmark(solve_n_queens_threaded, n, num_threads=num_threads)
    print(f"Tempo médio (Threaded)  : {thread_time:.6f} segundos")
    
    if thread_time > 0:
        speedup = seq_time / thread_time
        print(f"Speedup                : {speedup:.2f}x")
    else:
        print("Speedup                : N/A (tempo muito pequeno para medir)")
    
    # Imprime as soluções encontradas (Threaded)
    print("\nSoluções encontradas (Threaded):")
    print_solutions(thread_solutions)

if __name__ == "__main__":
    main()
