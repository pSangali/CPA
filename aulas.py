from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time, json, re

driver = webdriver.Chrome()

#acessa o site
driver.get('https://www.imdb.com/')
#menu->topico->subtopico
driver.find_element(By.ID, 'imdbHeader-navDrawerOpen').click()
time.sleep(1)
driver.find_element(By.XPATH, '//label[@aria-label="Expand TV Shows Nav Links"]').click()
time.sleep(1)
driver.find_element(By.XPATH, '//a[@href="/chart/toptv/?ref_=nv_tvv_250"]').click()
#feito chegada

#o CSS é bom pra qnd temos lista ou uma sequencia que nesse caso seria "ipc-meta..." o "li" é mais para especificar e evitar possiveis confusoes que o seletor poderia vir ter
sequencia_series = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")
#feito sequencia

series_list = []
for serie in sequencia_series[:250]:
    #o sub vai substituir os numeros e os espaços em brancos e deixara apenas o texto (titulo) que sera transformado em text e caso tenha espacos extra sera removido pelo strip
    titulo = re.sub(r'^\d+\.\s*', '', serie.find_element(By.CSS_SELECTOR, "h3").text.strip())
    link = serie.find_element(By.TAG_NAME, "a").get_attribute("href")

    ano, rating = None, None
    #o CSS comeca no 1 a contagem de filhos
    #aqui estamos acessando todas as classes que possuem ".cli..." e acessamos os valores do primeiro filho que nesse caso é o ano (assumindo um valor como lista)
    Ano = serie.find_elements(By.CSS_SELECTOR, ".cli-title-metadata-item:nth-child(1)")
    if Ano:
        #verifica um padrao especifico que nesse caso seria o valor de 4 digitos dentro de uma string
        match = re.search(r'(\d{4})', Ano[0].text)
        #transforma em um int
        if match: year = int(match.group(1))

    Rating = serie.find_elements(By.CSS_SELECTOR, ".ipc-rating-star--imdb")
    if Rating:
        match = re.search(r'(\d+[.,]\d+)', Rating[0].get_attribute("aria-label") or Rating[0].text)
        if match: rating = float(match.group(1).replace(',', '.'))

    series_list.append({
        "titulo": titulo, "ano_lancamento": ano,
        "nota_imdb": rating, "link": link
    })

#elenco
final_data = []
for i in series_list:
    driver.get(i["link"])
    time.sleep(3)

    pop, elenco, temp = None, [], None
    Pop = driver.find_elements(By.CSS_SELECTOR, "[data-testid='hero-rating-bar__popularity'] .sc-507c0d69-0")
    if Pop:
        match = re.search(r'(\d+)', Pop[0].text)
        if match: pop = int(match.group(1))

    lista_elenco = driver.find_elements(By.CSS_SELECTOR, "[data-testid='title-cast-item']")
    #no max 10 atores para nao ficar muito grande a lista
    for x in lista_elenco[:10]:
        actor = x.find_element(By.CSS_SELECTOR, "[data-testid='title-cast-item__actor']").text.strip()
        personagens = x.find_elements(By.CSS_SELECTOR, "[data-testid='title-cast-item__character']")
        #verifica se o nome do personagem foi encontrado
        character = personagens[0].text.strip() if personagens else "Character not specified"
        elenco.append({"ator": actor, "personagem": character})

    #pegua o cod fonte
    fonte = driver.page_source
    #meu sistema esta em ingles por isso coloquei em pt-br e ing para encontrar o num de temporadas
    for t in [r'(\d+)\s+season', r'(\d+)\s+temporada']:
        match = re.search(t, fonte, re.IGNORECASE)
        if match:
            temp = int(match.group(1))
            break

    i.update({"popularidade": pop, "elenco": elenco, "temporadas": temp})
    final_data.append(i)
    with open("top_250_series_imdb.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    time.sleep(2)

driver.quit()
