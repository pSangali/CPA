#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import re

# === CONFIGURAÇÃO DO WEBDRIVER ===
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Executa sem abrir janela
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# === FUNÇÃO AUXILIAR PARA LIMPAR TÍTULO E CONVERTER DADOS ===
def clean_data(title, year, episodes, rating):
    title = re.sub(r"\(\d{4}\)", "", title).strip()
    try:
        year = int(re.findall(r"\d{4}", year)[0])
    except:
        year = None
    try:
        episodes = int(re.sub(r"[^\d]", "", episodes))
    except:
        episodes = None
    try:
        rating = float(rating)
    except:
        rating = None
    return title, year, episodes, rating

# === ACESSA A LISTA DAS MELHORES SÉRIES ===
base_url = "https://www.imdb.com/chart/toptv/"
driver.get(base_url)
time.sleep(3)

series_data = []

rows = driver.find_elements(By.XPATH, '//tbody[@class="lister-list"]/tr')
print(f"Total de séries encontradas: {len(rows)}")

for row in rows:
    try:
        title_elem = row.find_element(By.XPATH, './/td[@class="titleColumn"]/a')
        title = title_elem.text
        link = title_elem.get_attribute("href")
        year = row.find_element(By.XPATH, './/span[@class="secondaryInfo"]').text
        rating = row.find_element(By.XPATH, './/td[@class="ratingColumn imdbRating"]/strong').text

        # Acessa a página da série para obter + detalhes
        driver.get(link)
        time.sleep(2)

        # Episódios
        try:
            episodes_text = driver.find_element(By.XPATH, '//section[contains(@data-testid, "Episodes")]').text
        except:
            episodes_text = "0"

        # Popularidade
        try:
            popularity_elem = driver.find_element(By.XPATH, '//div[contains(@data-testid, "hero-rating-bar__popularity__score")]')
            popularity = popularity_elem.text.strip()
        except:
            popularity = "N/A"

        # Elenco principal
        cast_list = []
        try:
            cast_section = driver.find_elements(By.XPATH, '//div[@data-testid="title-cast-item"]')[:5]
            for actor in cast_section:
                name = actor.find_element(By.XPATH, './/a').text
                try:
                    character = actor.find_element(By.XPATH, './/span[@class="ipc-metadata-list-item__list-content-item"]').text
                except:
                    character = "N/A"
                cast_list.append({
                    "actor": name,
                    "character": character
                })
        except:
            cast_list = []

        # Limpeza e conversões
        title, year, episodes, rating = clean_data(title, year, episodes_text, rating)

        series_data.append({
            "title": title,
            "year": year,
            "episodes": episodes,
            "rating": rating,
            "link": link,
            "popularity": popularity,
            "cast": cast_list
        })

        print(f"Coletado: {title}")
        driver.back()
        time.sleep(2)

    except Exception as e:
        print(f"Erro ao processar série: {e}")
        continue

# === SALVA EM JSON ===
with open("series_imdb.json", "w", encoding="utf-8") as f:
    json.dump(series_data, f, ensure_ascii=False, indent=4)

print("✅ Dados salvos em 'series_imdb.json'")
driver.quit()


# In[ ]:




