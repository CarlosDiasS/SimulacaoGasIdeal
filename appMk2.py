from flask import Flask, request, send_file, render_template
import io
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

app = Flask(__name__)

# Função da simulação (igual do passo 1)
def simular_gas(n, passos=100):
    t = np.linspace(0, 10, passos)
    energia = np.sin(t) + 0.1 * n / 1000
    pressao = np.cos(t) + 0.05 * n / 1000
    temperatura = 1 + 0.1 * np.sin(t / 2) + 0.02 * n / 1000
    forca_pistao = 0.5 + 0.3 * np.abs(np.sin(t * 1.5)) + 0.01 * n / 1000
    return t, energia, pressao, temperatura, forca_pistao

@app.route('/simulacao/histograma.png')
def histograma():
    try:
        n = int(request.args.get('n', 100))
        # Simula velocidades aleatórias (modulo) para n partículas
        velocidades = np.random.normal(loc=0, scale=1, size=n)
        velocidades = np.abs(velocidades)  # módulo da velocidade

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.hist(velocidades, bins=30, color='skyblue', edgecolor='black')
        ax.set_title("Histograma da Velocidade das Partículas")
        ax.set_xlabel("Velocidade")
        ax.set_ylabel("Frequência")
        ax.grid(True)

        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png')
        plt.close(fig)
        img_bytes.seek(0)
        return send_file(img_bytes, mimetype='image/png')
    except Exception as e:
        return f"Erro interno: {str(e)}", 500

# Função para gerar gráfico PNG com os 4 gráficos
@app.route('/simulacao/plot.png')
def plot():
    try:
        n = int(request.args.get('n', 100))
        t, energia, pressao, temperatura, forca_pistao = simular_gas(n)

        fig, axs = plt.subplots(2, 2, figsize=(10, 7))

        axs[0,0].plot(t, energia, 'b-')
        axs[0,0].set_title('Energia Cinética')
        axs[0,0].grid(True)

        axs[0,1].plot(t, pressao, 'r-')
        axs[0,1].set_title('Pressão vs Tempo')
        axs[0,1].grid(True)

        axs[1,0].plot(t, temperatura, 'g-')
        axs[1,0].set_title('Temperatura vs Tempo')
        axs[1,0].grid(True)

        axs[1,1].plot(t, forca_pistao, 'm-')
        axs[1,1].set_title('Força no Pistão')
        axs[1,1].grid(True)

        plt.tight_layout()

        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png')
        plt.close(fig)
        img_bytes.seek(0)
        return send_file(img_bytes, mimetype='image/png')

    except Exception as e:
        return f"Erro interno: {str(e)}", 500

# Função para gerar GIF animado das partículas
@app.route('/simulacao/anim.gif')
def anim():
    n = int(request.args.get('n', 100))
    lado = 10
    posicoes = np.random.rand(n, 2) * lado
    velocidades = (np.random.rand(n, 2) - 0.5) * 2

    fig, ax = plt.subplots(figsize=(5,5))
    ax.set_xlim(0, lado)
    ax.set_ylim(0, lado)
    scatter = ax.scatter(posicoes[:, 0], posicoes[:, 1])

    def atualizar(frame):
        nonlocal posicoes, velocidades
        posicoes += velocidades * 0.1
        for i in range(2):
            mask1 = posicoes[:, i] < 0
            mask2 = posicoes[:, i] > lado
            velocidades[mask1 | mask2, i] *= -1
            posicoes[mask1, i] = 0
            posicoes[mask2, i] = lado
        scatter.set_offsets(posicoes)
        return scatter,

    ani = FuncAnimation(fig, atualizar, frames=50, blit=True)
    gif_bytes = io.BytesIO()
    ani.save(gif_bytes, writer=PillowWriter(fps=10))
    plt.close(fig)
    gif_bytes.seek(0)
    return send_file(gif_bytes, mimetype='image/gif')

@app.route('/simulacao/final.png')
def final_simulacao():
    try:
        n = int(request.args.get('n', 100))
        lado = 10
        np.random.seed(42)  # Opcional: fixar para reproduzibilidade
        posicoes = np.random.rand(n, 2) * lado

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.scatter(posicoes[:, 0], posicoes[:, 1], c='blue', alpha=0.6, s=10)
        ax.set_xlim(0, lado)
        ax.set_ylim(0, lado)
        ax.set_title("Estado Final da Simulação")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True)

        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png')
        plt.close(fig)
        img_bytes.seek(0)
        return send_file(img_bytes, mimetype='image/png')
    except Exception as e:
        return f"Erro interno: {str(e)}", 500

@app.route('/')
def home():
    return render_template('simulacaoPistao.html')

if __name__ == "__main__":
    app.run(debug=True)
