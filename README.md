1- Intalação dos requisitos:
pip install flask pandas numpy requests matplotlib

2- Explicação dos arquivos:

*Filtro.py*

Contém a classe Time, responsável por toda a lógica de filtragem e manipulação de dados:
total_team_goals(time_name): Total de gols marcados por um time no período.
team(team_name1, team_name2): Lista de confrontos entre dois times.
state(estado): Retorna todos os times de um estado (ex: 'RJ').
mostraValor(value): Jogos em que qualquer time marcou exatamente value gols.
mostraNome(team_name): Lista todos os jogos de um time específico.
mostraLinhas(n): Retorna as n primeiras partidas do dataset.
inserir_dado(novo_dado): Adiciona um novo jogo ao dataset.
atualizar_dado(indice, dado_atualizado): Atualiza os dados de um jogo pelo índice.
deletar_dado(indice): Remove uma partida pelo índice.
listar_dados(): Retorna todos os jogos.
filtrar_dados(filtros): Filtra os dados com base em múltiplos critérios.

*Main.py*

GET /: Página inicial.
POST /inserir: Insere um novo jogo.
POST /filtrar: Filtra dados com base em parâmetros (JSON).
PUT /atualizar/<indice>: Atualiza um jogo pelo índice.
DELETE /deletar/<indice>: Deleta um jogo pelo índice.
GET /listar: Lista todos os dados.
GET /gols/<time>: Total de gols de um time.
GET /confronto?time1=X&time2=Y: Confrontos entre dois times.
GET /estado/<uf>: Times de um estado (sigla).
GET /Time/<nomeTeam>: Jogos de um time específico.
GET /gols/<n>/valor: Jogos com n gols por algum time.
GET /linhas/<n>: Primeiros n jogos do dataset.


*Consumidor.py*

Ações Realizadas
1- Inserir um novo jogo .
resposta = requests.post(f"{url_base}/inserir", json=novo_jogo)
Envia um jogo no formato JSON para ser adicionado ao dataset da API.
Dados inseridos:
{
  "datetime": "2024-05-01",
  "home_team": "Flamengo",
  "away_team": "Palmeiras",
  "home_goal": 2,
  "home_team_state": "RJ",
  "away_goal": 2,
  "away_team_state": "SP"
}

2- Listar todos os jogos.
resposta = requests.get(f"{url_base}/listar")
Recebe a lista completa de partidas (incluindo o novo jogo inserido, se a API não foi reiniciada).

3- Atualizar um jogo.
resposta = requests.put(f"{url_base}/atualizar/0", json=dado_atualizado)

4- Deletar um jogo.
resposta = requests.delete(f"{url_base}/deletar/0")
Remove o jogo de índice 0.

5- Listar as primeiras linhas.
resposta = requests.get(f"{url_base}/linhas/5")
Retorna as 5 primeiras partidas do dataset.

6- Consultar total de gols de um time.
resposta = requests.get(f"{url_base}/gols/Flamengo")
Informa quantos gols o Flamengo fez no total do histórico.

7- Consultar confrontos entre dois times.
resposta = requests.get(f"{url_base}/confronto?time1=Flamengo&time2=Palmeiras")
Lista todas as partidas entre Flamengo e Palmeiras.

8- Listar times de um estado.
resposta = requests.get(f"{url_base}/estado/RJ")
Mostra todos os times do estado do Rio de Janeiro (RJ).

9- Mostrar todos os jogos de um time.
resposta = requests.get(f"{url_base}/Time/Flamengo")
Lista todas as partidas em que o Flamengo jogou (em casa ou fora).

10- Buscar jogos com um número específico de gols.
resposta = requests.get(f"{url_base}/gols/3/valor")
Mostra jogos onde alguém marcou exatamente 3 gols (casa ou visitante).

*Datasets*

Brasileirao_Matches.csv: contém dados de partidas do Campeonato Brasileiro (Série A), incluindo informações como times mandante e visitante, número de gols, estádio, estado, data da partida, entre outros. Esse dataset permite diversas análises como confrontos entre times, total de gols marcados, distribuição de times por estado, e muito mais.

Libertadores_Matches.csv: reúne informações de partidas da Copa Libertadores da América, com estrutura semelhante ao dataset do Brasileirão. Ele também traz dados detalhados dos jogos, permitindo comparar desempenhos entre competições, analisar campanhas de times brasileiros na Libertadores, entre outras possibilidades.

Link: https://www.kaggle.com/datasets/ricardomattos05/brazilian-soccer-database?select=Libertadores_Matches.csv

*Front.html*

Bem, achamos mais 'divertido' fazer um front em HTML para testar a API de forma visual e interativa.
Em vez de usar apenas ferramentas como o Postman ou enviar requisições manualmente pelo terminal, quisemos montar algo mais prático e direto.
Com esse front, conseguimos simular todas as operações da API, como consultar, inserir, atualizar e deletar dados com apenas alguns cliques.
Além disso, foi uma boa oportunidade para aplicar e aprender sobre frontend.
No fim, ficou uma espécie de painel simples que agiliza bastante os testes e ainda deixa tudo mais intuitivo.









