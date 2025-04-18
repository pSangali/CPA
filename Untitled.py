from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import json
import re
import traceback
from bs4 import BeautifulSoup
import requests


def configurar_driver():
    """Configura e retorna o driver do Chrome."""
    print("Configurando o driver...")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Adicionar user-agent para evitar detecção de bot
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    print("Tentando inicializar o Chrome...")
    driver = webdriver.Chrome(options=chrome_options)
    print("Chrome inicializado com sucesso!")
    return driver


def extrair_com_requests():
    """Tenta extrair dados usando o requests e BeautifulSoup."""
    print("Tentando extrair dados com requests e BeautifulSoup...")

    # Headers para simular um navegador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive',
        'DNT': '1',
    }

    url = "https://www.imdb.com/chart/top/"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Falha ao acessar a página: Status code {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')

        # Procurar os elementos dos filmes
        filmes_list = []

        # Tentar diferentes padrões de HTML
        filme_elements = soup.select("li.ipc-metadata-list-summary-item") or soup.select(".lister-list tr")

        for idx, filme_element in enumerate(filme_elements[:250], 1):
            try:
                # Extrair título
                if soup.select("li.ipc-metadata-list-summary-item"):
                    # Novo layout
                    titulo_element = filme_element.select_one("h3") or filme_element.select_one(".ipc-title__text")
                    titulo_completo = titulo_element.text.strip() if titulo_element else "Título não encontrado"
                else:
                    # Layout antigo
                    titulo_element = filme_element.select_one(".titleColumn a")
                    titulo_completo = titulo_element.text.strip() if titulo_element else "Título não encontrado"

                # Remover a numeração do início do título
                titulo = re.sub(r'^\d+\.\s*', '', titulo_completo)

                # Extrair link
                if soup.select("li.ipc-metadata-list-summary-item"):
                    link_element = filme_element.select_one("a")
                else:
                    link_element = filme_element.select_one(".titleColumn a")

                link = link_element["href"] if link_element else ""
                if link and not link.startswith("http"):
                    link = f"https://www.imdb.com{link}"

                # Extrair ano
                ano = None
                if soup.select("li.ipc-metadata-list-summary-item"):
                    ano_element = filme_element.select_one(".cli-title-metadata-item:nth-child(1)")
                    if ano_element:
                        ano_match = re.search(r'(\d{4})', ano_element.text)
                        if ano_match:
                            ano = int(ano_match.group(1))
                else:
                    ano_element = filme_element.select_one(".titleColumn .secondaryInfo")
                    if ano_element:
                        ano_match = re.search(r'(\d{4})', ano_element.text)
                        if ano_match:
                            ano = int(ano_match.group(1))

                # Extrair nota
                nota = None
                if soup.select("li.ipc-metadata-list-summary-item"):
                    nota_element = filme_element.select_one(".ipc-rating-star--imdb")
                    if nota_element:
                        nota_text = nota_element.get("aria-label", "") or nota_element.text
                        nota_match = re.search(r'(\d+[.,]\d+)', nota_text)
                        if nota_match:
                            nota = float(nota_match.group(1).replace(',', '.'))
                else:
                    nota_element = filme_element.select_one(".ratingColumn strong")
                    if nota_element:
                        nota = float(nota_element.text.replace(',', '.'))

                filme_info = {
                    "titulo": titulo.strip(),
                    "ano_estreia": ano,
                    "nota_imdb": nota,
                    "link": link
                }

                filmes_list.append(filme_info)
                print(f"[{idx}/250] Processado filme: {titulo}")

            except Exception as e:
                print(f"Erro ao processar filme #{idx}: {str(e)}")

        return filmes_list

    except Exception as e:
        print(f"Erro ao extrair com requests: {str(e)}")
        traceback.print_exc()
        return []


def extrair_detalhes_filme_requests(filme):
    """Extrai detalhes adicionais da página específica de um filme usando requests."""
    if not filme["link"]:
        filme["popularidade"] = None
        filme["elenco"] = []
        return filme

    print(f"Acessando página do filme: {filme['titulo']}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }

    try:
        time.sleep(1)  # Pausa para evitar bloqueio
        response = requests.get(filme["link"], headers=headers)

        if response.status_code != 200:
            print(f"Falha ao acessar a página: Status code {response.status_code}")
            filme["popularidade"] = None
            filme["elenco"] = []
            return filme

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extrair popularidade
        popularidade = None
        popularidade_patterns = [
            r'Popularity\s*(\d+)',
            r'popularidade\s*(\d+)',
            r'Classificado com\s*#(\d+)',
            r'Ranked\s*#(\d+)'
        ]

        for pattern in popularidade_patterns:
            match = re.search(pattern, response.text, re.IGNORECASE)
            if match:
                popularidade = int(match.group(1))
                print(f"Popularidade encontrada: {popularidade}")
                break

        # Tentar extrair via seletores específicos se o regex falhar
        if not popularidade:
            popularidade_selectors = [
                "[data-testid='hero-rating-bar__popularity'] .sc-507c0d69-0",
                ".sc-5f7fb5b4-1",
                ".popularity",
                ".trending-today"
            ]

            for selector in popularidade_selectors:
                popularidade_elem = soup.select_one(selector)
                if popularidade_elem:
                    popularidade_text = popularidade_elem.text
                    popularidade_match = re.search(r'(\d+)', popularidade_text)
                    if popularidade_match:
                        popularidade = int(popularidade_match.group(1))
                        print(f"Popularidade encontrada via seletor: {popularidade}")
                        break

        # Extrair elenco principal
        elenco = []

        # Tentar diferentes seletores para o elenco
        elenco_patterns = [
            ".sc-bfec09a1-5",
            ".cast_list tr",
            "[data-testid='title-cast-item']",
            ".primary_photo",
            ".cast-item"
        ]

        for pattern in elenco_patterns:
            elenco_elements = soup.select(pattern)
            if elenco_elements:
                print(f"Encontrados {len(elenco_elements)} elementos de elenco com padrão {pattern}")

                for ator_element in elenco_elements[:10]:  # Limitar aos 10 primeiros
                    try:
                        # Tentar diferentes padrões para nome do ator
                        nome_ator = None
                        ator_patterns = [
                            ".sc-bfec09a1-1",
                            ".actor",
                            "[data-testid='title-cast-item__actor']",
                            "a img"
                        ]

                        for p in ator_patterns:
                            actor_elem = ator_element.select_one(p)
                            if actor_elem:
                                # Para imagens, pegar o atributo alt
                                if actor_elem.name == "img" and actor_elem.get("alt"):
                                    nome_ator = actor_elem["alt"].strip()
                                else:
                                    nome_ator = actor_elem.text.strip()

                                if nome_ator:
                                    break

                        # Tentar pelo elemento a
                        if not nome_ator:
                            a_elem = ator_element.select_one("a")
                            if a_elem:
                                nome_ator = a_elem.text.strip()

                        if not nome_ator:
                            continue

                        # Tentar diferentes padrões para personagem
                        nome_personagem = "Personagem não especificado"
                        personagem_patterns = [
                            ".sc-bfec09a1-3",
                            ".character",
                            "[data-testid='title-cast-item__character']",
                            ".character a"
                        ]

                        for p in personagem_patterns:
                            personagem_elem = ator_element.select_one(p)
                            if personagem_elem:
                                texto = personagem_elem.text.strip()
                                if texto:
                                    nome_personagem = texto
                                    break

                        elenco.append({
                            "ator": nome_ator,
                            "personagem": nome_personagem
                        })

                    except Exception as e:
                        print(f"Erro ao processar ator: {str(e)}")

                # Se encontramos elenco com esse padrão, paramos
                if elenco:
                    break

        # Adicionar detalhes ao filme
        filme["popularidade"] = popularidade
        filme["elenco"] = elenco

        print(f"Concluída extração de detalhes para: {filme['titulo']}")
        return filme

    except Exception as e:
        print(f"Erro ao processar detalhes do filme {filme['titulo']}: {str(e)}")
        traceback.print_exc()
        filme["popularidade"] = None
        filme["elenco"] = []
        return filme


def extrair_top_250_filmes_selenium(driver):
    """Extrai informações dos 250 filmes mais bem avaliados do IMDB usando Selenium."""
    print("Acessando a página de Top 250 filmes com Selenium...")
    try:
        driver.get("https://www.imdb.com/chart/top/")
        print("Página carregada. Aguardando elementos...")

        # Espera mais longa para carregar completamente
        time.sleep(5)

        # Converter o HTML para BeautifulSoup para análise mais flexível
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Tentar diversos padrões
        filme_elements = soup.select("li.ipc-metadata-list-summary-item") or soup.select(".lister-list tr")
        print(f"Encontrados {len(filme_elements)} elementos de filmes")

        if not filme_elements:
            print("Nenhum elemento de filme encontrado. Verificando HTML.")
            return []

        filmes_list = []
        for idx, filme_element in enumerate(filme_elements[:250], 1):
            try:
                # Extrair título
                if soup.select("li.ipc-metadata-list-summary-item"):
                    # Novo layout
                    titulo_element = filme_element.select_one("h3") or filme_element.select_one(".ipc-title__text")
                    titulo_completo = titulo_element.text.strip() if titulo_element else "Título não encontrado"
                else:
                    # Layout antigo
                    titulo_element = filme_element.select_one(".titleColumn a")
                    titulo_completo = titulo_element.text.strip() if titulo_element else "Título não encontrado"

                # Remover a numeração do início do título
                titulo = re.sub(r'^\d+\.\s*', '', titulo_completo)

                # Extrair link
                if soup.select("li.ipc-metadata-list-summary-item"):
                    link_element = filme_element.select_one("a")
                else:
                    link_element = filme_element.select_one(".titleColumn a")

                link = link_element["href"] if link_element else ""
                if link and not link.startswith("http"):
                    link = f"https://www.imdb.com{link}"

                # Extrair ano
                ano = None
                if soup.select("li.ipc-metadata-list-summary-item"):
                    ano_element = filme_element.select_one(".cli-title-metadata-item:nth-child(1)")
                    if ano_element:
                        ano_match = re.search(r'(\d{4})', ano_element.text)
                        if ano_match:
                            ano = int(ano_match.group(1))
                else:
                    ano_element = filme_element.select_one(".titleColumn .secondaryInfo")
                    if ano_element:
                        ano_match = re.search(r'(\d{4})', ano_element.text)
                        if ano_match:
                            ano = int(ano_match.group(1))

                # Extrair nota
                nota = None
                if soup.select("li.ipc-metadata-list-summary-item"):
                    nota_element = filme_element.select_one(".ipc-rating-star--imdb")
                    if nota_element:
                        nota_text = nota_element.get("aria-label", "") or nota_element.text
                        nota_match = re.search(r'(\d+[.,]\d+)', nota_text)
                        if nota_match:
                            nota = float(nota_match.group(1).replace(',', '.'))
                else:
                    nota_element = filme_element.select_one(".ratingColumn strong")
                    if nota_element:
                        nota = float(nota_element.text.replace(',', '.'))

                filme_info = {
                    "titulo": titulo.strip(),
                    "ano_estreia": ano,
                    "nota_imdb": nota,
                    "link": link
                }

                filmes_list.append(filme_info)
                print(f"[{idx}/250] Processado filme: {titulo}")

            except Exception as e:
                print(f"Erro ao processar filme #{idx}: {str(e)}")

        return filmes_list

    except Exception as e:
        print(f"Erro ao extrair lista de filmes: {str(e)}")
        traceback.print_exc()
        return []


def main():
    """Função principal que orquestra o processo de scraping."""
    print("Iniciando o processo de scraping do IMDB...")
    driver = None
    ARQUIVO_FINAL = "top_250_filmes_imdb.json"

    try:
        # Primeiro tentar com requests e BeautifulSoup
        filmes = extrair_com_requests()

        # Se não obtiver resultados, tentar com Selenium
        if not filmes:
            print("Tentando extrair com Selenium...")
            driver = configurar_driver()
            filmes = extrair_top_250_filmes_selenium(driver)

        print(f"Extraídos {len(filmes)} filmes da lista Top 250")

        if not filmes:
            print("Não foi possível extrair dados dos filmes. Verifique a estrutura do site ou a conexão.")
            return

        # Extrair detalhes adicionais de cada filme
        filmes_completos = []
        for idx, filme in enumerate(filmes, 1):
            print(f"\n[{idx}/{len(filmes)}] Extraindo detalhes para: {filme['titulo']}")
            filme_completo = extrair_detalhes_filme_requests(filme)
            filmes_completos.append(filme_completo)

            # Salvar o arquivo completo a cada filme processado
            # Isso garante que sempre teremos a versão mais atualizada
            with open(ARQUIVO_FINAL, "w", encoding="utf-8") as f:
                json.dump(filmes_completos, f, ensure_ascii=False, indent=4)

            print(f"Progresso salvo: {idx}/{len(filmes)} filmes processados")

            # Pausa para evitar sobrecarga no servidor
            time.sleep(2)

        print(f"Processo concluído! Os dados foram salvos em '{ARQUIVO_FINAL}'")

    except Exception as e:
        print(f"Erro durante o processo de scraping: {str(e)}")
        traceback.print_exc()

    finally:
        # Fechar o driver se foi inicializado
        if driver:
            print("Fechando o navegador...")
            try:
                driver.quit()
                print("Navegador fechado com sucesso.")
            except Exception as e:
                print(f"Erro ao fechar o navegador: {str(e)}")


if __name__ == "__main__":
    main()