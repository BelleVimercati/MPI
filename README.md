# Sistemas Distribuídos com MPI

## 🎯 Descrição do Projeto

Este projeto consiste na implementação de uma multiplicação de matriz por vetor utilizando MPI (Message Passing Interface) em Python, através da biblioteca `mpi4py`.

O código faz uso de primitivas coletivas para distribuição de dados entre os processos e coleta dos resultados, além de mensurar o desempenho do programa com diferentes quantidades de processos.

## 🏗️ Estrutura do Projeto

- `mpi_matrix_vector.py` → Código principal da multiplicação paralela de matriz por vetor.
- `benchmark.py` → Script para automação de testes de desempenho, cálculo de speedup e eficiência, além de geração de gráficos.

## 🔧 Tecnologias Utilizadas

- Python 3
- Biblioteca `mpi4py` (MPI para Python)
- MS-MPI (Windows) ou OpenMPI/MPICH (Linux/Mac)
- Matplotlib e NumPy para análises e gráficos

## 🔗 Primitivas Coletivas Utilizadas

- **`Bcast`** → Distribuição do vetor `x` para todos os processos.
- **`Scatterv`** → Distribuição de blocos da matriz `A` entre os processos.
- **`Gatherv`** → Coleta dos resultados parciais no processo raiz.
- **`Reduce (MPI.MAX)`** → Cálculo do tempo total de execução baseado no maior tempo entre os processos.

## 🚀 Como Executar

- Executando de maneira direta: (escolhendo quantos núcleos deseja utilizar)
  
```bash
mpiexec -n 4 python mpi_matrix_vector.py
```

- Executando com o script:

```bash
python benchmark.py
```

## 🧠 Metodologia de Testes

- Tamanho da matriz: **10.000 x 10.000** -> (Ajustável)
- Testado com os seguintes números de processos: **1, 2, 4, 6, 8** (rodado localmente)
- Cada configuração foi executada **3 vezes**, tomando a média dos tempos.
- Métricas avaliadas:
  - **Tempo de execução**.
- **Speedup:**  
  ![Speedup](https://latex.codecogs.com/svg.image?\bg_white%20Speedup%20=%20\frac{Tempo\_sequencial}{Tempo\_paralelo})

- **Eficiência:**  
  ![Eficiência](https://latex.codecogs.com/svg.image?\bg_white%20Eficiência%20=%20\frac{Speedup}{Nº\_de\_processos}%20\times%20100\%)

<!-- ## 📊 Resultados Obtidos

| Processos | Tempo (s) | Speedup | Eficiência (%) |
|------------|-----------|---------|----------------|
| 1          | 100       | 1.00    | 100            |
| 2          | 52        | 1.92    | 96             |
| 4          | 27        | 3.70    | 92             |
| 8          | 15        | 6.66    | 83             |
| 16         | 9         | 11.11   | 69             | -->
