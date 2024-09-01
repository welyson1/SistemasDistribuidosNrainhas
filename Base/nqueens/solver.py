import time
from typing import List, Tuple

class NQueensSolver:
    def __init__(self, n: int):
        """
        Inicializa o solucionador do problema das N-Rainhas.
        :param n: tamanho do tabuleiro e o número de rainhas.
        """
        self.n = n  # Tamanho do tabuleiro
        self.solutions = []  # Lista para armazenar todas as soluções encontradas

    def is_safe(self, board: List[List[int]], row: int, col: int) -> bool:
        """
        Verifica se é seguro colocar uma rainha na posição (linha, coluna).
        Este método é chamado toda vez que o algoritmo tenta colocar uma nova rainha no tabuleiro.

        :param board: O tabuleiro atual, representado como uma lista de listas.
        :param row: A linha onde se deseja colocar a rainha.
        :param col: A coluna onde se deseja colocar a rainha.
        :return: True se for seguro colocar a rainha, False caso contrário.
        """
        # Verifica a linha a esquerda
        for i in range(col):
            if board[row][i] == 1:  # Se encontrar uma rainha (representada por 1)
                return False  # Nao é seguro, há uma rainha na mesma linha

        # Verifica a diagonal superior esquerda
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 1:  # Se encontrar uma rainha
                return False  # Não é seguro, há uma rainha na diagonal superior

        # Verifica a diagonal inferior esquerda
        for i, j in zip(range(row, self.n, 1), range(col, -1, -1)):
            if board[i][j] == 1:  # Se encontrar uma rainha
                return False  # Não é seguro, há uma rainha na diagonal inferior

        return True  # É seguro colocar a rainha nesta posição

    def solve_util(self, board: List[List[int]], col: int) -> bool:
        """
        Método auxiliar recursivo para resolver o problema das N-Rainhas.
        Utiliza a técnica de backtracking para encontrar todas as soluções possíveis.

        :param board: O tabuleiro atual.
        :param col: A coluna atual sendo considerada.
        :return: True se uma solução for encontrada, False caso contrário.
        """
        # Caso base: se todas as rainhas foram colocadas, temos uma solução
        if col >= self.n:
            self.solutions.append([row[:] for row in board])
            return True

        res = False
        # Tenta colocar a rainha em cada linha desta coluna
        for i in range(self.n):
            if self.is_safe(board, i, col):
                # Coloca a rainha nesta posição
                board[i][col] = 1
                # Move para a próxima coluna
                res = self.solve_util(board, col + 1) or res
                # Backtrack: remove a rainha desta posição
                board[i][col] = 0

        return res

    def solve(self) -> List[List[List[int]]]:
        """
        Resolve o problema das N-Rainhas.

        :return: Uma lista de todas as soluções encontradas.
        """
        # Inicializa um tabuleiro vazio
        board = [[0 for _ in range(self.n)] for _ in range(self.n)]
        # Inicia o processo de solução a partir da primeira coluna
        self.solve_util(board, 0)
        # Retorna todas as soluções encontradas
        return self.solutions

    @staticmethod
    def measure_time(func):
        """
        Para medir o tempo de execução de uma função.

        :param func: A função a ser medida.
        :return: Uma tupla contendo o resultado da função e o tempo de execução.
        """
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            return result, end_time - start_time
        return wrapper