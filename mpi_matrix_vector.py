from mpi4py import MPI
import numpy as np
import time

comm = MPI.COMM_WORLD #comunicador
rank = comm.Get_rank() #identificador dentro do processo atual
size = comm.Get_size() #captura o numero total de processos

# N define o tamanho da matriz (NxN)
# N = 10000
N = int(9000 * np.sqrt(size))

if N < 9000:
    N = 9000

# Inicialização da matriz no processo 0
if rank == 0:
    A = np.random.rand(N, N)
    x = np.random.rand(N)
else:
    A = None #Garante que a matriz completa só existem no processo 0
    x = np.empty(N, dtype='d') # Este vetor x vazio será preenchido posteriormente com os dados broadcastados pelo rank 0.

#Broadcast do vetor x para todos os processos
comm.Bcast(x, root=0) #O processo raiz (especificado por root=0) envia a cópia do seu vetor x para todos os outros processos no comunicador comm. esta linha, todos os processos terão uma cópia idêntica do vetor x que foi gerado no rank 0.

#Scatter das linhas da matriz A
rows_per_proc = N // size
remainder = N % size

#Calculando distribuição das linhas 
if rank < remainder:
    local_rows = rows_per_proc + 1
    start_row = rank * local_rows
else:
    local_rows = rows_per_proc
    start_row = rank * local_rows + remainder

# Cada processo recebe sua submatriz
local_A = np.empty((local_rows, N), dtype='d') #matriz varia que comporta o tamanho da porção do processo A que irá receber

sendcounts = [(rows_per_proc + 1) * N if i< remainder else rows_per_proc * N for i in range(size)] #especifica quantos elementos (não linhas) cada processo receberá da matriz A.
displs = [sum(sendcounts[:i]) for i in range(size)] # determina o índice inicial

comm.Scatterv([A, sendcounts, displs, MPI.DOUBLE], local_A, root=0)

# Cada processo faz sua parte da multiplicação
start = time.time()
local_y = local_A.dot(x)
end = time.time()
local_time = end - start

# Gather dos resultados
recvcounts = [rows if (i < remainder) else rows_per_proc for i, rows in enumerate([rows_per_proc + 1] * remainder + [rows_per_proc] * (size - remainder))]
recvcounts = [r for r in recvcounts]
recvcounts_in_elems = recvcounts

displs_out = [sum(recvcounts_in_elems[:i]) for i in range(size)]

if rank == 0:
    y = np.empty(N, dtype='d')
else:
    y = None

comm.Gatherv(local_y, [y, recvcounts_in_elems, displs_out, MPI.DOUBLE], root=0)

# Coletando os tempos de cada processo
total_time = comm.reduce(local_time, op=MPI.MAX, root=0)
