import json, Filtro
from flask import Flask, request, Response, render_template
from Filtro import *

app = Flask(__name__)
brasil = Filtro.Time()  # Instância única aqui

# Usa um jsonify sem ordenação
def jsonify_ordered(data):
    return Response(
        response=json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False),
        mimetype='application/json'
    )

@app.route('/')
def home():
    return render_template('front.html')

# Inserir
@app.route('/inserir', methods=['POST'])
def inserir_dado():
    novo_dado = request.get_json()
    resultado = brasil.inserir_dado(novo_dado)
    return jsonify_ordered(resultado)

@app.route('/filtrar', methods=['POST'])
def filtrar_dados():
    filtros = request.get_json()
    resultado = brasil.filtrar_dados(filtros)
    return jsonify_ordered(resultado)


# Deletar
@app.route('/deletar/<int:indice>', methods=['DELETE'])
def deletar_dado(indice):
    resultado = brasil.deletar_dado(indice)
    return jsonify_ordered(resultado)

# Atualizar
@app.route('/atualizar/<int:indice>', methods=['PUT'])
def atualizar_dado(indice):
    dado_atualizado = request.get_json()
    resultado = brasil.atualizar_dado(indice, dado_atualizado)
    return jsonify_ordered(resultado)

# Listar
@app.route('/listar', methods=['GET'])
def listar_dados():
    return jsonify_ordered(brasil.listar_dados())

# Consulta
@app.route('/gols/<time>')
def gols_time(time):
    return jsonify_ordered(brasil.total_team_goals(time))

@app.route('/confronto')
def confronto():
    time1 = request.args.get("time1")
    time2 = request.args.get("time2")
    return jsonify_ordered(brasil.team(time1, time2))

@app.route('/estado/<uf>')
def times_do_estado(uf):
    return jsonify_ordered(brasil.state(uf))

@app.route('/Time/<nomeTeam>')
def times(nomeTeam):
    return jsonify_ordered(brasil.mostraNome(nomeTeam))

@app.route('/gols/<int:n>/valor')
def jogos_com_valor(n):
    return jsonify_ordered(brasil.mostraValor(n))

@app.route('/linhas/<int:n>')
def primeiras_linhas(n):
    return jsonify_ordered(brasil.mostraLinhas(n))

# Front
app.run(port=5000, host='localhost', debug=True)
