import subprocess
import matplotlib.pyplot as plt
import numpy as np

process_counts = [1, 2, 4, 6, 8] 
mpi_program = "mpi_matrix_vector.py"
repeats = 3
times = []

print("Iniciando benchmark...")

for n_proc in process_counts:
    current_times = []
    print(f"\nTestando com {n_proc} processos...")
    
    for i in range(repeats):
        print(f"  Execução {i+1}/{repeats}")
        result = subprocess.run(
            ["mpiexec", "-n", str(n_proc), "python", mpi_program],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        output = result.stdout.strip().splitlines()
        
        for line in output:
            try:
                parts = line.strip().split()
                if len(parts) == 2 and int(parts[0]) == n_proc:
                    tempo = float(parts[1])
                    current_times.append(tempo)
                    print(f"    Tempo registrado: {tempo} segundos")
                    break
            except:
                continue
    
    media = np.mean(current_times)
    times.append(media)
    print(f"  -> Tempo médio com {n_proc} processos: {media:.4f} segundos")

# Calculando Speedup e Eficiência
t1 = times[0]
speedup = [t1 / t for t in times]
efficiency = [s / p * 100 for s, p in zip(speedup, process_counts)]

# Impressão em formato de tabela
print(f"{'Processos':>10} | {'Tempo (s)':>10} | {'Speedup':>8} | {'Eficiência (%)':>15}")
print("-" * 55)

for p, t, s, e in zip(process_counts, times, speedup, efficiency):
    print(f"{p:>10} | {t:>10.5f} | {s:>8.5f} | {e:>15.5f}")

# Plotando gráficos
plt.figure(figsize=(10, 5))

# Gráfico de Speedup
plt.subplot(1, 2, 1)
plt.plot(process_counts, speedup, marker='o')
plt.title("Speedup")
plt.xlabel("Número de Processos")
plt.ylabel("Speedup")
plt.grid(True)

# Gráfico de Eficiência
plt.subplot(1, 2, 2)
plt.plot(process_counts, efficiency, marker='s', color='orange')
plt.title("Eficiência (%)")
plt.xlabel("Número de Processos")
plt.ylabel("Eficiência (%)")
plt.grid(True)

plt.tight_layout()
plt.show()
