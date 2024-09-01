#### Explicar linha "multiprocessing.cpu_count()",

Essa linha está dentro do método **init** da classe ParallelNQueensSolver, que é uma subclasse de NQueensSolver.

multiprocessing.cpu_count(): Esse comando retorna o número de núcleos de CPU disponíveis na máquina onde o código está sendo executado. Isso é útil porque o problema das N-Rainhas pode ser resolvido mais rapidamente dividindo o trabalho entre vários núcleos de CPU, aproveitando o paralelismo.

Contexto no código: Ao definir o número de processos como o número de núcleos de CPU disponíveis (self.num_processes = multiprocessing.cpu_count()), o código se prepara para distribuir o trabalho entre todos os núcleos disponíveis. Isso significa que, ao invés de usar um único núcleo para resolver o problema, o código pode dividir o trabalho entre vários núcleos, aumentando a eficiência e diminuindo o tempo de execução.

Resumindo, essa linha de código garante que o solucionador paralelo do problema das N-Rainhas utilize eficientemente todos os recursos de processamento disponíveis na máquina.

#### Detalhes do GIL

O Global Interpreter Lock (GIL) é um conceito importante no contexto da linguagem de programação Python, especialmente quando falamos sobre multithreading e paralelismo. Aqui estão alguns detalhes sobre o GIL:

O que é o GIL?

- **GIL** significa _Global Interpreter Lock_ (Trava Global do Interpretador). É um mutex (mutual exclusion) que protege o acesso a objetos do Python, impedindo que múltiplas threads executem código Python ao mesmo tempo.

Por que o GIL existe?

- O GIL foi introduzido no Python para facilitar a implementação de um interpretador de thread segura em termos de memória. Como o gerenciamento de memória em Python não é thread-safe por padrão, o GIL evita que múltiplas threads modifiquem simultaneamente objetos Python, prevenindo possíveis corrupções de memória.

Impacto do GIL em Multithreading:

- **Multithreading**: Em Python, mesmo que você crie várias threads, o GIL faz com que apenas uma thread possa executar código Python de cada vez. Isso significa que, para tarefas fortemente ligadas à CPU, o uso de multithreading em Python não resulta em uma melhoria de desempenho significativa. Na verdade, pode até piorar o desempenho devido à sobrecarga adicional do gerenciamento de threads.
- **I/O Bound vs CPU Bound**: Para tarefas que são _I/O-bound_ (como operações de rede ou leitura/escrita de arquivos), o impacto do GIL é menor, pois as threads podem liberar o GIL enquanto aguardam a conclusão das operações de I/O. No entanto, para tarefas _CPU-bound_ (como cálculos intensivos), o GIL pode ser um gargalo significativo.

Alternativas ao Multithreading para Paralelismo:

- **Multiprocessing**: Ao contrário do multithreading, o módulo `multiprocessing` cria processos separados, cada um com seu próprio GIL, permitindo a execução real de código Python em paralelo em múltiplos núcleos da CPU. Isso é especialmente útil para tarefas CPU-bound.

- **Extensions em C/C++**: Para contornar o GIL, algumas extensões em C/C++ liberam o GIL enquanto executam código nativo, permitindo que threads rodem em paralelo de maneira eficiente.

- **GIL nas versões mais recentes**: Há um contínuo debate na comunidade Python sobre a remoção ou melhoria do GIL, e várias propostas e experimentos foram feitos ao longo dos anos. Porém, remover o GIL completamente é um desafio, devido ao impacto que teria na compatibilidade e desempenho das extensões e bibliotecas existentes.

Conclusão:
O GIL é uma característica intrínseca do interpretador CPython que simplifica o desenvolvimento de código seguro, mas limita o potencial de paralelismo verdadeiro usando threads em Python. Para tarefas que exigem desempenho paralelo em Python, o uso de `multiprocessing` ou até mesmo a implementação de partes críticas do código em linguagens como C/C++ pode ser mais eficaz.

#### Diferentes Configurações de Multiprocessing: ProcessPoolExecutor/ThreadPoolExecutor

O Python oferece diferentes formas de paralelismo e concorrência através dos módulos `multiprocessing` e `concurrent.futures`. Duas das classes mais utilizadas para criar pools de processos ou threads são `ProcessPoolExecutor` e `ThreadPoolExecutor`. Vamos explorar as diferenças entre elas e quando cada uma deve ser utilizada.

**1. `ProcessPoolExecutor`**

**Descrição:**

- `ProcessPoolExecutor` faz parte do módulo `concurrent.futures` e permite a criação de um pool de processos, onde cada processo é independente e executa código Python em paralelo.
- Cada processo no pool tem seu próprio espaço de memória, o que significa que não compartilham o mesmo GIL (Global Interpreter Lock).

**Quando usar:**

- Ideal para tarefas _CPU-bound_, ou seja, tarefas que demandam muito processamento e beneficiam-se de execução paralela em múltiplos núcleos da CPU.
- Exemplos: processamento de imagens, cálculos matemáticos complexos, simulações científicas.

**Vantagens:**

- Pode realmente utilizar múltiplos núcleos da CPU, o que permite um ganho de desempenho significativo para tarefas pesadas em CPU.
- Cada processo é isolado, o que significa que falhas em um processo não afetam os outros.

**Desvantagens:**

- Criação de processos é mais custosa em termos de tempo e memória do que a criação de threads.
- A comunicação entre processos pode ser mais complexa e lenta devido à necessidade de serialização (por exemplo, usando `pickle`).

**Exemplo:**

```python
from concurrent.futures import ProcessPoolExecutor

def heavy_computation(x):
    return x * x

with ProcessPoolExecutor() as executor:
    results = list(executor.map(heavy_computation, range(10)))
print(results)
```

**2. `ThreadPoolExecutor`**

**Descrição:**

- `ThreadPoolExecutor` também faz parte do módulo `concurrent.futures` e cria um pool de threads, que são leves e compartilham o mesmo espaço de memória.
- As threads, no entanto, são limitadas pelo GIL, o que significa que apenas uma thread pode executar código Python ao mesmo tempo.

**Quando usar:**

- Ideal para tarefas _I/O-bound_, ou seja, tarefas que passam a maior parte do tempo esperando por operações de entrada/saída, como leitura de arquivos, requisições de rede, ou operações de banco de dados.
- Exemplos: servidores web, crawlers de web, aplicações que realizam muitas operações de leitura e escrita.

**Vantagens:**

- Threads são mais leves que processos e geralmente têm um tempo de criação e overhead de memória menores.
- Excelente para aumentar a responsividade de aplicações I/O-bound, permitindo que o tempo ocioso seja usado para outras operações.

**Desvantagens:**

- Como todas as threads compartilham o mesmo espaço de memória e estão sujeitas ao GIL, não há ganho de desempenho significativo para tarefas CPU-bound.
- Concorrência em threads pode ser mais complexa devido a possíveis condições de corrida.

**Exemplo:**

```python
from concurrent.futures import ThreadPoolExecutor

def io_task(x):
    print(f"Task {x}")
    # Simula uma operação I/O-bound
    return x

with ThreadPoolExecutor() as executor:
    results = list(executor.map(io_task, range(10)))
print(results)
```

**Comparação Resumida:**

| Característica                 | `ProcessPoolExecutor`                           | `ThreadPoolExecutor`                                 |
| ------------------------------ | ----------------------------------------------- | ---------------------------------------------------- |
| **Utilização**                 | Tarefas _CPU-bound_                             | Tarefas _I/O-bound_                                  |
| **Paralelismo real**           | Sim (utiliza múltiplos núcleos da CPU)          | Não (limitado pelo GIL)                              |
| **Overhead de criação**        | Alto (processos são mais pesados)               | Baixo (threads são mais leves)                       |
| **Isolamento**                 | Cada processo tem seu próprio espaço de memória | Todas as threads compartilham memória                |
| **Segurança**                  | Processos são mais isolados                     | Threads podem ter problemas com condições de corrida |
| **Comunicação entre unidades** | Mais complexa (necessidade de serialização)     | Mais simples (compartilham memória)                  |

**Conclusão:**

- Use `ProcessPoolExecutor` para tarefas que demandam alta computação (CPU-bound) e onde o isolamento entre tarefas é importante.
- Use `ThreadPoolExecutor` para tarefas que envolvem muito I/O, como operações de rede ou leitura/escrita de arquivos, onde o tempo de espera pode ser aproveitado para executar outras tarefas simultaneamente.

Escolher a configuração correta depende da natureza da tarefa que você está tentando paralelizar ou executar de forma concorrente.

#### Gráfico de Contenção de Locks e Barramentos

image: output.png

Explicação:
Linhas: Cada linha mostra como o número de threads/processos aguardando por um recurso específico (lock ou barramento) varia ao longo do tempo.
Picos: Os picos nas linhas indicam momentos de alta contenção, onde muitas threads ou processos estão competindo pelo mesmo recurso, possivelmente causando degradação no desempenho.
Diferença entre Contenção de Locks e Barramentos: Pode-se observar como os padrões de contenção diferem para locks e barramentos, refletindo a natureza das operações sendo executadas.
Este gráfico permite visualizar facilmente como a contenção afeta o desempenho de um sistema, e pode ser uma ferramenta útil para identificar gargalos em aplicações concorrentes e paralelas.
