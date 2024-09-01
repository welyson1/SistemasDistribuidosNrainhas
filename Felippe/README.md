# Multiprocessing em Python

## Introdução ao Multiprocessing

Multiprocessing é uma técnica de programação que permite a execução simultânea de múltiplas tarefas em um computador. Em Python, a biblioteca `multiprocessing` fornece uma interface para criar e gerenciar processos, permitindo que programas aproveitem múltiplos núcleos de processamento.

## Como Funciona o Multiprocessing

### Processos vs. Threads

- **Processos** são instâncias independentes de um programa, com seu próprio espaço de memória.
- **Threads** são unidades de execução dentro de um processo, compartilhando o mesmo espaço de memória.

O multiprocessing em Python usa processos, não threads, o que oferece algumas vantagens:
- Contorna o Global Interpreter Lock (GIL) do Python, permitindo verdadeiro paralelismo.
- Maior isolamento entre tarefas, aumentando a estabilidade.

### Criação de Processos

Quando você usa `multiprocessing.Pool`, o Python:
1. Cria cópias separadas do seu programa (processos filhos).
2. Cada processo tem sua própria instância do interpretador Python.
3. Os processos são distribuídos entre os núcleos disponíveis no CPU.

### Comunicação Entre Processos

- Processos não compartilham memória diretamente.
- A comunicação é feita através de mecanismos como filas e pipes.
- Dados são serializados (transformados em bytes) para serem passados entre processos.

## O Global Interpreter Lock (GIL) e Seu Impacto

O Global Interpreter Lock (GIL) é um mecanismo na implementação CPython do Python que impede que múltiplas threads nativas executem bytecodes Python simultaneamente. O GIL existe para garantir a segurança de thread em operações de memória, simplificando o gerenciamento de memória e facilitando a integração com extensões C que não são thread-safe.

Devido ao GIL, o multithreading em Python não oferece verdadeiro paralelismo para tarefas intensivas em CPU. Mesmo em sistemas multicore, apenas uma thread pode executar código Python por vez, limitando significativamente o ganho de desempenho em operações paralelas intensivas em CPU.

O multiprocessing, por outro lado, contorna essa limitação criando múltiplos processos Python independentes. Cada processo tem seu próprio interpretador Python e, consequentemente, seu próprio GIL. Isso permite que o código Python seja executado verdadeiramente em paralelo em diferentes núcleos do processador.

Para o problema das N-Rainhas, que é computacionalmente intensivo, o multiprocessing oferece vantagens claras sobre o multithreading:

 - Utilização efetiva de múltiplos cores: Cada processo pode executar em um núcleo diferente, aproveitando toda a capacidade do processador.
 - Paralelismo real: As buscas por soluções podem ocorrer simultaneamente, sem serem bloqueadas pelo GIL.
 - Escalabilidade: O desempenho pode melhorar significativamente com o aumento do número de núcleos disponíveis.

Ao usar multiprocessing em nossa solução, podemos dividir o problema em subproblemas independentes e distribuí-los entre vários processos. Cada processo busca soluções para uma parte específica do problema, contornando efetivamente as limitações impostas pelo GIL e resultando em um desempenho substancialmente melhor em sistemas multicore.

## Como o Computador Lida com Processos Paralelos

1. **Escalonamento**: O sistema operacional aloca tempo de CPU para cada processo.
2. **Troca de Contexto**: O SO alterna rapidamente entre processos, dando a ilusão de execução simultânea.
3. **Alocação de Recursos**: Cada processo recebe sua própria alocação de memória e recursos.
4. **Balanceamento de Carga**: O SO tenta distribuir os processos igualmente entre os núcleos disponíveis.

## Por Que o Multiprocessing Torna o Código Mais Rápido

1. **Aproveitamento de Múltiplos Núcleos**: Utiliza toda a capacidade do processador.
2. **Execução Verdadeiramente Paralela**: Tarefas são executadas simultaneamente em diferentes núcleos.
3. **Redução do Tempo Total de Execução**: Tarefas independentes são processadas concorrentemente.
4. **Eficiência em Tarefas Intensivas**: Ideal para operações que demandam muito processamento.

## Exemplo Prático: Resolução do Problema N-Rainhas

No nosso código de resolução do problema N-Rainhas:

1. **Divisão do Problema**: O tabuleiro é dividido em configurações iniciais diferentes.
2. **Distribuição de Tarefas**: Cada processo recebe uma configuração inicial para resolver.
3. **Execução Paralela**: Múltiplos processos buscam soluções simultaneamente.
4. **Combinação de Resultados**: As soluções parciais são combinadas no final.

## Considerações Importantes

- **Overhead de Criação de Processos**: Criar processos tem um custo computacional.
- **Limite de Escalabilidade**: O ganho de desempenho é limitado pelo número de núcleos disponíveis.
- **Complexidade Adicional**: O código multiprocessado pode ser mais difícil de depurar e manter.

## Conclusão

O multiprocessing em Python oferece uma maneira poderosa de aproveitar o hardware moderno para acelerar tarefas computacionalmente intensivas. Ao dividir o trabalho entre múltiplos processos, podemos resolver problemas complexos, como o N-Rainhas, de forma muito mais eficiente em sistemas multicore.
