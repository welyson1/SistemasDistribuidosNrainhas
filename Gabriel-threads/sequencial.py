"""
    Pode-se representar o tabuleiro com 1 dimensão, reduzindo complexidade
    Ex 1:
    -----------------
    |   | Q |   |   |
    |   |   |   | Q |
    | Q |   |   |   |
    |   |   | Q |   |
    -----------------

    vetor que representa o tabuleiro [1, 3, 0, 2]

    Ex 2:
    -----------------
    |   |   | Q |   |
    | Q |   |   |   |
    |   |   |   | Q |
    |   | Q |   |   |
    -----------------

    vetor que representa o tabuleiro [2, 0, 3, 1]

"""

def safe_position(board, row, col, number_of_queens):
    # Check row on left side
    for i in range(col):
        if board[row][i] == 1:
            return False

    # Check upper diagonal on left side
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    # Check lower diagonal on left side
    for i, j in zip(range(row, number_of_queens, 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    return True


def resolve_backtrack(board, col, number_of_queens, solutions):
    if col == number_of_queens:
        solution = []
        for i in range(number_of_queens):
            for j in range(number_of_queens):
                if board[i][j] == 1:
                    solution.append(j)
        solutions.append(solution)
        return

    # tenta colocar uma rainha nas linhas da coluna
    for i in range(number_of_queens):
        if safe_position(board, i, col, number_of_queens):
            # coloca a rainha
            board[i][col] = 1
            # faz o 'backtracking' para colocar o resto das rainhas
            resolve_backtrack(board, col + 1, number_of_queens, solutions)
            # no 'backtrack' remove a rainha para tentar outras posições
            board[i][col] = 0


def resolve_n_queens(number_of_queens):

    # inicializa com zeros
    board = [[0 for _ in range(number_of_queens)] for _ in range(number_of_queens)]
    solutions = []

    # começa a resolver a partir da primeira coluna
    resolve_backtrack(board, 0, number_of_queens, solutions)
    return solutions


number_of_queens = 6
# condicionando de acordo com o número de rainhas
if number_of_queens >= 4:
    all_solutions = resolve_n_queens(number_of_queens)
    total_solutions = len(all_solutions)

    print(f"Número de soluções para {number_of_queens}-Queens: {total_solutions}")

    # se for maior que 10 soluções 'solutions' será 10
    solutions = min(total_solutions, 10)

    for i, solution in enumerate(all_solutions[:solutions], 1):
        print(f"Solução {i}: {solution}")
elif number_of_queens == 2 or number_of_queens == 3:
    print(f"Número de rainhas não possui soluções")
else:
    print(f"Número de rainhas possui apenas 1 solução")


