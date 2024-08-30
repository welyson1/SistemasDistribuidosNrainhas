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

    O problema pode ser resolvido pela pela propriedade das diagonais:

    A soma das coordenadas da diagonal da esquerda para a direita sempre são iguais a soma das coordenadas da rainha

    A soma das coordenadas da diagonal da direita para a esquerda sempre são iguai a subtração das coordenadas da rainha

    Ex: Diagonal esquerda para a direita

        -----------------
    0   |   |   |   |   |
    1   |   |   | X |   |   =>> Rainha (2,1) = 2 + 1 = 3
    2   |   | Q |   |   |       Diagonal superior direita => (1,2) = 1 + 2 = 3
    3   | X |   |   |   |       Diagonal inferior esquerda => (3,0) = 3 + 0 = 3
        -----------------
          0   1   2   3

        -----------------
    0   |   |   |   |   |
    1   | X |   |   |   |   =>> Rainha (2,1) = 2 - 1 = 1
    2   |   | Q |   |   |       Diagonal superior esquerda => (1,0) = 1 - 0 = 1
    3   |   |   | X |   |       Diagonal inferior direita => (3,2) = 3 - 2 = 1
        -----------------
          0   1   2   3
"""
import time


def solve_n_queens(n):
    """
        Cada índice representa uma linha, o valor representa a coluna da rainha
        Rainha na coluna 2 e linha 0 -> board[0] = 2
        Ex: n = 4 -> board = [ * , * , * , *]
    """

    board = ['*'] * n

    """
        columns = [] -> Lista de colunas ocupadas

        positive_diagonals = []  -> Lista de diagonais positivas ocupadas (linha + coluna)

        negative_diagonals = []  -> Conjunto de diagonais negativas ocupadas (linha - coluna)

        solutions = []  -> Lista para armazenar todas as soluções
    """

    columns = []
    positive_diagonals = []
    negative_diagonals = []
    solutions = []

    # Uma posição é segura se sua coluna e diagonais não estão ocupadas
    def valid_position(row, col):
        return col not in columns and row + col not in positive_diagonals and row - col not in negative_diagonals

    def place_queen(row):
        # Verifica se todas as rainhas foram posicionadas
        # TODO: ver pq dessa condição
        if row == n:
            # Se sim, adiciona a solução atual à lista de soluções
            solutions.append(board[:])
            return
        # Tenta colocar uma rainha em cada coluna da linha atual
        for col in range(n):
            # Verifica se a posição atual é segura
            if valid_position(row, col):
                # Posiciona a rainha
                board[row] = col

                # Marca a coluna e as diagonais como ocupadas
                columns.append(col)

                # Marca a diagonal positiva como ocupada
                positive_diagonals.append(row + col)

                # Marca a diagonal negativa como ocupada
                negative_diagonals.append(row - col)

                # Move para a próxima linha
                place_queen(row + 1)

                # Remove a marcação da coluna
                columns.pop()

                # Remove a marcação da diagonal positiva
                positive_diagonals.pop()

                # Remove a marcação da diagonal negativa
                negative_diagonals.pop()

    # Inicia o processo recursivo a partir da primeira linha
    place_queen(0)
    return solutions
