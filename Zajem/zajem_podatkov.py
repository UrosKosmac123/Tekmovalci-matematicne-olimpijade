from bs4 import BeautifulSoup
import requests
import csv

seznam_drzav = requests.get('https://www.imo-official.org/countries.aspx').text
soup_drzave = BeautifulSoup(seznam_drzav, 'lxml')

seznam_koncnic = []

def poisci_koncnice():
    drzave = soup_drzave.find_all('td',{'align':'center'})
    for drzava in drzave:
        seznam_koncnic.append(drzava.text)

#poisci_koncnice()
#print(seznam_koncnic)
#print(len(seznam_koncnic))

seznam_podatkov = []

def zapisi_podatke_tekmovalcev():
    tekmovalci = requests.get(f'https://www.imo-official.org/country_individual_r.aspx?code=FRA&column=year&order=desc&gender=hide').text
    soup_tekmovalci = BeautifulSoup(tekmovalci, 'lxml')
    podatki = soup_tekmovalci.find_all('tr')
    for podatek in podatki:
        seznam_podatkov.append(podatek.get_text(separator=' '))
      

zapisi_podatke_tekmovalcev()

nov_seznam_podatkov = []
for oseba in seznam_podatkov[2:]:
    podatki = oseba.split(' ')
    nov_seznam_podatkov.append(podatki)

seznam_let_od_1990_2020 = [] 

for podatek in nov_seznam_podatkov:
    if podatek[0] > '1989':
        seznam_let_od_1990_2020.append(podatek)
    else:
        pass

#print(seznam_let_od_1990_2020)

#for koncnica in seznam_koncnic:
#    tekmovalci = requests.get(f'https://www.imo-official.org/country_individual_r.aspx?code={koncnica}&column=year&order=desc&gender=hide').text
#    soup_tekmovalci = BeautifulSoup(tekmovalci, 'lxml')
#    print(soup_tekmovalci.prettify())

with open('Francija.csv', 'w', newline='') as file:
    zapisi = csv.writer(file, delimiter= ',')
    zapisi.writerows(seznam_let_od_1990_2020)

    
#with open('Francija.csv', 'w', newline='') as file:
#    podatki = ["leto","ime","priimek","N1","N2","N3","N4","N5","N6","N7","skupaj","absolutno mesto","relativno mesto","nagrada",]
#    writer = csv.DictWriter(file, fieldnames=podatki)
#    for row in seznam_podatkov:
#        writer.writerow(row)
