"""
Problém obchodního cestujícího
    - minimalizace nákladů během cesty mezi všemi místy

1. vytvořit si malinký graf ve formě matice
2. vytvořit si populaci kandidátů na řešení
3. ohodnotit jedince fitness
"""

import random

mesta = [
    # Praha, Brno, Ostrava
    [0,250,320],    # Praha
    [30,0,15],    # Brno
    [29,14,0]     # Ostrava
]

def vytvor_kandidata():
    mista = [0,1,2]
    pop = [mista.copy() for _ in range(len(mista))]
    for i in range(len(pop)):
        random.shuffle(pop[i])
    return pop

def ohodnot_fitness(x):
    cena = 0
    for i in range(1, len(x)):
        cena += mesta[x[i-1]][x[i]]
    return cena

def klonovani(jedinec, pocet_klonu, pravdepodobnost_mutace):
    klonovani = [jedinec.copy() for _ in range(pocet_klonu)]
    for klon in klonovani:
        for i in range(len(klon)):
            if random.random() < pravdepodobnost_mutace:
                klon[i] = random.randint(0, 1)  # nahodna uprava genu
    return klonovani


for jedinec in vytvor_kandidata():
    print(jedinec, ohodnot_fitness(jedinec))