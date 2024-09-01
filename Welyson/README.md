# Mapas de Calor e Logging

Este projeto implementa um solucionador para o problema das N-Rainhas usando métodos sequenciais e paralelos. Ele inclui funcionalidades para logging dos resultados e geração de mapas de calor para visualizar a distribuição das soluções.

# Interpretando o Mapa de Calor das N-Rainhas

O mapa de calor que geramos para o problema das N-Rainhas é uma ferramenta visual poderosa que nos ajuda a entender os padrões nas soluções encontradas. Aqui está uma explicação passo a passo de como interpretar este mapa:

## O que é o mapa de calor?
Os mapas de calor fornecem uma visualização da frequência com que cada posição do tabuleiro é ocupada por uma rainha nas soluções encontradas.

- Cores mais escuras (vermelho) indicam posições mais frequentemente ocupadas.
- Cores mais claras (amarelo/branco) indicam posições menos frequentemente ocupadas.
- Os números em cada célula representam a proporção de soluções em que aquela posição é ocupada.

1. **Representação do tabuleiro**: Cada quadrado no mapa de calor representa uma posição no tabuleiro de xadrez. As linhas representam as fileiras do tabuleiro, e as colunas representam as colunas do tabuleiro.

2. **Cores e números**: As cores e os números em cada quadrado indicam a frequência com que uma rainha é colocada naquela posição específica, considerando todas as soluções encontradas.

![Mapa de calor](https://raw.githubusercontent.com/welyson1/SistemasDistribuidosNrainhas/main/Welyson/solution_images/combined_heatmap.png)

## Como interpretar as cores e números

3. **Escala de cores**: 
   - Cores mais escuras (tendendo ao vermelho) indicam posições onde as rainhas são colocadas com mais frequência.
   - Cores mais claras (tendendo ao amarelo ou branco) indicam posições onde as rainhas são colocadas com menos frequência.

4. **Números nas células**: 
   - Os números em cada célula representam a proporção de soluções em que uma rainha é colocada naquela posição.
   - Por exemplo, um valor de 0.25 significa que em 25% das soluções, uma rainha foi colocada naquela posição.

## Requisitos

- Python 3.7+
- matplotlib
- seaborn
- numpy

Você pode instalar as dependências necessárias usando:

```
pip install matplotlib seaborn numpy
```

## Estrutura do Projeto

- `main.py`: Arquivo principal que executa os solucionadores e gera logs e mapas de calor.
- `logger.py`: Contém a classe `NQueensLogger` para logging dos resultados.
- `image_generator.py`: Contém a classe `NQueensHeatmapGenerator` para gerar mapas de calor.
- `nqueens/`: Diretório contendo os solucionadores sequencial e paralelo.

## Como Usar

1. Clone o repositório ou baixe os arquivos do projeto.

2. Navegue até o diretório do projeto no terminal.

3. Execute o script principal:

   ```
   python main.py
   ```

   Por padrão, isso executará o solucionador para N = 4, 8, 10, 12 e 13, gerará logs e mapas de calor.

4. Para desabilitar a geração de mapas de calor, modifique a última linha em `main.py`:

   ```python
   main(generate_heatmaps=False)
   ```

## Customização

- Para alterar os valores de N, modifique a lista `n_values` em `main.py`.
- Para ajustar os parâmetros de logging, edite a classe `NQueensLogger` em `logger.py`.
- Para modificar a aparência dos mapas de calor, edite a classe `NQueensHeatmapGenerator` em `image_generator.py`.

## Saída

Após a execução, você encontrará:

1. Arquivos de log no diretório `logs/`:
   - Formato: `nqueens_log_YYYYMMDD_HHMMSS.json`
   - Contém detalhes sobre cada execução, incluindo N, tipo de solucionador, número de soluções e tempo de execução.

2. Mapas de calor no diretório `heatmaps/`:
   - Mapas individuais: `{N}_queens/{solver_type}_heatmap.png`
   - Mapa combinado: `combined_heatmap.png`
