from nqueens.solver import NQueensSolver
from typing import List, Tuple

class SequentialNQueensSolver(NQueensSolver):
    """
    Implementação sequencial do solucionador do problema das N-Rainhas.
    Esta classe herda da classe base NQueensSolver e sobrescreve apenas o método solve().
    """

    @NQueensSolver.measure_time
    def solve(self) -> Tuple[List[List[List[int]]], float]:
        """
        Resolve o problema das N-Rainhas de forma sequencial.

        Este método é decorado com uma lógica que mede o tempo de execução.

        :return: Uma tupla contendo:
                 - Uma lista de todas as soluções encontradas (cada solução é uma lista de listas de inteiros)
                 - O tempo de execução em segundos (float)
        """
        # Chama o método solve() da classe (NQueensSolver)
        # A implementação sequencial simplesmente utiliza a lógica da classe base
        return super().solve()