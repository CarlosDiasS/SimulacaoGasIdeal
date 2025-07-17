import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.spatial import cKDTree

# Parâmetros gerais
num_particulas = 300     # Número de partículas
intervalo_tempo = 0.015   # Intervalo de tempo (s)
num_passos_simulacao = 100 # Número de passos na simulação
nivel_ruido = 0.02        # Intensidade do ruído branco (aumentado para maior movimento)
const_boltzmann = 1.38e-23 # Constante de Boltzmann (J/K)
raio_colisao = 0.05       # Raio de colisão das partículas
epsilon = 1.0  # profundidade do poço
sigma = 0.1    # distância onde o potencial é zero
r_cut = 2.5 * sigma


# Parâmetros ajustáveis pelo usuário
massa_pistao = 6         # Massa do pistão
area_base = 2.0          # Área da base

# Inicializar partículas com massas e velocidades diferentes
def inicializar_sistema(n_particulas, area):
    lado = np.sqrt(area)
    posicoes = np.random.uniform(0, lado, (n_particulas, 2))
    massas = np.random.uniform(1, 5, n_particulas)  # Massas variando entre 1 e 5
    # Inicializar velocidades com valores pequenos (não zero)
    velocidades_iniciais = np.random.uniform(1, 5.0, n_particulas)  # Velocidades iniciais
    direcoes = np.random.normal(size=(n_particulas, 2))
    direcoes /= np.linalg.norm(direcoes, axis=1)[:, np.newaxis]
    velocidades = direcoes * velocidades_iniciais[:, np.newaxis]  # Velocidades iniciais
    return posicoes, velocidades, massas, lado

# Atualização de posições, detecção de colisões com as paredes e entre partículas
def atualizar_movimento(posicoes, velocidades, massas, limite, dt, ruido):
    # Adicionar ruído branco às velocidades
    deslocamento_ruido = np.random.normal(0, ruido, posicoes.shape)
    velocidades += deslocamento_ruido * dt  # Atualiza as velocidades com o ruído

    # Atualizar posições com base nas novas velocidades
    posicoes += velocidades * dt

    # Colisão com as paredes
    for eixo in range(2):
        mascara_baixa = posicoes[:, eixo] < 0
        mascara_alta = posicoes[:, eixo] > limite
        velocidades[mascara_baixa | mascara_alta, eixo] *= -1
        posicoes[mascara_baixa, eixo] = 0
        posicoes[mascara_alta, eixo] = limite
    
    # Colisão entre partículas
    tree = cKDTree(posicoes)
    pares = tree.query_pairs(raio_colisao)
    
    for i, j in pares:
        delta_v = velocidades[i] - velocidades[j]
        delta_x = posicoes[i] - posicoes[j]
        distancia = np.linalg.norm(delta_x)
        if distancia == 0:
            continue
        direcao_normalizada = delta_x / distancia
        velocidade_relativa = np.dot(delta_v, direcao_normalizada)
        
        if velocidade_relativa < 0:
            mi = massas[i]
            mj = massas[j]
            fator = 2 * (mi * mj) / (mi + mj)
            impulso = fator * velocidade_relativa * direcao_normalizada
            velocidades[i] -= impulso / mi
            velocidades[j] += impulso / mj
    
    return posicoes, velocidades, deslocamento_ruido

# Calcular energia cinética e pressão
def calcular_energia(velocidades, massas):
    return 0.5 * np.sum(massas[:, np.newaxis] * velocidades**2)

def calcular_pressao(velocidades, massas, volume):
    v_quadrado_medio = np.mean(np.sum(velocidades**2, axis=1))
    massa_media = np.mean(massas)
    return (2 / 3) * massa_media * v_quadrado_medio * len(velocidades) / volume

# Função de simulação
def simular():
    posicoes, velocidades, massas, lado = inicializar_sistema(num_particulas, area_base)
    volume = lado**3
    energia_cinetica_total = []
    ruido_acumulado = []
    velocidades_medias = []
    velocidades_finais = None  # Para armazenar as velocidades finais

    # Configuração para animação
    fig, ax = plt.subplots()
    ax.set_xlim(0, lado)
    ax.set_ylim(0, lado)
    scatter = ax.scatter(posicoes[:, 0], posicoes[:, 1], c='blue', alpha=0.6)
    velocidade_texto = ax.text(0.02, 0.95, 'Velocidade Média: 0.00', transform=ax.transAxes)

    def atualizar(frame):
        nonlocal posicoes, velocidades, velocidades_finais
        posicoes, velocidades, deslocamento_ruido = atualizar_movimento(posicoes, velocidades, massas, lado, intervalo_tempo, nivel_ruido)
        scatter.set_offsets(posicoes)

        energia = calcular_energia(velocidades, massas)
        energia_cinetica_total.append(energia)
        ruido_medio = np.mean(np.abs(deslocamento_ruido))
        ruido_acumulado.append(ruido_medio)
        velocidade_media = np.mean(np.linalg.norm(velocidades, axis=1))
        velocidades_medias.append(velocidade_media)
        velocidade_texto.set_text(f'Velocidade Média: {velocidade_media:.2f}')

        # Armazenar as velocidades finais no último passo
        if frame == num_passos_simulacao - 1:
            velocidades_finais = np.linalg.norm(velocidades, axis=1)
        
        return scatter, velocidade_texto

    # Animação
    ani = FuncAnimation(fig, atualizar, frames=num_passos_simulacao, interval=intervalo_tempo * 1000, repeat=False)
    plt.title("Simulação - Movimento das Partículas")
    plt.show()

# Executar simulação
simular()