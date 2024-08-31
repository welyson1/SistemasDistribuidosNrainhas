import time
import threading
from queue import Queue
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Helper function to check if a position is safe
def is_safe(board, row, col):
    for i in range(col):
        if board[row][i] == 1:
            return False
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    for i, j in zip(range(row, len(board), 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    return True

# Sequential N-Queens solver with animation
def solve_nqueens_seq(board, col, solutions, moves):
    if col >= len(board):
        solutions.append([''.join('Q' if cell else '.' for cell in row) for row in board])
        return
    for i in range(len(board)):
        if is_safe(board, i, col):
            board[i][col] = 1
            moves.append((i, col, True))
            solve_nqueens_seq(board, col + 1, solutions, moves)
            board[i][col] = 0
            moves.append((i, col, False))

def n_queens_sequential(n):
    board = [[0] * n for _ in range(n)]
    solutions = []
    moves = []
    solve_nqueens_seq(board, 0, solutions, moves)
    return solutions, moves

# Function to handle each thread's work
def thread_worker(n, col, board, solutions, lock, moves):
    if col >= n:
        with lock:
            solutions.append([''.join('Q' if cell else '.' for cell in row) for row in board])
        return
    for i in range(n):
        if is_safe(board, i, col):
            board_copy = [row[:] for row in board]
            board_copy[i][col] = 1
            with lock:
                moves.append((i, col, True))
            thread_worker(n, col + 1, board_copy, solutions, lock, moves)
            with lock:
                moves.append((i, col, False))

def n_queens_parallel(n):
    board = [[0] * n for _ in range(n)]
    solutions = []
    moves = []
    lock = threading.Lock()
    threads = []
    for i in range(n):
        board_copy = [row[:] for row in board]
        board_copy[i][0] = 1
        thread = threading.Thread(target=thread_worker, args=(n, 1, board_copy, solutions, lock, moves))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    return solutions, moves

# Function to animate the board with code execution
def animate_solutions(moves, n, ax, code_ax, title, code_lines):
    board = [[0] * n for _ in range(n)]

    def update(frame):
        i, col, place = moves[frame]
        board[i][col] = 1 if place else 0
        ax.clear()
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title)
        ax.imshow(board, cmap='binary')

        code_ax.clear()
        code_ax.set_xticks([])
        code_ax.set_yticks([])
        code_ax.set_title('Code Execution')
        code_ax.text(0.5, 0.5, code_lines[frame], fontsize=12, ha='center', va='center', wrap=True)

    return animation.FuncAnimation(plt.gcf(), update, frames=len(moves), interval=300)

# Generate code lines for animation
def generate_code_lines(moves, n):
    code_lines = []
    for i, (row, col, place) in enumerate(moves):
        if place:
            code_lines.append(f"Placing queen at ({row}, {col})")
        else:
            code_lines.append(f"Removing queen from ({row}, {col})")
    return code_lines

# Test and compare sequential and parallel solutions
n = 8  # Change N value to test other sizes

# Sequential solution and animation
start_time = time.time()
seq_solutions, seq_moves = n_queens_sequential(n)
seq_time = time.time() - start_time
seq_code_lines = generate_code_lines(seq_moves, n)

# Parallel solution and animation
start_time = time.time()
par_solutions, par_moves = n_queens_parallel(n)
par_time = time.time() - start_time
par_code_lines = generate_code_lines(par_moves, n)

# Plotting
fig, axs = plt.subplots(2, 2, figsize=(16, 12))

# Sequential animation
anim_seq = animate_solutions(seq_moves, n, axs[0, 0], axs[0, 1], f'Sequential - Time: {seq_time:.4f}s', seq_code_lines)

# Parallel animation
anim_par = animate_solutions(par_moves, n, axs[1, 0], axs[1, 1], f'Parallel - Time: {par_time:.4f}s', par_code_lines)

# Show the animation
plt.tight_layout()
plt.show()
