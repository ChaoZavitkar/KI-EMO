"""
Problém obchodního cestujícího
    - minimalizace nákladů během cesty mezi všemi místy

1. vytvořit si malinký graf ve formě matice
2. vytvořit si populaci kandidátů na řešení
3. ohodnotit jedince fitness
"""

import random

# Graf ve formě matice
mesta = [
    # Praha, Brno, Ostrava
    [0, 250, 320],  # Praha
    [30, 0, 15],    # Brno
    [29, 14, 0]     # Ostrava
]

def vytvor_kandidata(velikost_populace):
    mista = list(range(len(mesta)))
    populace = []
    for _ in range(velikost_populace):
        jedinec = mista.copy()
        random.shuffle(jedinec)
        populace.append(jedinec)
    return populace

def ohodnot_fitness(trasa):
    cena = 0
    # Projdeme všechna města v trase a počítáme náklady cesty
    for i in range(len(trasa)):
        aktualni_mesto = trasa[i]
        dalsi_mesto = trasa[(i + 1) % len(trasa)]
        cena += mesta[aktualni_mesto][dalsi_mesto]
    return cena

def klonovani(jedinec, pocet_klonu, pravdepodobnost_mutace):
    klony = []
    for _ in range(pocet_klonu):
        klon = jedinec.copy()
        if random.random() < pravdepodobnost_mutace:
            # Mutace (swap dvou náhodných měst v trase)
            i, j = random.sample(range(len(klon)), 2)
            klon[i], klon[j] = klon[j], klon[i]
        klony.append(klon)
    return klony

# Nastavení velikosti populace
velikost_populace = 10

# Vytvoření populace kandidátů
populace = vytvor_kandidata(velikost_populace)

# Ohodnocení fitness a tisk výsledků
for jedinec in populace:
    fitness = ohodnot_fitness(jedinec)
    print(jedinec, fitness)
