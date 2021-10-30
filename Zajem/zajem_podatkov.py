from bs4 import BeautifulSoup
import requests

seznam_drzav = requests.get('https://www.imo-official.org/countries.aspx').text
soup_drzave = BeautifulSoup(seznam_drzav, 'lxml')

seznam_koncnic = []

def poisci_koncnice():
    drzave = soup_drzave.find_all('td',{'align':'center'})
    for drzava in drzave:
        seznam_koncnic.append(drzava.text)
        #print(drzava.text)

#poisci_koncnice()
#print(seznam_koncnic)
#print(len(seznam_koncnic))

seznam_podatkov = []

def zapisi_podatke_tekmovalcev():
    tekmovalci = requests.get(f'https://www.imo-official.org/country_individual_r.aspx?code=FRA&column=year&order=desc&gender=hide').text
    soup_tekmovalci = BeautifulSoup(tekmovalci, 'lxml')
    podatki = soup_tekmovalci.find_all('tr', class_ = 'imp')
    for podatek in podatki:
        seznam_podatkov.append(podatek.get_text(separator=' '))


zapisi_podatke_tekmovalcev()
print(seznam_podatkov)

#print(soup_tekmovalci.prettify())

#for koncnica in seznam_koncnic:
#    tekmovalci = requests.get(f'https://www.imo-official.org/country_individual_r.aspx?code={koncnica}&column=year&order=desc&gender=hide').text
#    soup_tekmovalci = BeautifulSoup(tekmovalci, 'lxml')
#    print(soup_tekmovalci.prettify())
