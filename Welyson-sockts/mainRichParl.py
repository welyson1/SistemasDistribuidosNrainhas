import time
import threading
import inspect
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.syntax import Syntax
from rich.live import Live
from rich.table import Table

console = Console()

def posicao_segura(tabuleiro, linha, coluna):
    for i in range(coluna):
        if tabuleiro[linha][i] == 1:
            return False
    for i, j in zip(range(linha, -1, -1), range(coluna, -1, -1)):
        if tabuleiro[i][j] == 1:
            return False
    for i, j in zip(range(linha, len(tabuleiro), 1), range(coluna, -1, -1)):
        if tabuleiro[i][j] == 1:
            return False
    return True

def resolver_nrainhas_thread(tabuleiro, coluna, solucoes, lock, live, layout):
    n = len(tabuleiro)
    if coluna >= n:
        with lock:
            solucoes.append([''.join('Q' if cell else '.' for cell in row) for row in tabuleiro])
        return

    for i in range(n):
        tabuleiro[i][coluna] = 1
        update_visualization(live, layout, tabuleiro, f"Testando rainha na posição ({i}, {coluna})")
        if posicao_segura(tabuleiro, i, coluna):
            threads = []
            for j in range(coluna + 1, n):
                t = threading.Thread(target=resolver_nrainhas_thread, args=(tabuleiro, j, solucoes, lock, live, layout))
                threads.append(t)
                t.start()
            for t in threads:
                t.join()
        tabuleiro[i][coluna] = 0
        update_visualization(live, layout, tabuleiro, f"Removendo rainha da posição ({i}, {coluna})")

def n_rainhas_paralela(n):
    tabuleiro = [[0] * n for _ in range(n)]
    solucoes = []
    lock = threading.Lock()
    
    layout = Layout()
    layout.split_column(
        Layout(name="upper"),
        Layout(name="lower")
    )
    layout["upper"].split_row(
        Layout(name="code", ratio=2),
        Layout(name="board", ratio=1)
    )
    layout["lower"].update(Panel("Logs"))

    code = Syntax(inspect.getsource(resolver_nrainhas_thread), "python", line_numbers=True)
    layout["code"].update(Panel(code, title="Código Python"))

    with Live(layout, refresh_per_second=4) as live:
        resolver_nrainhas_thread(tabuleiro, 0, solucoes, lock, live, layout)
    
    return solucoes

def update_visualization(live, layout, tabuleiro, message):
    board_table = Table(show_header=False, show_lines=True)
    for row in tabuleiro:
        board_table.add_row(*['♛' if cell else ' ' for cell in row])
    layout["board"].update(Panel(board_table, title="Tabuleiro"))
    layout["lower"].update(Panel(message))
    live.update(layout)
    time.sleep(0.02)  # Ajuste este valor para controlar a velocidade da animação

if __name__ == "__main__":
    n = 4  # Número de rainhas

    console.print("[bold green]Resolvendo N-Rainhas Paralelo[/bold green]")
    start_time = time.time()
    solucoes_paralelo = n_rainhas_paralela(n)
    tempo_paralelo = time.time() - start_time
    console.print(f"Soluções Paralelo: {len(solucoes_paralelo)} em {tempo_paralelo:.4f}s")
