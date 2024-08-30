import sequencial
import paralelo

"""
    Máquina utilizada na execução:
    
    Processador: 
    AMD Ryzen 7 4800H (8 cores, 16 threads), 2.9GHz - 4.2GHz, 16MB cache, 45W TDP
    
    Memória: 16Gb RAM
    Armazenamento: SSD 1TB
    
    Versão do Python: 3.12.1
    
"""


def main():
    number_of_queens = [4, 5, 6, 7, 8, 9, 10]

    for n in number_of_queens:

        all_solutions_sequencial, sequencial_time = sequencial.sequencial_solve(n)
        all_solutions_paralelo, paralelo_time = paralelo.paralelo_solver(n)

        total_solutions_sequencial = len(all_solutions_sequencial)
        total_solutions_paralelo = len(all_solutions_paralelo)

        sequencial_solutions_to_print = min(total_solutions_sequencial, 5)
        paralelo_solutions_to_print = min(total_solutions_paralelo, 5)

        print(f"Solução para {n}-Queen:\n")
        print(f"Sequencial: {total_solutions_sequencial}\n")
        for i, solution in enumerate(all_solutions_sequencial[:sequencial_solutions_to_print], 1):
            print(f"{i}: {solution}")
        print(f"Tempo: {sequencial_time:.5f} segundos\n")

        print(f"Paralelo: {total_solutions_paralelo}\n")
        for i, solution in enumerate(all_solutions_paralelo[:paralelo_solutions_to_print], 1):
            print(f"{i}: {solution}")
        print(f"Tempo: {paralelo_time:.5f} segundos\n")


if __name__ == "__main__":
    main()
