import json
from flask import Flask, request, Response, render_template
from Filtro import *

app = Flask(__name__)
brasil = Time()  # Instância única

def jsonify_ordered(data):
    return Response(
        response=json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False),
        mimetype='application/json'
    )

@app.route('/')
def home():
    return render_template('front.html')

@app.route('/dado', methods=['GET', 'POST'])
def dado_colecao():
    if request.method == 'GET':
        return jsonify_ordered(brasil.listar_dados()), 200
    elif request.method == 'POST':
        novo_dado = request.get_json()
        if not novo_dado:
            return jsonify_ordered({"erro": "Dados inválidos"}), 400
        resultado = brasil.inserir_dado(novo_dado)
        return jsonify_ordered({"mensagem": "Inserido com sucesso", "resultado": resultado}), 200

@app.route('/dado/<int:indice>', methods=['PUT', 'DELETE'])
def dado_item(indice):

    if request.method == 'PUT':
        dado_atualizado = request.get_json()
        if not dado_atualizado:
            return jsonify_ordered({"erro": "Dados inválidos"}), 400
        resultado = brasil.atualizar_dado(indice, dado_atualizado)
        return jsonify_ordered({"mensagem": "Atualizado com sucesso", "resultado": resultado}), 200

    elif request.method == 'DELETE':
        resultado = brasil.deletar_dado(indice)
        return jsonify_ordered({"mensagem": "Removido com sucesso", "resultado": resultado}), 200

@app.route('/filtrar', methods=['POST'])
def filtrar_dados():
    filtros = request.get_json()
    if not filtros:
        return jsonify_ordered({"erro": "Filtros ausentes ou inválidos"}), 400
    resultado = brasil.filtrar_dados(filtros)
    return jsonify_ordered(resultado), 200

@app.route('/gols/<time>')
def gols_time(time):
    resultado = brasil.total_team_goals(time)
    if resultado is None:
        return jsonify_ordered({"erro": f"Time '{time}' não encontrado"}), 400
    return jsonify_ordered({"gols": resultado}), 200

@app.route('/confronto')
def confronto():
    time1 = request.args.get("time1")
    time2 = request.args.get("time2")
    if not time1 or not time2:
        return jsonify_ordered({"erro": "Ambos os times devem ser informados"}), 400
    resultado = brasil.team(time1, time2)
    return jsonify_ordered(resultado), 200

@app.route('/estado/<uf>')
def times_do_estado(uf):
    resultado = brasil.state(uf)
    if not resultado:
        return jsonify_ordered({"erro": f"Nenhum time encontrado no estado '{uf.upper()}'"}), 400
    return jsonify_ordered(resultado), 200

@app.route('/Time/<nomeTeam>')
def times(nomeTeam):
    resultado = brasil.mostraNome(nomeTeam)
    if not resultado:
        return jsonify_ordered({"erro": f"Time '{nomeTeam}' não encontrado"}), 400
    return jsonify_ordered(resultado), 200

@app.route('/gols/<int:n>/valor')
def jogos_com_valor(n):
    resultado = brasil.mostraValor(n)
    return jsonify_ordered(resultado), 200

@app.route('/linhas/<int:n>')
def primeiras_linhas(n):
    resultado = brasil.mostraLinhas(n)
    return jsonify_ordered(resultado), 200

# Front
app.run(port=5000, host='localhost', debug=True)