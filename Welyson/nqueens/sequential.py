# sequential.py

from nqueens.solver import NQueensSolver
from typing import List, Tuple

class SequentialNQueensSolver(NQueensSolver):
    @NQueensSolver.measure_time
    def solve(self) -> Tuple[List[List[List[int]]], float]:
        """
        Resolve o problema das N-Rainhas de forma sequencial.

        :return: Tupla contendo a lista de soluções e o tempo de execução.
        """
        return super().solve()
