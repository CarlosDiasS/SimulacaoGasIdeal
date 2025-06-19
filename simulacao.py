import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

def MetodoEuler(posicoes, velocidades, dt, massa, gamma, T, L):
    n = posicoes.shape[0]
    ruidoBranco = np.random.normal(0, np.sqrt(2 * gamma * T / massa / dt), (n, 2))
    forcas = -gamma * velocidades + ruidoBranco
    velocidades += forcas * dt
    posicoes += velocidades * dt
    posicoes %= L
    return posicoes, velocidades


def Simulacao(n, k):

    # Parâmetros
    L = 10.0  # Tamanho da caixa (L x L) 2D
    dt = 0.01  # Passo de tempo
    passos = 1000  # Número de passos de simulação
    gamma = 0.1  # Coeficiente de dissipação
    T = 1.0  # Temperatura do reservatório térmico (k_B = 1)
    massa = 1.0  # Massa das partículas

    # Inicialização
    posicoes = np.random.rand(n, 2) * L
    velocidades = np.random.normal(0, np.sqrt(T / massa), (n, 2))

    # Escolhe k partículas para traçar (índices aleatórios)
    indices_trajetoria = np.random.choice(n, k, replace=False)
    trajetorias = {i: [] for i in indices_trajetoria}

    for passo in range(passos):
        posicoes, velocidades = MetodoEuler(
            posicoes, velocidades, dt, massa, gamma, T, L
        )

        if passo % 10 == 0:
            for i in indices_trajetoria:
                trajetorias[i].append(posicoes[i].copy())


    # Plotagem

    fig, ax = plt.subplots(figsize=(6, 6))
    for i in indices_trajetoria:
        traj = np.array(trajetorias[i])
        ax.plot(traj[:, 0], traj[:, 1], label=f"Partícula {i}")
    ax.set_title(f"Trajetória de {k} partículas")
    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True)
    ax.set_aspect("equal")

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf