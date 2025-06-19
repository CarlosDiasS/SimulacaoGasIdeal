# app.py

from flask import Flask, request, render_template, send_file
from simulacao import Simulacao

app = Flask(__name__)


@app.route('/simulacao')
def simulacao():
    return render_template('simulacao.html')


@app.route('/simulacao/plot.png')
def imagem_plot():
    n = int(request.args.get('n', 10000))
    k = int(request.args.get('k', 20))
    buf = Simulacao(n, k)
    return send_file(buf, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8080)

# Aplicacao rodando em um ambiente virtual isolado
# source venv-simulador/bin/activate
