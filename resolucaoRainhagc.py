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

def solve_n_queens_util(board, col, n):
    if col >= n:
        return True
    for i in range(n):
        if is_safe(board, i, col, n):
            board[i][col] = 1
            if solve_n_queens_util(board, col + 1, n):
                return True
            board[i][col] = 0
    return False

def solve_n_queens_sequential(n):
    board = [[0 for _ in range(n)] for _ in range(n)]
    if solve_n_queens_util(board, 0, n):
        return board
    return None

def solve_n_queens_worker(start_row, n, result_queue):
    board = [[0 for _ in range(n)] for _ in range(n)]
    board[start_row][0] = 1
    if solve_n_queens_util(board, 1, n):
        result_queue.put(board)
    else:
        result_queue.put(None)

def solve_n_queens_threaded(n, num_threads):
    threads = []
    result_queue = Queue()

    for i in range(min(n, num_threads)):
        thread = threading.Thread(target=solve_n_queens_worker, args=(i, n, result_queue))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    while not result_queue.empty():
        result = result_queue.get()
        if result:
            return result

    return None

def print_solution(board):
    if board:
        for row in board:
            print(" ".join(map(str, row)))
    else:
        print("Solução não encontrada")

def benchmark(func, n, num_runs=5, **kwargs):
    total_time = 0
    for _ in range(num_runs):
        start_time = time.perf_counter()
        solution = func(n, **kwargs)
        end_time = time.perf_counter()
        total_time += end_time - start_time
    
    avg_time = total_time / num_runs
    return solution, avg_time

def main():
    n_values = [4, 8, 12, 16, 20]
    num_threads = multiprocessing.cpu_count() 
    
    print(f"Comparação entre Implementações Sequencial e Threaded (usando {num_threads} threads)")
    print("=" * 80)
    
    for n in n_values:
        print(f"\nN = {n}")
        print("-" * 10)
        
        # Versão Sequencial
        seq_solution, seq_time = benchmark(solve_n_queens_sequential, n)
        print(f"Tempo médio (Sequencial): {seq_time:.6f} segundos")
        
        # Versão Threaded
        thread_solution, thread_time = benchmark(solve_n_queens_threaded, n, num_threads=num_threads)
        print(f"Tempo médio (Threaded)  : {thread_time:.6f} segundos")
        
        if thread_time > 0:
            speedup = seq_time / thread_time
            print(f"Speedup                : {speedup:.2f}x")
        else:
            print("Speedup                : N/A (tempo muito pequeno para medir)")
        
        # Imprime a solução encontrada
        print("\nSolução encontrada (Threaded):")
        print_solution(thread_solution)

if __name__ == "__main__":
    main()