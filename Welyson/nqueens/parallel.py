# parallel.py

import multiprocessing
from typing import List, Tuple
from nqueens.solver import NQueensSolver

class ParallelNQueensSolver(NQueensSolver):
    def __init__(self, n: int):
        super().__init__(n)
        self.num_processes = multiprocessing.cpu_count()

    def solve_partial(self, start_row: int) -> List[List[List[int]]]:
        """
        Resolve parcialmente o problema das N-Rainhas, começando de uma linha específica.

        :param start_row: Linha inicial para colocar a primeira rainha.
        :return: Lista de soluções parciais.
        """
        board = [[0 for _ in range(self.n)] for _ in range(self.n)]
        board[start_row][0] = 1
        partial_solutions = []
        self.solve_util(board, 1, partial_solutions)
        return partial_solutions

    def solve_util(self, board: List[List[int]], col: int, partial_solutions: List[List[List[int]]]) -> bool:
        """
        Função de utilidade recursiva para resolver parcialmente o problema das N-Rainhas.

        :param board: Tabuleiro atual.
        :param col: Coluna atual sendo considerada.
        :param partial_solutions: Lista para armazenar soluções parciais.
        :return: True se uma solução for encontrada, False caso contrário.
        """
        if col >= self.n:
            partial_solutions.append([row[:] for row in board])
            return True

        res = False
        for i in range(self.n):
            if self.is_safe(board, i, col):
                board[i][col] = 1
                res = self.solve_util(board, col + 1, partial_solutions) or res
                board[i][col] = 0  # Backtrack

        return res

    @NQueensSolver.measure_time
    def solve(self) -> Tuple[List[List[List[int]]], float]:
        """
        Resolve o problema das N-Rainhas de forma paralela.

        :return: Tupla contendo a lista de soluções e o tempo de execução.
        """
        with multiprocessing.Pool(processes=self.num_processes) as pool:
            partial_solutions = pool.map(self.solve_partial, range(self.n))

        self.solutions = [solution for sublist in partial_solutions for solution in sublist]
        return self.solutions