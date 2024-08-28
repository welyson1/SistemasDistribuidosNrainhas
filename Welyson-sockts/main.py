import time
import threading
import matplotlib.pyplot as plt
import numpy as np

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

# Função para plotar um tabuleiro de damas realista
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

# Função para plotar as soluções lado a lado
def plotar_solucoes_lado_a_lado(sol_sequencial, sol_paralelo, tempo_seq, tempo_par):
    n = len(sol_sequencial)
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    # Converter a solução para um tabuleiro 2D de inteiros
    tabuleiro_seq = [[1 if c == 'Q' else 0 for c in linha] for linha in sol_sequencial]
    tabuleiro_par = [[1 if c == 'Q' else 0 for c in linha] for linha in sol_paralelo]

    plotar_tabuleiro_realista(axs[0], tabuleiro_seq, f'Sequencial (Tempo: {tempo_seq:.4f}s)')
    plotar_tabuleiro_realista(axs[1], tabuleiro_par, f'Paralelo (Tempo: {tempo_par:.4f}s)')

    plt.show()

# Testar e comparar soluções sequenciais e paralelas
n = 10  # Exemplo com N=8, pode ser ajustado para outros valores
tempos_sequenciais = []
tempos_paralelos = []

# Executar teste para um único valor de N e medir tempos de execução
start_time = time.time()
solucoes_seq = n_rainhas_sequencial(n)
tempo_seq = time.time() - start_time
tempos_sequenciais.append(tempo_seq)

start_time = time.time()
solucoes_par = n_rainhas_paralelo(n)
tempo_par = time.time() - start_time
tempos_paralelos.append(tempo_par)

# Verificar a correção
assert len(solucoes_seq) == len(solucoes_par), f"Divergência nas soluções para N={n}"

# Exibir soluções e tempos de execução lado a lado
print("Exemplo de Soluções para N=8:")
print(f"Soluções Sequencial: {len(solucoes_seq)} em {tempo_seq:.4f}s")
print(f"Soluções Paralelo: {len(solucoes_par)} em {tempo_par:.4f}s")

# Plotar as primeiras soluções para visualização lado a lado
plotar_solucoes_lado_a_lado(solucoes_seq[0], solucoes_par[0], tempo_seq, tempo_par)

# Exibir gráficos de tempo de execução para diferentes valores de N
n_values = [4, 5, 6, 7, 8, 9, 10]
tempos_sequenciais = []
tempos_paralelos = []

for n in n_values:
    start_time = time.time()
    solucoes_seq = n_rainhas_sequencial(n)
    tempo_seq = time.time() - start_time
    tempos_sequenciais.append(tempo_seq)

    start_time = time.time()
    solucoes_par = n_rainhas_paralelo(n)
    tempo_par = time.time() - start_time
    tempos_paralelos.append(tempo_par)

    # Verificar a correção
    assert len(solucoes_seq) == len(solucoes_par), f"Divergência nas soluções para N={n}"

# Plotar o resultado de tempo de execução
plt.plot(n_values, tempos_sequenciais, label='Sequencial', marker='o')
plt.plot(n_values, tempos_paralelos, label='Paralelo', marker='o')
plt.xlabel('N (Número de Rainhas)')
plt.ylabel('Tempo de Execução (segundos)')
plt.title('Tempo de Execução: N-Rainhas Sequencial vs Paralelo')
plt.legend()
plt.grid(True)
plt.show()
