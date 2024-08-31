import itertools

def is_safe(board):
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == j - i:
                return False
    return True

def solve_n_queens_brute_force(n):
    solutions = []
    for perm in itertools.permutations(range(n)):
        if is_safe(perm):
            solutions.append(perm)
    return solutions

def print_solution(solution):
    n = len(solution)
    for row in solution:
        line = ['Q' if i == row else '.' for i in range(n)]
        print(' '.join(line))
    print()

# Exemplo de uso
n = 10
solutions = solve_n_queens_brute_force(n)
print(f"Número de soluções encontradas: {len(solutions)}")
print("Primeira solução:")
print_solution(solutions[0])