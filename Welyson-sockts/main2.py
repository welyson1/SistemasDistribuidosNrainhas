import time
import threading
import matplotlib.pyplot as plt
import psutil  # Para monitorar o uso de CPU e outros recursos do sistema
import platform  # Para obter informações sobre o ambiente
from queue import Queue

# Helper function to check if a position is safe
def is_safe(board, row, col):
    # Check this row on the left side
    for i in range(col):
        if board[row][i] == 1:
            return False
    
    # Check upper diagonal on the left side
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    # Check lower diagonal on the left side
    for i, j in zip(range(row, len(board), 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    return True

# Sequential N-Queens solver
def solve_nqueens_seq(board, col, solutions):
    if col >= len(board):
        solutions.append([''.join('Q' if cell else '.' for cell in row) for row in board])
        return
    
    for i in range(len(board)):
        if is_safe(board, i, col):
            board[i][col] = 1
            solve_nqueens_seq(board, col + 1, solutions)
            board[i][col] = 0

def n_queens_sequential(n):
    board = [[0] * n for _ in range(n)]
    solutions = []
    solve_nqueens_seq(board, 0, solutions)
    return solutions

# Function to handle each thread's work
def thread_worker(n, col, board, solutions, lock):
    if col >= n:
        with lock:
            solutions.append([''.join('Q' if cell else '.' for cell in row) for row in board])
        return
    
    for i in range(n):
        if is_safe(board, i, col):
            board_copy = [row[:] for row in board]  # Copy the board
            board_copy[i][col] = 1
            thread_worker(n, col + 1, board_copy, solutions, lock)

def n_queens_parallel(n):
    board = [[0] * n for _ in range(n)]
    solutions = []
    lock = threading.Lock()
    threads = []
    
    thread_creation_start_time = time.time()

    for i in range(n):
        board_copy = [row[:] for row in board]
        board_copy[i][0] = 1
        thread = threading.Thread(target=thread_worker, args=(n, 1, board_copy, solutions, lock))
        threads.append(thread)
        thread.start()
    
    thread_creation_end_time = time.time()

    for thread in threads:
        thread.join()

    thread_join_end_time = time.time()

    return solutions, thread_creation_end_time - thread_creation_start_time, thread_join_end_time - thread_creation_end_time

# Test and compare sequential and parallel solutions
n_values = [4, 5, 6, 7, 8, 9, 10]
sequential_times = []
parallel_times = []
overhead_thread_creation = []
overhead_thread_join = []
cpu_usages_sequential = []
cpu_usages_parallel = []

# Get CPU count for environment information
cpu_count = psutil.cpu_count(logical=False)
cpu_count_logical = psutil.cpu_count(logical=True)
python_version = platform.python_version()

print(f"Environment: {cpu_count} physical CPUs, {cpu_count_logical} logical CPUs, Python {python_version}")

# Run tests and measure execution times
for n in n_values:
    print(f"Testing N={n}...")
    
    # Sequential execution
    start_time = time.time()
    cpu_percent_before = psutil.cpu_percent(interval=None)
    seq_solutions = n_queens_sequential(n)
    cpu_percent_after = psutil.cpu_percent(interval=None)
    seq_time = time.time() - start_time
    cpu_usage_seq = cpu_percent_after - cpu_percent_before
    sequential_times.append(seq_time)
    cpu_usages_sequential.append(cpu_usage_seq)
    
    # Parallel execution
    start_time = time.time()
    cpu_percent_before = psutil.cpu_percent(interval=None)
    par_solutions, thread_creation_time, thread_join_time = n_queens_parallel(n)
    cpu_percent_after = psutil.cpu_percent(interval=None)
    par_time = time.time() - start_time
    cpu_usage_par = cpu_percent_after - cpu_percent_before
    parallel_times.append(par_time)
    overhead_thread_creation.append(thread_creation_time)
    overhead_thread_join.append(thread_join_time)
    cpu_usages_parallel.append(cpu_usage_par)
    
    # Verify correctness
    assert len(seq_solutions) == len(par_solutions), f"Mismatch in solutions for N={n}"

# Plot the results

# Plot execution time comparison
plt.figure(figsize=(12, 6))

plt.subplot(2, 2, 1)
plt.plot(n_values, sequential_times, label='Sequential', marker='o')
plt.plot(n_values, parallel_times, label='Parallel', marker='o')
plt.xlabel('N (Número de Rainhas)')
plt.ylabel('Tempo de Execução (segundos)')
plt.title('Tempo de Execução: Sequencial vs Paralelo')
plt.legend()
plt.grid(True)

# Plot overhead comparison
plt.subplot(2, 2, 2)
plt.bar(n_values, overhead_thread_creation, width=0.4, label='Criação de Threads', align='center')
plt.bar([n + 0.4 for n in n_values], overhead_thread_join, width=0.4, label='Join de Threads', align='center')
plt.xlabel('N (Número de Rainhas)')
plt.ylabel('Tempo (segundos)')
plt.title('Overhead de Gerenciamento de Threads')
plt.legend()
plt.grid(True)

# Plot CPU usage comparison
plt.subplot(2, 2, 3)
plt.plot(n_values, cpu_usages_sequential, label='Uso de CPU Sequencial', marker='o')
plt.plot(n_values, cpu_usages_parallel, label='Uso de CPU Paralelo', marker='o')
plt.xlabel('N (Número de Rainhas)')
plt.ylabel('Uso de CPU (%)')
plt.title('Uso de CPU: Sequencial vs Paralelo')
plt.legend()
plt.grid(True)

# Plot execution time breakdown
plt.subplot(2, 2, 4)
plt.bar(n_values, sequential_times, width=0.4, label='Tempo Sequencial Total', align='center')
plt.bar([n + 0.4 for n in n_values], parallel_times, width=0.4, label='Tempo Paralelo Total', align='center')
plt.xlabel('N (Número de Rainhas)')
plt.ylabel('Tempo Total (segundos)')
plt.title('Comparação de Tempo de Execução Total')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()