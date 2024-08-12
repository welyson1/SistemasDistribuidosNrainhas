import socket
import pickle
import logging
import sys
import time

# Configuração de logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Worker:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port

    def is_safe(self, board, row, col):
        for i in range(col):
            if board[row][i] == 1:
                return False
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        for i, j in zip(range(row, len(board), 1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        return True

    def solve_n_queens_util(self, board, col):
        if col >= len(board):
            logging.info("Funcionalidade: Solução encontrada!")
            return True
        for i in range(len(board)):
            if self.is_safe(board, i, col):
                board[i][col] = 1
                logging.debug(f"Rainha posicionada em ({i}, {col})")
                if self.solve_n_queens_util(board, col + 1):
                    return True
                board[i][col] = 0
                logging.debug(f"Rainha removida de ({i}, {col})")
        return False

    def run(self):
        logging.info(f"Worker conectando ao coordenador em {self.host}:{self.port}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            logging.info(f"Conectado ao coordenador em {self.host}:{self.port}")

            data = s.recv(4096)
            if not data:
                logging.warning("Nenhum dado recebido do coordenador")
                return

            board = pickle.loads(data)
            logging.debug(f"Tarefa recebida: {board}")

            start_time = time.time()
            if self.solve_n_queens_util(board, 1):
                s.sendall(pickle.dumps(board))
                logging.info("Funcionalidade: Solução enviada ao coordenador")
            else:
                s.sendall(pickle.dumps(None))
                logging.info("Funcionalidade: Nenhuma solução encontrada, enviado None ao coordenador")
            end_time = time.time()
            elapsed_time = end_time - start_time
            logging.info(f"Eficiência: Tempo gasto pelo worker: {elapsed_time:.2f} segundos")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 12345
    worker = Worker(port=port)
    worker.run()
