import multiprocessing
from typing import List, Tuple
from nqueens.solver import NQueensSolver

class ParallelNQueensSolver(NQueensSolver):
    def __init__(self, n: int):
        """
        Solucionador paralelo do problema das N-Rainhas.

        :param n: O tamanho do tabuleiro e o número de rainhas.
        """
        super().__init__(n)
        # Define o número de processos como o número de CPUs disponíveis
        # Isso permite utilizar eficientemente todos os núcleos do processador
        self.num_processes = multiprocessing.cpu_count()

    def solve_partial(self, start_row: int) -> List[List[List[int]]]:
        """
        Resolve o problema das N-Rainhas, começando com a primeira rainha em uma linha específica.

        1. Cada processo paralelo chama este método com um 'start_row' diferente.
        2. Isso divide o espaço total de soluções em subconjuntos não sobrepostos.
        3. Cada subconjunto representa todas as soluções possíveis começando com a primeira rainha em uma linha específica.

        Por exemplo, em um tabuleiro 4x4:
        - Processo 1: start_row = 0 (primeira rainha na primeira linha)
        - Processo 2: start_row = 1 (primeira rainha na segunda linha)
        - Processo 3: start_row = 2 (primeira rainha na terceira linha)
        - Processo 4: start_row = 3 (primeira rainha na quarta linha)

        Este método é usado para paralelização, onde cada processo começa de uma linha diferente.

        :param start_row: A linha inicial para colocar a primeira rainha (0 <= start_row < n).
        :return: Uma lista de soluções parciais encontradas para esta configuração inicial.
        """
        # Inicializa um tabuleiro vazio
        board = [[0 for _ in range(self.n)] for _ in range(self.n)]
        # Coloca a primeira rainha na linha de início, oque define o ponto de partida unico para este processo
        board[start_row][0] = 1
        partial_solutions = []
        # Inicia a resolução a partir da segunda coluna (indice 1) pois o indice 0 já está preenchida com a rainha inicial
        self.solve_util(board, 1, partial_solutions)
        return partial_solutions

    def solve_util(self, board: List[List[int]], col: int, partial_solutions: List[List[List[int]]]) -> bool:
        """
        Método auxiliar recursivo para resolver parcialmente o problema das N-Rainhas.
        Usa backtracking para explorar todas as possibilidades a partir de uma configuração inicial.

        Este método é chamado repetidamente pelo solve_partial para explorar todas as
        configurações possíveis do tabuleiro, começando da coluna especificada.

        :param board: O tabuleiro atual, com as rainhas já posicionadas nas colunas anteriores.
        :param col: A coluna atual sendo considerada para posicionar a próxima rainha.
        :param partial_solutions: Lista para armazenar as soluções parciais encontradas.
        :return: True se uma solução for encontrada, False caso contrário.
        """
        # Se todas as rainhas foram colocadas (chegamos à última coluna + 1), temos uma solução completa
        if col >= self.n:
            partial_solutions.append([row[:] for row in board])
            return True

        res = False
        # Tenta colocar a rainha em cada linha desta coluna
        for i in range(self.n):
            if self.is_safe(board, i, col):
                board[i][col] = 1 # Coloca a rainha nesta posição
                res = self.solve_util(board, col + 1, partial_solutions) or res # Recursivamente tenta colocar o resto das rainhas
                board[i][col] = 0  # Backtrack: remove a rainha desta posição para tentar outras

        return res

    @NQueensSolver.measure_time
    def solve(self) -> Tuple[List[List[List[int]]], float]:
        """
        Resolve o problema das N-Rainhas de forma paralela.
        Usa um pool de processos para distribuir o trabalho entre múltiplos cores da CPU.

        O método funciona da seguinte forma:
        1. Cria um pool de processos (um para cada núcleo da CPU).
        2. Divide o problema em N subproblemas (um para cada linha inicial possível).
        3. Distribui esses subproblemas entre os processos disponíveis.
        4. Cada processo resolve seu subproblema independentemente.
        5. Combina as soluções de todos os processos em uma lista final.

        :return: Uma tupla contendo a lista de todas as soluções encontradas e o tempo de execução.
        """
        # Cria um pool de processos para executar tarefas em paralelo
        with multiprocessing.Pool(processes=self.num_processes) as pool:
            # Distribui o trabalho entre os processos, cada um começando de uma linha diferente
            partial_solutions = pool.map(self.solve_partial, range(self.n))

        # Combina todas as soluções parciais em uma única lista
        self.solutions = [solution for sublist in partial_solutions for solution in sublist]
        return self.solutions