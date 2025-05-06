import pandas as pd, numpy as np

class Time:
    def __init__(self):
        brasil = pd.read_csv("DataSets/Brasileirao_Matches.csv")
        brasil = brasil.drop(["season", "round"], axis=1).dropna()
        brasil_ano = brasil["datetime"].map(lambda x: str(x)[:10])
        brasil_times = brasil[["home_team", "away_team"]].map(lambda x: x[:-3])
        goals = brasil[["home_goal", "home_team_state", "away_goal", "away_team_state"]]
        brasil = pd.concat([brasil_ano, brasil_times, goals], axis=1)

        self.brasil = brasil

    def total_team_goals(self, team_name):
        "me da o total de gols do time escolhido detodo o periodo"
        gols_casa = int(np.sum(self.brasil[self.brasil['home_team'] == team_name]['home_goal']))
        gols_fora = int(np.sum(self.brasil[self.brasil['away_team'] == team_name]['away_goal']))
        total = gols_casa + gols_fora
        return {
            "time": team_name,
            "total_gols": total
        }


    def team(self, team_name1, team_name2):
        "retorna as datas dos jogos entre 2 times"
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


    def state(self, estado):
        "lista todos os times de um estado específico"
        estado = estado.upper()
        times_casa = self.brasil[self.brasil['home_team_state'] == estado]['home_team']
        times_fora = self.brasil[self.brasil['away_team_state'] == estado]['away_team']
        times = sorted(set(pd.concat([times_casa, times_fora]).unique()))
        return {
            "estado": estado,
            "quantidade": len(times),
            "times": times
        }


    def mostraValor(self, value):
        "retorna o número específico de gols de todos os times"
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


    def mostraNome(self, team_name):
        " mostra todos os jogos do time específico"
        jogos = self.brasil[(self.brasil['home_team'] == team_name) | (self.brasil['away_team'] == team_name)]
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
        return {"jogos": lista_jogos}


    def mostraLinhas(self, n):
        "retorna as n linhas que o usario queira do dataset"
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

    def inserir_dado(self, novo_dado):
        "Adiciona um novo jogo ao DataFrame"
        df_novo = pd.DataFrame([novo_dado])
        self.brasil = pd.concat([self.brasil, df_novo], ignore_index=True)
        return {"mensagem": "Dado inserido com sucesso", "dado": novo_dado}

    def atualizar_dado(self, indice, dado_atualizado):
        "Atualiza um jogo existente por índice"
        if indice < 0 or indice >= len(self.brasil):
            return {"erro": "Índice inválido"}
        for chave, valor in dado_atualizado.items():
            if chave in self.brasil.columns:
                self.brasil.at[indice, chave] = valor
        return {"mensagem": "Dado atualizado com sucesso", "dado": self.brasil.iloc[indice].to_dict()}

    def deletar_dado(self, indice):
        "Remove um jogo por índice"
        if indice < 0 or indice >= len(self.brasil):
            return {"erro": "Índice inválido"}
        dado_removido = self.brasil.iloc[indice].to_dict()
        self.brasil = self.brasil.drop(index=indice).reset_index(drop=True)
        return {"mensagem": "Dado deletado com sucesso", "dado": dado_removido}

    def listar_dados(self):
        "Retorna todos os dados como lista de dicionários"
        return self.brasil.to_dict(orient='records')

    def filtrar_dados(self, filtros):
        df_filtrado = self.brasil.copy()
        for chave, valor in filtros.items():
            if chave in df_filtrado.columns:
                df_filtrado = df_filtrado[df_filtrado[chave] == valor]
        return df_filtrado.to_dict(orient="records")

#print(Time(brasil).total_team_goals("Gremio"))
#print(Time(brasil).team("Internacional", "Gremio"))
#print(Time(brasil).state("sp"))
#print(Time(brasil).mostraNome("Gremio"))
#print(Time(brasil).mostraValor(6))
#print(Time(brasil).mostraLinhas(10))
