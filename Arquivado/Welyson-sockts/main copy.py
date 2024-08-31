import time
import threading
import matplotlib.pyplot as plt
import numpy as np
import os

# Função auxiliar para verificar se uma posição é segura
def posicao_segura(tabuleiro, linha, coluna):
    # Verifica esta linha à esquerda
    for i in range(coluna):
        if tabuleiro[linha][i] == 1:
            return False
    
    # Verifica a diagonal superior à esquerda
    for i, j in zip(range(linha, -1, -1), range(coluna, -1, -1)):
        if tabuleiro[i][j] == 1:
            return False

    # Verifica a diagonal inferior à esquerda
    for i, j in zip(range(linha, len(tabuleiro), 1), range(coluna, -1, -1)):
        if tabuleiro[i][j] == 1:
            return False

    return True

# Resolvedor sequencial de N Rainhas
def resolver_nrainhas_seq(tabuleiro, coluna, solucoes):
    if coluna >= len(tabuleiro):
        solucoes.append([''.join('Q' if cell else '.' for cell in row) for row in tabuleiro])
        return
    
    for i in range(len(tabuleiro)):
        if posicao_segura(tabuleiro, i, coluna):
            tabuleiro[i][coluna] = 1
            resolver_nrainhas_seq(tabuleiro, coluna + 1, solucoes)
            tabuleiro[i][coluna] = 0

def n_rainhas_sequencial(n):
    tabuleiro = [[0] * n for _ in range(n)]
    solucoes = []
    resolver_nrainhas_seq(tabuleiro, 0, solucoes)
    return solucoes

# Função para lidar com o trabalho de cada thread
def trabalhador_thread(n, coluna, tabuleiro, solucoes, lock):
    if coluna >= n:
        with lock:
            solucoes.append([''.join('Q' if cell else '.' for cell in row) for row in tabuleiro])
        return
    
    for i in range(n):
        if posicao_segura(tabuleiro, i, coluna):
            tabuleiro_copia = [row[:] for row in tabuleiro]  # Copia o tabuleiro
            tabuleiro_copia[i][coluna] = 1
            trabalhador_thread(n, coluna + 1, tabuleiro_copia, solucoes, lock)

def n_rainhas_paralelo(n):
    tabuleiro = [[0] * n for _ in range(n)]
    solucoes = []
    lock = threading.Lock()
    threads = []
    
    for i in range(n):
        tabuleiro_copia = [row[:] for row in tabuleiro]
        tabuleiro_copia[i][0] = 1
        thread = threading.Thread(target=trabalhador_thread, args=(n, 1, tabuleiro_copia, solucoes, lock))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

    return solucoes

def plotar_tabuleiro_realista(ax, tabuleiro, title):
    n = len(tabuleiro)
    # Criação do tabuleiro de xadrez
    tabuleiro_img = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if (i + j) % 2 == 0:
                tabuleiro_img[i, j] = 1  # Cor clara

    ax.imshow(tabuleiro_img, cmap='gray', interpolation='none')

    # Posicionar as rainhas
    for i in range(n):
        for j in range(n):
            if tabuleiro[i][j] == 1:
                ax.text(j, i, '♛', ha='center', va='center', fontsize=24, color='red')

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title)

def salvar_solucoes_lado_a_lado(solucoes_seq, solucoes_par, tempo_seq, tempo_par, pasta):
    if not os.path.exists(pasta):
        os.makedirs(pasta)
    
    n = len(solucoes_seq[0])
    num_solucoes = min(len(solucoes_seq), len(solucoes_par))
    
    for i in range(num_solucoes):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        tabuleiro_seq = [[1 if c == 'Q' else 0 for c in linha] for linha in solucoes_seq[i]]
        tabuleiro_par = [[1 if c == 'Q' else 0 for c in linha] for linha in solucoes_par[i]]
        
        plotar_tabuleiro_realista(ax1, tabuleiro_seq, f"Sequencial (Tempo: {tempo_seq:.4f}s)")
        plotar_tabuleiro_realista(ax2, tabuleiro_par, f"Paralelo (Tempo: {tempo_par:.4f}s)")
        
        plt.suptitle(f"Solução {i+1} para N-Rainhas (N={n})")
        
        filename = os.path.join(pasta, f"solucao_{i+1}.png")
        plt.savefig(filename)
        plt.close(fig)

# Testar e comparar soluções sequenciais e paralelas
n = 10  # Exemplo com N=8, pode ser ajustado para outros valores

# Executar soluções sequenciais e paralelas
start_time = time.time()
solucoes_seq = n_rainhas_sequencial(n)
tempo_seq = time.time() - start_time

start_time = time.time()
solucoes_par = n_rainhas_paralelo(n)
tempo_par = time.time() - start_time

# Verificar a correção
assert len(solucoes_seq) == len(solucoes_par), f"Divergência nas soluções para N={n}"

# Exibir informações sobre as soluções
print(f"Soluções para N={n}:")
print(f"Sequencial: {len(solucoes_seq)} soluções em {tempo_seq:.4f}s")
print(f"Paralelo: {len(solucoes_par)} soluções em {tempo_par:.4f}s")

# Salvar todas as soluções como imagens lado a lado
pasta_solucoes = "solucoes_n_rainhas_lado_a_lado"
salvar_solucoes_lado_a_lado(solucoes_seq, solucoes_par, tempo_seq, tempo_par, pasta_solucoes)

print(f"Todas as soluções foram salvas como imagens na pasta '{pasta_solucoes}'.")