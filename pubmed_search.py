import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os

author_name = input("Digite o nome do autor: ")

search_term = author_name.replace(" ", "+")

try:
    page = requests.get(
    "https://pubmed.ncbi.nlm.nih.gov/?term="+search_term+"&size=200")
except:
    print("Muito provavelmente o site está bloqueando suas chamadas, execute novamente daqui 4 minutos.")

soup = BeautifulSoup(page.content, 'html.parser')


all_articles = []

total_elements = soup.find(class_="results-amount").find(class_="value").get_text()

pagination = soup.find(class_ = "page-number-wrapper")
total_pages = soup.find(class_ = "of-total-pages").get_text().replace("of ", "")

print("Total de elementos encontrados: " + total_elements)
print("Aguarde a execução do script...")
for page in range(0, int(total_pages)):
    page = requests.get(
    "https://pubmed.ncbi.nlm.nih.gov/?term="+search_term+"&size=200&&page="+str(page+1))
    soup = BeautifulSoup(page.content, 'html.parser')
    articles = soup.find_all(class_='docsum-content')

    for article in articles:
        title = article.find(class_='docsum-title').get_text().replace("\n", "").replace("                ", "").replace("              ","")
        citation = article.find(class_='docsum-journal-citation full-journal-citation').get_text()

        doi = ""
        citation_elements = list(filter(lambda el: "doi" in el, citation.split(". ")))

        if len(citation_elements) > 0:
            doi = citation_elements[0].replace("doi: ", "")
        else:
            doi = "Doi Não informado"

        all_articles.append([title, doi])
       

folderpath = os.path.expanduser("~") + "\Documents\pesquisas_pubmed"
if not os.path.exists(folderpath):
    os.makedirs(folderpath)
    print('Created:', folderpath)

file_name = folderpath + "\-" +search_term + "-" + datetime.now().strftime("%d_%m_%Y_%H_%M") + ".csv"
for article in all_articles:
     with open(file_name, 'w', newline='',encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        
        writer.writerow(['Titulo', 'DOI'])
        writer.writerows(all_articles)

print("Arquivo salvo: "+ file_name)

input("Pressione ENTER para continuar")
