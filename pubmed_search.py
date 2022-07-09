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


pagination = soup.find(class_ = "page-number-wrapper")
total_pages = soup.find(class_ = "of-total-pages").get_text().replace("of ", "")
print("Total de elementos encontrados: " + str(int(total_pages) * 200))
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
       

file_name = os.path.expanduser("~") + "\Documents\pumed" + "\-" +search_term + "-" + datetime.now().strftime("%d_%m_%Y_%H_%M") + ".csv"
for article in all_articles:
     with open(file_name, 'w', newline='',encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        
        writer.writerow(['Titulo', 'DOI'])
        writer.writerows(all_articles)

print("Arquivo salvo: "+ file_name)
