# N-Rainhas
Para resolver problemas complexos, como o Problema das N Rainhas, diferentes métodos de solução podem ser aplicados, cada um com suas características, vantagens e desvantagens. Vamos explorar alguns dos métodos mais comuns: **Backtracking**, **Força Bruta**, **Algoritmos Genéticos**, **Programação Dinâmica**, **Heurísticas e Meta-heurísticas**, e **Algoritmos Guloso (Greedy)**, comparando-os em termos de eficiência, aplicabilidade e complexidade.

## 1. **Backtracking**

### **Descrição:**  
- Backtracking é uma técnica de busca sistemática utilizada para resolver problemas de decisão, onde soluções são construídas incrementalmente. Se uma solução parcial não pode ser estendida para uma solução completa, o algoritmo retrocede ("backtracks") para a última decisão tomada e tenta outra alternativa.

**Aplicabilidade:**  
- É ideal para problemas onde soluções podem ser visualizadas como um espaço de árvore de decisões, como o Problema das N Rainhas, Sudoku, problemas de caminho em grafos, etc.

## 2. **Força Bruta (Brute Force)**

### **Descrição:**  
- O método de Força Bruta envolve testar todas as combinações possíveis para encontrar a solução para o problema. Não há otimização ou estratégia para reduzir o espaço de busca.

**Aplicabilidade:**  
- Usado quando há um pequeno número de possibilidades ou quando todas as soluções possíveis devem ser verificadas. Exemplo: verificar todas as combinações possíveis de senha em um ataque de força bruta.

## 3. **Algoritmos Genéticos**

### **Descrição:**  
- Algoritmos Genéticos são uma classe de algoritmos de otimização inspirados na teoria da evolução de Darwin. Eles usam operações como seleção, crossover (cruzamento) e mutação para evoluir uma população de soluções potenciais ao longo de várias gerações.

**Aplicabilidade:**  
- Útil em problemas de otimização complexos, como roteamento, programação e design, onde o espaço de solução é vasto e tradicionalmente difícil de explorar.

## 4. **Programação Dinâmica (Dynamic Programming)**

### **Descrição:**  
- Programação Dinâmica é uma técnica de otimização que resolve problemas complexos quebrando-os em subproblemas menores e armazenando os resultados de subproblemas já resolvidos para evitar recomputações.

**Aplicabilidade:**  
- Utilizada em problemas que podem ser divididos em subproblemas interdependentes, como o problema da mochila, caminho mais curto em um grafo, sequência comum mais longa, etc.

## 5. **Heurísticas e Meta-heurísticas**

### **Descrição:**  
- Heurísticas são métodos que exploram conhecimento especializado para encontrar soluções aproximadas para problemas complexos em um tempo razoável. Meta-heurísticas são estratégias de alto nível que guiam outras heurísticas, como Simulated Annealing, Algoritmos Genéticos, e Particle Swarm Optimization.

**Aplicabilidade:**  
- Usados em problemas de otimização onde encontrar uma solução ótima é menos importante do que encontrar uma solução boa em um tempo razoável. Exemplos incluem problemas de roteamento, agendamento e clustering.

## 6. **Algoritmos Guloso (Greedy Algorithms)**

### **Descrição:**  
- Algoritmos Guloso constroem soluções passo a passo, escolhendo a opção mais favorável disponível no momento (a escolha "gulosa"). Eles não revisitam decisões anteriores, o que significa que não garantem uma solução ótima global.

**Aplicabilidade:**  
- Útil para problemas onde uma solução ótima global pode ser alcançada através de uma série de escolhas ótimas locais, como o problema da moeda (troco mínimo), árvores geradoras mínimas, e algoritmos de caminho mínimo.

## **Comparação entre os Métodos**

- **Eficiência de Tempo:** Programação Dinâmica e Algoritmos Guloso são geralmente mais rápidos quando aplicáveis, enquanto Força Bruta é a mais lenta.
### - **Aplicabilidade:** Algoritmos Genéticos e Meta-heurísticas são mais flexíveis, adaptáveis a uma ampla gama de problemas. Backtracking e Programação Dinâmica são mais especializados.
### - **Complexidade de Implementação:** Algoritmos Genéticos, Heurísticas e Meta-heurísticas requerem mais parametrização e ajuste fino. Algoritmos de Força Bruta e Guloso são mais simples de implementar.
### - **Otimização:** Programação Dinâmica e Backtracking são mais voltados para encontrar soluções exatas, enquanto Algoritmos Genéticos e Meta-heurísticas se concentram em soluções aproximadas.


-------------------------

Felipe: porque estamos usando multiprocessos ao inves de threads?, o que da para melhorar ✅

Cunha: Explicar linha "multiprocessing.cpu_count()", Detalhes do GIL, Gráfico de Contenção de Locks, Dashboards Interativos: Plotly e Bokeh, Diferentes Configurações de Multiprocessing: ProcessPoolExecutor/ThreadPoolExecutor, comentarios no codigo base linha a linha, Gráfico de Contenção de Locks e Barramentos ✅

Welyson: Problema N-rainhas o que é?, Porque escolhemos o backtracking, porque python?, Tabuleiros Lado a Lado, salvar logs. ✅

Zuin: Gráficos de Overhead de Comunicação, Uso de CPU, Gráfico de Uso de Memória(opcional), porque estamos usando multiprocessos ao inves de threads?, fluxograma da execução do codigo base(olhar vscode)

Gabriel: 
Speedup(colocar refencia para falar que o speedup é do paralelo comparado com sequencial)
Eficiência, ajustar e plotar em porcentagem
Gráfico de Escalabilidade(Tentar ou eleminar)
comentarios no codigo base linha a linha ✅
Ambiente de Execução que o script esta rodando: Qual CPU, SO, Versão python, IDE (Falta IDE), ...?✅

Todos: Salvar os resultados das execuções, comentarios no codigo linha a linha do plot, readme feito em cada pasta