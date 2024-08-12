import socket
import threading
import pickle
import logging
import sys
import time

# Configuração de logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Coordenador:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.workers = []
        self.solucoes = []
        self.lock = threading.Lock()

    def handle_worker(self, conn, addr):
        logging.info(f"Tratando o worker {addr}")
        try:
            data = conn.recv(4096)
            if not data:
                logging.warning(f"Nenhum dado recebido do worker {addr}")
                return
            
            board = pickle.loads(data)
            logging.debug(f"Dados recebidos do worker {addr}: {board}")

            if board:
                with self.lock:
                    self.solucoes.append(board)
                    logging.info(f"Funcionalidade: Solução adicionada por {addr}, total de soluções: {len(self.solucoes)}")
            else:
                logging.warning(f"Nenhuma solução encontrada pelo worker {addr}")
        except Exception as e:
            logging.error(f"Erro ao tratar o worker {addr}: {e}")
        finally:
            conn.close()
            logging.info(f"Conexão encerrada com {addr}")

    def iniciar(self, n):
        logging.info(f"Iniciando coordenador em {self.host}:{self.port} para N={n}")
        start_time = time.time()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            logging.info(f"Aguardando conexões em {self.host}:{self.port}")

            for i in range(n):
                conn, addr = s.accept()
                self.workers.append((conn, addr))
                logging.info(f"Worker conectado: {addr}")

                board = [[0] * n for _ in range(n)]
                board[i][0] = 1
                conn.sendall(pickle.dumps(board))
                logging.debug(f"Tarefa inicial enviada para {addr}: {board}")

            for conn, addr in self.workers:
                threading.Thread(target=self.handle_worker, args=(conn, addr)).start()

            for t in threading.enumerate():
                if t != threading.current_thread():
                    t.join()

        end_time = time.time()
        elapsed_time = end_time - start_time

        logging.info("Coordenador finalizou todas as tarefas")
        logging.info(f"Eficiência: Tempo de execução da solução paralela: {elapsed_time:.2f} segundos")
        logging.info(f"Funcionalidade: Total de Soluções Encontradas: {len(self.solucoes)}")
        logging.info(f"Escalabilidade: Soluções encontradas para N={n}")
        return self.solucoes

if __name__ == "__main__":
    n = 8
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 12345
    coordenador = Coordenador(port=port)
    solucoes = coordenador.iniciar(n)
    
    logging.info(f"Resumo Final das Soluções para N={n}:")
    for solucao in solucoes:
        for linha in solucao:
            logging.debug(linha)
        logging.info("Solução impressa\n")
