# Pseudocódigo para Soluções das N-Rainhas

## Solução Sequencial

```
Função SequentialNQueensSolver(N):
    soluções = lista vazia
    tabuleiro = matriz NxN preenchida com zeros

    Função is_safe(tabuleiro, linha, coluna):
        Para i de 0 até linha-1:
            Se tabuleiro[i][coluna] == 1:
                Retorna Falso
            Se tabuleiro[linha-i-1][coluna-i-1] == 1:
                Retorna Falso
            Se coluna+i < N e tabuleiro[linha-i-1][coluna+i] == 1:
                Retorna Falso
        Retorna Verdadeiro

    Função solve_util(tabuleiro, coluna):
        Se coluna >= N:
            Adiciona cópia do tabuleiro às soluções
            Retorna Verdadeiro

        Para linha de 0 até N-1:
            Se is_safe(tabuleiro, linha, coluna):
                tabuleiro[linha][coluna] = 1
                solve_util(tabuleiro, coluna + 1)
                tabuleiro[linha][coluna] = 0  // Backtrack

    solve_util(tabuleiro, 0)
    Retorna soluções

```

## Solução Paralela

```
Função ParallelNQueensSolver(N):
    soluções = lista vazia compartilhada entre threads
    num_threads = número de núcleos de CPU disponíveis

    Função solve_partial(linha_inicial):
        tabuleiro = matriz NxN preenchida com zeros
        tabuleiro[linha_inicial][0] = 1
        soluções_parciais = lista vazia

        Função is_safe(tabuleiro, linha, coluna):
            // Mesma implementação da versão sequencial

        Função solve_util(tabuleiro, coluna):
            Se coluna >= N:
                Adiciona cópia do tabuleiro às soluções_parciais
                Retorna Verdadeiro

            Para linha de 0 até N-1:
                Se is_safe(tabuleiro, linha, coluna):
                    tabuleiro[linha][coluna] = 1
                    solve_util(tabuleiro, coluna + 1)
                    tabuleiro[linha][coluna] = 0  // Backtrack

        solve_util(tabuleiro, 1)
        Retorna soluções_parciais

    // Cria uma pool de threads
    pool = ThreadPool(num_threads)

    // Mapeia a função solve_partial para cada linha inicial possível
    resultados = pool.map(solve_partial, range(N))

    // Combina todas as soluções parciais
    Para resultado em resultados:
        soluções.extend(resultado)

    Retorna soluções

```

## Explicação das Diferenças Principais

1. **Inicialização**:
   - Sequencial: Inicia com um tabuleiro vazio e começa a busca a partir da primeira coluna.
   - Paralelo: Cria várias instâncias de tabuleiro, cada uma com uma rainha já posicionada na primeira coluna em uma linha diferente.

2. **Divisão do Trabalho**:
   - Sequencial: Explora todas as possibilidades em uma única thread.
   - Paralelo: Divide o trabalho entre múltiplas threads, cada uma explorando um subconjunto do espaço de soluções.

3. **Combinação de Resultados**:
   - Sequencial: As soluções são adicionadas diretamente à lista de soluções.
   - Paralelo: Cada thread gera soluções parciais, que são posteriormente combinadas em uma lista final de soluções.

4. **Eficiência**:
   - Sequencial: Mais simples de implementar, mas pode ser mais lento para valores grandes de N.
   - Paralelo: Mais complexo, mas potencialmente mais rápido para valores grandes de N, especialmente em sistemas com múltiplos núcleos.

5. **Uso de Recursos**:
   - Sequencial: Usa apenas um núcleo do processador.
   - Paralelo: Pode utilizar múltiplos núcleos do processador, distribuindo a carga de trabalho.

Esta abordagem paralela divide o problema inicial em N subproblemas independentes, onde cada subproblema fixa a posição da rainha na primeira coluna e busca soluções para as colunas restantes. Isso permite que múltiplas threads trabalhem simultaneamente em diferentes partes do espaço de soluções, potencialmente reduzindo o tempo total de execução em sistemas com múltiplos núcleos de processamento.

