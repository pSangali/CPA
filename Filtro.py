import pandas as pd, numpy as np, matplotlib.pyplot as plt

#filtrar os datasest e possiveis perguntas

#le o dataset
brasil = pd.read_csv("DataSets/Brasileirao_Matches.csv")
#exclui colunas "inuteis", e exclui valores ausentes
brasil = brasil.drop(["season", "round"], axis=1).dropna()
#deixa só ano/mes/dia
brasil_ano = brasil["datetime"].map(lambda x: str(x)[:10])
#deixa só nome do time
brasil_times = brasil[["home_team", "away_team"]].map(lambda x: x[:-3])
#slado de gols
goals = brasil[["home_goal", "home_team_state", "away_goal", "away_team_state"]]
#junta tudo
brasil = pd.concat([brasil_ano, brasil_times, goals], axis=1)


#team = brasil[["home_team", "away_team"]]
#goals = brasil[["home_goal", "away_goal"]]
#team_goal = brasil_ano[["home_team","home_goal", "away_team", "away_goal"]]

#utilizar np para calcular e o plt para "mostrar" com os metodos para chamar dps
class Time:
    def __init__(self, brasil):
        self.brasil = brasil

    #me da o total de gols do time escolhido detodo o periodo
    def total_team_goals(self, team_name):
        gols_casa = int(np.sum(self.brasil[self.brasil['home_team'] == team_name]['home_goal']))
        gols_fora = int(np.sum(self.brasil[self.brasil['away_team'] == team_name]['away_goal']))
        total = gols_casa + gols_fora
        return {
            "time": team_name,
            "total_gols": total
        }

    # retorna as datas dos jogos entre 2 times
    def team(self, team_name1, team_name2):
        jogos = self.brasil[
            ((self.brasil['home_team'] == team_name1) & (self.brasil['away_team'] == team_name2)) |
            ((self.brasil['home_team'] == team_name2) & (self.brasil['away_team'] == team_name1))
            ]
        lista_jogos = [
            {
                "data": i["datetime"],
                "casa": i["home_team"],
                "gols_casa": int(i["home_goal"]),
                "fora": i["away_team"],
                "gols_fora": int(i["away_goal"])
            }
            for _, i in jogos.iterrows()
        ]
        return {
            "times": [team_name1, team_name2],
            "jogos": lista_jogos
        }

    # lista todos os times de um estado específico
    def state(self, estado):
        estado = estado.upper()
        times_casa = self.brasil[self.brasil['home_team_state'] == estado]['home_team']
        times_fora = self.brasil[self.brasil['away_team_state'] == estado]['away_team']
        times = sorted(set(pd.concat([times_casa, times_fora]).unique()))
        return {
            "estado": estado,
            "quantidade": len(times),
            "times": times
        }

    # retorna o número específico de gols de todos os times
    def mostraValor(self, value):
        value = int(value)
        jogos = self.brasil[(self.brasil['home_goal'] == value) | (self.brasil['away_goal'] == value)]
        lista_jogos = [
            {
                "data": i["datetime"],
                "casa": i["home_team"],
                "gols_casa": int(i["home_goal"]),
                "fora": i["away_team"],
                "gols_fora": int(i["away_goal"])
            }
            for _, i in jogos.iterrows()
        ]
        return {
            "gols_exatos": value,
            "jogos": lista_jogos
        }

    # mostra todos os jogos do time específico
    def mostraNome(self, team_name):
        jogos = self.brasil[(self.brasil['home_team'] == team_name) | (self.brasil['away_team'] == team_name)]
        lista_jogos = [
            {
                "Adata": i["datetime"],
                "casa": i["home_team"],
                "gols_casa": int(i["home_goal"]),
                "fora": i["away_team"],
                "gols_fora": int(i["away_goal"])
            }
            for _, i in jogos.iterrows()
        ]
        return {"jogos": lista_jogos}

    #retorna as n linhas que o usario queira do dataset
    def mostraLinhas(self, n):
        n = int(n)
        linhas = self.brasil.head(n)
        lista_linhas = [
            {
                "adata": i["datetime"],
                "casa": i["home_team"],
                "gols_casa": int(i["home_goal"]),
                "estado_casa": i["home_team_state"],
                "fora": i["away_team"],
                "gols_fora": int(i["away_goal"]),
                "estado_fora": i["away_team_state"]
            }
            for _, i in linhas.iterrows()
        ]
        return {
            "quantidade": n,
            "jogos": lista_linhas
        }


#print(Time(brasil).total_team_goals("Gremio"))
#print(Time(brasil).team("Internacional", "Gremio"))
#print(Time(brasil).state("sp"))
#print(Time(brasil).mostraNome("Gremio"))
#print(Time(brasil).mostraValor(6))
#print(Time(brasil).mostraLinhas(10))
