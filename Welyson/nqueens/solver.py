# solver.py

import time
from typing import List, Tuple

class NQueensSolver:
    def __init__(self, n: int):
        """
        Inicializa o solucionador do problema das N-Rainhas.

        :param n: Número de rainhas e tamanho do tabuleiro.
        """
        self.n = n
        self.solutions = []

    def is_safe(self, board: List[List[int]], row: int, col: int) -> bool:
        """
        Verifica se é seguro colocar uma rainha na posição (row, col).

        :param board: Tabuleiro atual.
        :param row: Linha a ser verificada.
        :param col: Coluna a ser verificada.
        :return: True se for seguro, False caso contrário.
        """
        # Verifica a linha à esquerda
        for i in range(col):
            if board[row][i] == 1:
                return False

        # Verifica a diagonal superior esquerda
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False

        # Verifica a diagonal inferior esquerda
        for i, j in zip(range(row, self.n, 1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False

        return True

    def solve_util(self, board: List[List[int]], col: int) -> bool:
        """
        Função de utilidade recursiva para resolver o problema das N-Rainhas.

        :param board: Tabuleiro atual.
        :param col: Coluna atual sendo considerada.
        :return: True se uma solução for encontrada, False caso contrário.
        """
        if col >= self.n:
            self.solutions.append([row[:] for row in board])
            return True

        res = False
        for i in range(self.n):
            if self.is_safe(board, i, col):
                board[i][col] = 1
                res = self.solve_util(board, col + 1) or res
                board[i][col] = 0  # Backtrack

        return res

    def solve(self) -> List[List[List[int]]]:
        """
        Resolve o problema das N-Rainhas.

        :return: Lista de todas as soluções encontradas.
        """
        board = [[0 for _ in range(self.n)] for _ in range(self.n)]
        self.solve_util(board, 0)
        return self.solutions

    @staticmethod
    def measure_time(func):
        """
        Decorador para medir o tempo de execução de uma função.

        :param func: Função a ser medida.
        :return: Tupla contendo o resultado da função e o tempo de execução.
        """
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            return result, end_time - start_time
        return wrapper