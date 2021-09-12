import requests
from bs4 import BeautifulSoup
from time import sleep
import os

def pokupi_imena(stranica):
    page = requests.get(stranica)
    soup = BeautifulSoup(page.content, "html.parser", from_encoding="utf-8")
    sadrzaj = soup.find("div", {"class": "content"})
    imena = sadrzaj.find_all('strong')
    
    for ime in imena:
        ime = ime.text
        ime = ime.replace("•", "")
        if ime == u'\xa0':
            continue
        ime = ime.replace(",","")
        ime = ime.strip().capitalize()
        if not any(x in ime.upper() for x in ['TROJKE' ,'BLIZANCI', 'DEČACI','DEVOJČICE']):
            prikupljena_imena[ime] = prikupljena_imena.get(ime, 0) + 1

def pronadji_stranice_sa_imenima():
    URL = "https://www.mojnovisad.com/tag/imena-beba/"
    BASE_URL = "https://www.mojnovisad.com"
    trazeni_deo_naslova = "MATIČNA KNJIGA ROĐENIH"

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    clanci = soup.find_all("div", {"class": "highlight"})
    for brojac, clanak in enumerate(clanci):
        if clanak.text.strip()[:22] == trazeni_deo_naslova:
            stranica = BASE_URL + clanak.find_next('a')['href']
            pokupi_imena(stranica)
            sleep(1)
            print(f'{brojac}.Radim stranicu: {stranica}')

def napravi_csv(putanja, imena):
    with open(os.path.expanduser(putanja), 'w', encoding="utf-8") as f:
        [f.write('{0},{1}\n'.format(key, value)) for key, value in imena.items()]

if __name__ == "__main__":
    prikupljena_imena = {}
    pronadji_stranice_sa_imenima()
    prikupljena_imena = dict(sorted(prikupljena_imena.items(), key=lambda item: item[1], reverse=True))
    napravi_csv('~/Desktop/imena.csv', prikupljena_imena)
 
