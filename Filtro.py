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
        gols_casa = np.sum(self.brasil[brasil['home_team'] == team_name]['home_goal'])
        gols_fora = np.sum(self.brasil[brasil['away_team'] == team_name]['away_goal'])
        return f"Quantidade total de gols do {team_name} foi de {int(gols_casa + gols_fora)}"

    # retorna as datas dos jogos entre 2 times
    def team(self, team_name1, team_name2):
        jogos = self.brasil[
            ((self.brasil['home_team'] == team_name1) & (self.brasil['away_team'] == team_name2)) |
            ((self.brasil['home_team'] == team_name2) & (self.brasil['away_team'] == team_name1))
            ]
        jogos_formatados = [
            f"{i['datetime']}: {i['home_team']} {int(i['home_goal'])} x {int(i['away_goal'])} {i['away_team']}"
            for _, i in jogos.iterrows()
        ]
        return f"As partidas entre {team_name1} e {team_name2} foram:\n" + "\n".join(jogos_formatados)

    # lista todos os times de um estado específico
    def state(self, estado):
        estado = estado.upper()
        times_casa = self.brasil[self.brasil['home_team_state'] == estado]['home_team']
        times_fora = self.brasil[self.brasil['away_team_state'] == estado]['away_team']

        # concatena os times e remove duplicatas com unique()
        times = pd.concat([times_casa, times_fora]).unique()

        return f"Os times que têm como origem {estado} são {len(times)}: \n" + "\n".join(sorted(times))

    # retorna o número específico de gols de todos os times
    def mostraValor(self, value):
        value = int(value)  # garante que seja número
        jogos = self.brasil[(self.brasil['home_goal'] == value) | (self.brasil['away_goal'] == value)]
        jogos_formatados = [
            f"{i['datetime']}: {i['home_team']} {int(i['home_goal'])} x {int(i['away_goal'])} {i['away_team']}"
            for _, i in jogos.iterrows()
        ]
        return f"Os jogos com exatamente {value} gols foram:\n" + "\n".join(jogos_formatados)

    # mostra todos os jogos do time específico
    def mostraNome(self, team_name):
        jogos = self.brasil[(self.brasil['home_team'] == team_name) | (self.brasil['away_team'] == team_name)]
        nome_formatados = [
            f'data {i["datetime"]}: {i["home_team"]} {int(i["home_goal"])} x {i["away_team"]} {int(i["away_goal"])}'
            for _, i  in jogos.iterrows()  
        ]
        return f"Os jogos do {team_name} foram \n"  + "\n".join(nome_formatados)

#print(Time(brasil).total_team_goals("Gremio"))
#print(Time(brasil).team("Internacional", "Gremio"))
#print(Time(brasil).state("sp"))
#print(Time(brasil).mostraNome("Gremio"))
#print(Time(brasil).mostraValor(6))
