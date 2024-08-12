import threading
import time

class QueenThread(threading.Thread):
    def __init__(self, n, id):
        threading.Thread.__init__(self)
        self.n = n
        self.id = id
        print(f"Thread {id} criada para resolver o problema de N rainhas com tamanho de tabuleiro {n}")

    def run(self):
        print(f"Thread {self.id} iniciando a resolucao do problema de N rainhas...")
        start_time = time.time()

        # Inicializa o tabuleiro
        board = [-1] * self.n
        print(f"Tabuleiro inicializado com tamanho {self.n}")

        # Inicializa a solução
        solutions = []
        print(f"Lista de solucoes inicializada")

        # Função para verificar se uma rainha pode ser colocada em uma posição específica
        def is_safe(board, row, col):
            for i in range(row):
                if board[i] == col or board[i] - i == col - row or board[i] + i == col + row:
                    return False
            return True

        # Função para resolver o problema de N rainhas
        def solve(board, row):
            if row == self.n:
                # Encontrou uma solução
                solutions.append(board[:])
                print(f"Solucao encontrada: {board}")
            else:
                for col in range(self.n):
                    if is_safe(board, row, col):
                        board[row] = col
                        print(f"Colocando rainha em posicao ({row}, {col})")
                        solve(board, row + 1)

        # Resolve o problema de N rainhas
        solve(board, 0)
        print(f"Resolucao do problema de N rainhas concluida")

        # Imprime as soluções
        print(f"Solucoes encontradas pela thread {self.id}:")
        for solution in solutions:
            print(solution)

        end_time = time.time()
        print(f"Tempo de execucao da thread {self.id}: {end_time - start_time:.2f}s")

# Cria e inicia as threads
n = 4
threads = []
for i in range(n):
    thread = QueenThread(n, i)
    thread.start()
    threads.append(thread)

# Espera pelas threads terminarem
for thread in threads:
    thread.join()