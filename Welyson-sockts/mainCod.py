import time
import threading
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

# Function to animate the board
def animate_solutions(moves, n, ax, title):
    board = [[0] * n for _ in range(n)]

    def update(frame):
        i, col, place = moves[frame]
        board[i][col] = 1 if place else 0
        ax.clear()
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title)
        ax.imshow(board, cmap='binary')
        
        # Highlighting lines being updated
        if place:
            ax.axhline(y=i, color='red', linestyle='--', linewidth=2)
            ax.axvline(x=col, color='red', linestyle='--', linewidth=2)
    
    return animation.FuncAnimation(plt.gcf(), update, frames=len(moves), interval=300)

# Test and compare sequential and parallel solutions
n = 8  # Change N value to test other sizes

# Sequential solution and animation
start_time = time.time()
seq_solutions, seq_moves = n_queens_sequential(n)
seq_time = time.time() - start_time

# Parallel solution and animation
start_time = time.time()
par_solutions, par_moves = n_queens_parallel(n)
par_time = time.time() - start_time

# Plotting
fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# Sequential animation
anim_seq = animate_solutions(seq_moves, n, axs[0], f'Sequential - Time: {seq_time:.4f}s')

# Parallel animation
anim_par = animate_solutions(par_moves, n, axs[1], f'Parallel - Time: {par_time:.4f}s')

# Show the animation
plt.tight_layout()
plt.show()
