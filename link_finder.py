import requests
from bs4 import BeautifulSoup
import os
import io

# URL inicial
url = "https://www.nomedosite.com"

# Inicializa a fila com a URL inicial
queue = [url]

# Armazena os sites visitados
visited = set()

# Nome do arquivo para armazenar os links
filename = "links.txt"

# Verifica se o arquivo já existe, se não existir cria um novo arquivo
if not os.path.exists(filename):
    open(filename, 'w').close()

# Função para escrever os links no arquivo de texto
def write_links(links):
    if links == None:
        print ("Busca finalizada.")
    else:
        with io.open(filename, 'a', encoding='utf-8') as f:
            for link in links:
                f.write(link + "\n")

# Loop principal
while queue:
    # Remove o primeiro site da fila
    url = queue.pop(0)

    # Verifica se o site já foi visitado, se já foi, pula para o próximo
    if url in visited:
        continue

    # Faz a requisição HTTP para o site
    response = requests.get(url)

    # Verifica se a requisição foi bem sucedida, se não foi, pula para o próximo
    if response.status_code != 200:
        continue

    # Adiciona o site aos sites visitados
    visited.add(url)

    # Extrai os links da página HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a')]

    # Escreve os links no arquivo de texto
    if links:
        write_links(links)
 
    # Adiciona os links à fila, excluindo os que já foram visitados
    for link in links:
        if link not in visited and link not in queue:
            queue.append(link)
