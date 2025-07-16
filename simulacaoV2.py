import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

def calcular_forcas_interparticulas(posicoes, r_cut, k_repulsao, L):
    n = posicoes.shape[0]
    forcas = np.zeros_like(posicoes)

    for i in range(n):
        for j in range(i + 1, n):
            # Considera o espaço periódico (mínima imagem)
            delta = posicoes[i] - posicoes[j]
            delta -= L * np.round(delta / L)
            dist = np.linalg.norm(delta)

            if dist < r_cut and dist > 1e-5:
                direcao = delta / dist
                intensidade = k_repulsao * (r_cut - dist)
                f = intensidade * direcao
                forcas[i] += f
                forcas[j] -= f  # Ação e reação

    return forcas

##primeira ordem 
def MetodoEuler(posicoes, velocidades, dt, massa, gamma, T, L, r_cut, k_repulsao):
    n = posicoes.shape[0]
    ruidoBranco = np.random.normal(0, np.sqrt(2 * gamma * T / massa / dt), (n, 2))
    forcas_visc_aleat = -gamma * velocidades + ruidoBranco

    forcas_repulsivas = calcular_forcas_interparticulas(posicoes, r_cut, k_repulsao, L) / massa

    aceleracoes = forcas_visc_aleat + forcas_repulsivas

    velocidades += aceleracoes * dt
    posicoes += velocidades * dt
    posicoes %= L  # Condições periódicas

    return posicoes, velocidades

#histograma de velocidades
def plot_distribuicao_velocidades(velocidades, massa, T):
    modulos_v = np.linalg.norm(velocidades, axis=1)

    # Histograma
    v_vals = np.linspace(0, np.max(modulos_v), 100)
    hist, bins = np.histogram(modulos_v, bins=v_vals, density=True)
    centers = 0.5 * (bins[1:] + bins[:-1])

    # Distribuição de Maxwell-Boltzmann em 2D
    def maxwell_2d(v, m, T):
        return (m / T) * v * np.exp(-m * v**2 / (2 * T))

def Simulacao(n, k):
    # Parâmetros
    L = 10.0
    dt = 0.01
    passos = 1000
    gamma = 0.1
    T = 1.0
    massa = 1.0
    r_cut = 0.5  # Limiar para atuação da força
    k_repulsao = 10.0  # Constante de repulsão (colisão elástica)




    # # Inicialização
    # posicoes = np.random.rand(n, 2) * L
    # velocidades = np.random.normal(0, np.sqrt(T / massa), (n, 2))

    # indices_trajetoria = np.random.choice(n, k, replace=False)
    # trajetorias = {i: [] for i in indices_trajetoria}

    # for passo in range(passos):
    #     posicoes, velocidades = MetodoEuler(
    #         posicoes, velocidades, dt, massa, gamma, T, L, r_cut, k_repulsao
    #     )

    #     if passo % 10 == 0:
    #         for i in indices_trajetoria:
    #             trajetorias[i].append(posicoes[i].copy())

    # # Plotagem
    # fig, ax = plt.subplots(figsize=(6, 6))
    # for i in indices_trajetoria:
    #     traj = np.array(trajetorias[i])
    #     ax.plot(traj[:, 0], traj[:, 1], label=f"Partícula {i}")
    # ax.set_title(f"Trajetória de {k} partículas")
    # ax.set_xlim(0, L)
    # ax.set_ylim(0, L)
    # ax.set_xlabel("x")
    # ax.set_ylabel("y")
    # ax.grid(True)
    # ax.set_aspect("equal")

    # buf = BytesIO()
    # plt.savefig(buf, format='png')
    # buf.seek(0)
    # plt.close(fig)
    # return buf