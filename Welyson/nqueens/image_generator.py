# image_generator.py
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class NQueensHeatmapGenerator:
    def __init__(self):
        self.img_dir = "heatmaps"

    def generate_heatmaps(self, log_file):
        with open(log_file, 'r') as f:
            log_data = [json.loads(line) for line in f]

        for entry in log_data:
            n = entry['n']
            solver_type = entry['solver_type']
            solutions = entry['solutions']
            time = entry['time']

            self._generate_heatmap(n, solver_type, solutions, time)

    def _generate_heatmap(self, n, solver_type, solutions, time):
        heatmap_data = np.zeros((n, n))
        
        for solution in solutions:
            for row in range(n):
                for col in range(n):
                    if solution[row][col] == 1:
                        heatmap_data[row][col] += 1

        # Normalize the heatmap data
        heatmap_data = heatmap_data / len(solutions)

        plt.figure(figsize=(10, 8))
        sns.heatmap(heatmap_data, annot=True, fmt='.2f', cmap='YlOrRd', square=True)
        plt.title(f"{n}-Queens {solver_type.capitalize()} Heatmap\n"
                  f"Total solutions: {len(solutions)}, Time: {time:.4f}s")
        plt.xlabel('Column')
        plt.ylabel('Row')

        img_dir = os.path.join(self.img_dir, f"{n}_queens")
        os.makedirs(img_dir, exist_ok=True)
        plt.savefig(os.path.join(img_dir, f"{solver_type}_heatmap.png"), bbox_inches='tight')
        plt.close()

    def generate_combined_heatmap(self, log_file):
        with open(log_file, 'r') as f:
            log_data = [json.loads(line) for line in f]

        n_values = sorted(set(entry['n'] for entry in log_data))
        solver_types = sorted(set(entry['solver_type'] for entry in log_data))

        fig, axes = plt.subplots(len(n_values), len(solver_types), figsize=(5*len(solver_types), 5*len(n_values)))
        fig.suptitle("N-Queens Solutions Heatmaps", fontsize=16)

        for i, n in enumerate(n_values):
            for j, solver_type in enumerate(solver_types):
                entry = next(entry for entry in log_data if entry['n'] == n and entry['solver_type'] == solver_type)
                solutions = entry['solutions']
                time = entry['time']

                heatmap_data = np.zeros((n, n))
                for solution in solutions:
                    for row in range(n):
                        for col in range(n):
                            if solution[row][col] == 1:
                                heatmap_data[row][col] += 1

                heatmap_data = heatmap_data / len(solutions)

                ax = axes[i][j] if len(n_values) > 1 else axes[j]
                sns.heatmap(heatmap_data, annot=True, fmt='.2f', cmap='YlOrRd', square=True, ax=ax, cbar=False)
                ax.set_title(f"{n}-Queens {solver_type.capitalize()}\n"
                             f"Solutions: {len(solutions)}, Time: {time:.4f}s")
                ax.set_xlabel('Column')
                ax.set_ylabel('Row')

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig(os.path.join(self.img_dir, "combined_heatmap.png"), bbox_inches='tight')
        plt.close()