# image_generator.py
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class NQueensHeatmapGenerator:
    def __init__(self):
        self.img_dir = "./Welyson/heatmaps"  # Diretório onde as imagens dos heatmaps serão salvas

    def generate_heatmaps(self, log_file):
        # Lê o arquivo de log e carrega os dados JSON de cada linha
        with open(log_file, 'r') as f:
            log_data = [json.loads(line) for line in f]

        # Para cada entrada nos dados de log, gera um heatmap correspondente
        for entry in log_data:
            n = entry['n']  # Tamanho do tabuleiro (n x n)
            solver_type = entry['solver_type']  # Tipo de solver utilizado
            solutions = entry['solutions']  # Lista de soluções para o problema das N-Rainhas
            time = entry['time']  # Tempo gasto para encontrar as soluções

            self._generate_heatmap(n, solver_type, solutions, time)

    def _generate_heatmap(self, n, solver_type, solutions, time):
        # Inicializa uma matriz de zeros para armazenar a contagem de soluções para cada posição no tabuleiro
        heatmap_data = np.zeros((n, n))
        
        # Incrementa a contagem na posição correspondente do tabuleiro para cada rainha em cada solução
        for solution in solutions:
            for row in range(n):
                for col in range(n):
                    if solution[row][col] == 1:
                        heatmap_data[row][col] += 1

        # Normaliza os dados do heatmap dividindo pela quantidade total de soluções
        heatmap_data = heatmap_data / len(solutions)

        # Configura o tamanho da figura e plota o heatmap usando seaborn
        plt.figure(figsize=(10, 8))
        sns.heatmap(heatmap_data, annot=True, fmt='.2f', cmap='YlOrRd', square=True)
        plt.title(f"{n}-Rainhas {solver_type.capitalize()} Mapa de calor\n"
                  f"Total de soluções: {len(solutions)}, Tempo: {time:.4f}s")
        plt.xlabel('Coluna')
        plt.ylabel('Linha')

        # Cria o diretório para salvar o heatmap se ele não existir
        img_dir = os.path.join(self.img_dir, f"{n}_queens")
        os.makedirs(img_dir, exist_ok=True)
        plt.savefig(os.path.join(img_dir, f"{solver_type}_heatmap.png"), bbox_inches='tight')
        plt.close()

    def generate_combined_heatmap(self, log_file):
        # Lê o arquivo de log e carrega os dados JSON de cada linha
        with open(log_file, 'r') as f:
            log_data = [json.loads(line) for line in f]

        # Extrai valores únicos de n e tipos de solver dos dados de log
        n_values = sorted(set(entry['n'] for entry in log_data))
        solver_types = sorted(set(entry['solver_type'] for entry in log_data))

        # Configura o layout da figura para múltiplos heatmaps combinados
        fig, axes = plt.subplots(len(n_values), len(solver_types), figsize=(5*len(solver_types), 5*len(n_values)))
        fig.suptitle("Mapas de calor das soluções N-Rainhas", fontsize=16)

        # Itera sobre cada valor de n e tipo de solver para plotar heatmaps individuais em uma grade
        for i, n in enumerate(n_values):
            for j, solver_type in enumerate(solver_types):
                # Encontra a entrada correspondente nos dados de log
                entry = next(entry for entry in log_data if entry['n'] == n and entry['solver_type'] == solver_type)
                solutions = entry['solutions']
                time = entry['time']

                # Inicializa a matriz de dados do heatmap e incrementa a contagem para cada solução
                heatmap_data = np.zeros((n, n))
                for solution in solutions:
                    for row in range(n):
                        for col in range(n):
                            if solution[row][col] == 1:
                                heatmap_data[row][col] += 1

                # Normaliza os dados do heatmap
                heatmap_data = heatmap_data / len(solutions)

                # Seleciona o eixo apropriado para o subplot e plota o heatmap
                ax = axes[i][j] if len(n_values) > 1 else axes[j]
                sns.heatmap(heatmap_data, annot=True, fmt='.2f', cmap='YlOrRd', square=True, ax=ax, cbar=False)
                ax.set_title(f"{n}-Rainhas {solver_type.capitalize()}\n"
                             f"Soluções: {len(solutions)}, Tempo: {time:.4f}s")
                ax.set_xlabel('Coluna')
                ax.set_ylabel('Linha')

        # Ajusta o layout da figura e salva a imagem combinada dos heatmaps
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig(os.path.join(self.img_dir, "combined_heatmap.png"), bbox_inches='tight')
        plt.close()
