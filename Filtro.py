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
goals = brasil[["home_goal", "home_team_state", "away_goal","away_team_state"]]
#junta tudo
brasil = pd.concat([brasil_ano, brasil_times,goals], axis=1)

#team = brasil[["home_team", "away_team"]]
#goals = brasil[["home_goal", "away_goal"]]
#team_goal = brasil_ano[["home_team","home_goal", "away_team", "away_goal"]]

#utilizar np para calcular e o plt para "mostrar" com os metodos para chamar dps
class Time:
    def __init__(self, brasil):
        self.brasil = brasil

    #me da o total de gols do time escolhido
    def total_team_goals(self, team_name):
        gols_casa = np.sum(self.brasil[brasil['home_team'] == team_name]['home_goal'])
        gols_fora = np.sum(self.brasil[brasil['away_team'] == team_name]['away_goal'])
        return int(gols_casa + gols_fora)

    #retorna as datas dos jogos entre 2 times
    def team(self, team_name, team_name2):
        pass

    #

print("gols: ",Time(brasil).total_team_goals("Sao Paulo"))


