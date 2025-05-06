import requests
import json

url_base = "http://localhost:5000"

# Inserir dado
novo_jogo = {
    "datetime": "2024-05-01",
    "home_team": "Flamengo",
    "away_team": "Palmeiras",
    "home_goal": 2,
    "home_team_state": "RJ",
    "away_goal": 2,
    "away_team_state": "SP"
}
resposta = requests.post(f"{url_base}/dado", json=novo_jogo)
print("Inserir:", resposta.json())

# Listar todos
resposta = requests.get(f"{url_base}/dado")
print("Listar:", json.dumps(resposta.json(), indent=2, ensure_ascii=False))

# Atualizar o primeiro jogo (índice 0)
dado_atualizado = novo_jogo.copy()
dado_atualizado["away_goal"] = 3
resposta = requests.put(f"{url_base}/dado/0", json=dado_atualizado)
print("Atualizar:", resposta.json())

# Deletar o primeiro jogo (índice 0)
resposta = requests.delete(f"{url_base}/dado/0")
print("Deletar:", resposta.json())

# Consulta: primeiros 5 jogos
resposta = requests.get(f"{url_base}/linhas/5")
print("Primeiras linhas:", json.dumps(resposta.json(), indent=2, ensure_ascii=False))

# Consulta: gols do time
resposta = requests.get(f"{url_base}/gols/Flamengo")
print("Gols do time:", resposta.json())

# Consulta: confronto entre dois times
resposta = requests.get(f"{url_base}/confronto?time1=Flamengo&time2=Palmeiras")
print("Confronto:", json.dumps(resposta.json(), indent=2, ensure_ascii=False))

# Consulta: times por estado
resposta = requests.get(f"{url_base}/estado/RJ")
print("Times por estado (RJ):", resposta.json())

# Consulta: informações do time
resposta = requests.get(f"{url_base}/Time/Flamengo")
print("Informações do time:", resposta.json())

# Consulta: jogos com valor de gols
resposta = requests.get(f"{url_base}/gols/3/valor")
print("Jogos com 3 gols:", resposta.json())
