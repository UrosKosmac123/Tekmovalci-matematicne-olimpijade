import bs4
from bs4 import BeautifulSoup
import requests
import csv
import pandas

seznam_drzav = requests.get('https://www.imo-official.org/countries.aspx').text
soup_drzave = BeautifulSoup(seznam_drzav, 'lxml')

seznam_koncnic = []

def poisci_drzave():
    text = requests.get('https://www.imo-official.org/countries.aspx').text
    soup = bs4.BeautifulSoup(text, 'lxml')
    return [c.text for c in soup.select('#main tbody tr td:first-child')]

drzave = poisci_drzave()
print(drzave)

def poisci_tekmovalce():
    ctn = []
    col = ['leto', 'ime', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'empty', 'skupaj', 'absolutno_mesto', 'relativno_mesto', 'nagrada']

    def varen_int(val, default=None):
        try:
            return int(val)
        except ValueError:
            return default

    def varen_float(val, default=None):
        try:
            return float(val)
        except ValueError:
            return default

    def poberi_tekmovalce_row(row, drzava):
        tekmovalec = {'drzava': drzava }

        for i, cell in enumerate(row.findChildren('td', recursive=False)):
            t = cell.get_text(separator=' ')
            if i < len(col):
                tekmovalec[col[i]] = t

        is_male = tekmovalec["ime"].find("♂") > -1
        is_female = tekmovalec["ime"].find("♀") > -1
            
        tekmovalec["ime"] = tekmovalec["ime"].strip("♂♀ ")
        if is_male:
            tekmovalec["spol"] = "moški"
        elif is_female:
            tekmovalec["spol"] = "ženska"
        else:
            tekmovalec["spol"] = None

        tekmovalec["N1"] = varen_int(tekmovalec["N1"])
        tekmovalec["N2"] = varen_int(tekmovalec["N2"])
        tekmovalec["N3"] = varen_int(tekmovalec["N3"])
        tekmovalec["N4"] = varen_int(tekmovalec["N4"])
        tekmovalec["N5"] = varen_int(tekmovalec["N5"])
        tekmovalec["N6"] = varen_int(tekmovalec["N6"])
        tekmovalec["skupaj"] = varen_int(tekmovalec["skupaj"])
        tekmovalec["absolutno_mesto"] = varen_int(tekmovalec["absolutno_mesto"])
        tekmovalec["relativno_mesto"] = varen_float(tekmovalec["relativno_mesto"].strip("%"))
        tekmovalec.pop("empty")

        return tekmovalec

    for drzava in drzave:
        text = requests.get(f'https://www.imo-official.org/country_individual_r.aspx?code={drzava}&gender=show&nameform=western').text
        soup = bs4.BeautifulSoup(text, 'lxml')
        ctn += [poberi_tekmovalce_row(c, drzava) for c in soup.select('#main tbody tr')]

    with open('Zajem/podatki.csv', 'w', newline='') as file:
        podatki = ['drzava', 'leto', 'ime', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'empty', 'skupaj', 'absolutno_mesto', 'relativno_mesto', 'nagrada','spol']
        writer = csv.DictWriter(file, fieldnames=podatki)
        writer.writerows(ctn)

    #print(ctn)
    return ctn

tekmovalci = pandas.DataFrame(poisci_tekmovalce())
