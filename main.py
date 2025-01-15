import math
from collections import Counter

def tokenizacja(tekst):
    znaki_interpunkcyjne = '"!#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    tekst = ''.join(znak for znak in tekst if znak not in znaki_interpunkcyjne)
    return tekst.lower().split()

def oblicz_prawdopodobienstwo(tokeny_dokumentu, tokeny_zapytania, tokeny_korpusu, lambda_=0.5):
    licznik_dokumentu = Counter(tokeny_dokumentu)
    licznik_korpusu = Counter(tokeny_korpusu)
    dlugosc_dokumentu = len(tokeny_dokumentu)
    dlugosc_korpusu = len(tokeny_korpusu)

    prawdopodobienstwo = 0
    for token in tokeny_zapytania:
        prawd_dokumentu = licznik_dokumentu[token] / dlugosc_dokumentu if dlugosc_dokumentu > 0 else 0
        prawd_korpusu = licznik_korpusu[token] / dlugosc_korpusu if dlugosc_korpusu > 0 else 0
        prawd_gladkie = lambda_ * prawd_dokumentu + (1 - lambda_) * prawd_korpusu

        if prawd_gladkie > 0:
            prawdopodobienstwo += math.log(prawd_gladkie)
        else:
            prawdopodobienstwo += -math.inf

    return prawdopodobienstwo

def szeregowanie_dokumentow(dokumenty, zapytanie, lambda_=0.5):
    tokeny_zapytania = tokenizacja(zapytanie)
    tokeny_dokumentow = [tokenizacja(dokument) for dokument in dokumenty]

    tokeny_korpusu = [token for dokument in tokeny_dokumentow for token in dokument]

    wyniki = []
    for i, tokeny_dokumentu in enumerate(tokeny_dokumentow):
        wynik = oblicz_prawdopodobienstwo(tokeny_dokumentu, tokeny_zapytania, tokeny_korpusu, lambda_)
        wyniki.append((i, wynik))

    wyniki = sorted(wyniki, key=lambda x: (-x[1], x[0]))

    return [indeks for indeks, _ in wyniki]

if __name__ == "__main__":
    n = int(input().strip())
    dokumenty = [input().strip() for _ in range(n)]
    zapytanie = input().strip()

    wynik = szeregowanie_dokumentow(dokumenty, zapytanie)
    print(wynik)

