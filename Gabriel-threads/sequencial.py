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
import time


def is_position_valid(board, row, col, number_of_queens):
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
        if is_position_valid(board, i, col, number_of_queens):
            # coloca a rainha
            board[i][col] = 1
            # faz o 'backtracking' para colocar o resto das rainhas
            resolve_backtrack(board, col + 1, number_of_queens, solutions)
            # no 'backtrack' remove a rainha para tentar outras posições
            board[i][col] = 0


def initialize_board(number_of_queens):
    # inicializa tabuleiro com zeros
    # inicializar com um caracter como '.' ou '*' aumenta o tempo.
    return [[0] * number_of_queens for _ in range(number_of_queens)]


def resolve_n_queens(number_of_queens):
    board = initialize_board(number_of_queens)
    solutions = []

    # começa a resolver a partir da primeira coluna
    resolve_backtrack(board, 0, number_of_queens, solutions)
    return solutions


"""
    Para N igual a 1, temos apenas 1 solução
    Para N igual a 2 e 3, não existe solução
    
    Se verificado valores de N menores que 4, o tempo
    de execução aumenta ligeiramente
    
    A execução usando perf_counter(), process_time() and time()
    possuem resultados semalhantes.
"""

number_of_queens = [4, 5, 6, 7, 8, 9, 10, 11, 12]
# condicionando de acordo com o número da lista de rainhas
for queens in number_of_queens:
    if queens >= 4:
        time_start = time.perf_counter()

        all_solutions = resolve_n_queens(queens)
        total_solutions = len(all_solutions)

        end_time = time.perf_counter()
        exec_time = end_time - time_start

        print(f"Número de soluções para {queens}-Queens: {total_solutions}\n")
        print(f"Tempo de execução: {exec_time:.5f}s\n")

        # se for maior que 10 soluções 'solutions' será 10
        solutions = min(total_solutions, 10)

        for i, solution in enumerate(all_solutions[:solutions], 1):
            print(f"Solução {i}: {solution}")
        print("\n")


