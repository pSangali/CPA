import json, Filtro
from flask import Flask, request, Response
from Filtro import *

app = Flask(__name__)

#usa um jsonify sem ordenacao
def jsonify_ordered(data):
    return Response(
        response=json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False),
        mimetype='application/json'
    )


#montar api puxar os metodos/classes
@app.route('/Time')
def obter_times():
    return jsonify_ordered(Filtro.Time(brasil).mostraLinhas(10))


@app.route('/linhas/<int:n>')
#exemplo linhas/5
def primeiras_linhas(n):
    return jsonify_ordered(Filtro.Time(brasil).mostraLinhas(n))

@app.route('/gols/<time>')
def gols_time(time):
    return jsonify_ordered(Filtro.Time(brasil).total_team_goals(time))

@app.route('/confronto')
def confronto():
    time1 = request.args.get("time1")
    time2 = request.args.get("time2")
    return jsonify_ordered(Filtro.Time(brasil).team(time1, time2))

@app.route('/estado/<uf>')
def times_do_estado(uf):
    return jsonify_ordered(Filtro.Time(brasil).state(uf))

@app.route('/gols/<int:n>/valor')
def jogos_com_valor(n):
    return jsonify_ordered(Filtro.Time(brasil).mostraValor(n))


#front


app.run(port=5000, host='localhost', debug=True)
