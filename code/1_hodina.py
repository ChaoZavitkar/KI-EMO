predmety = {
    "ps5": {"cena": 10000, "vaha": 2},
    "tv": {"cena": 5000, "vaha": 5},
    "laptop": {"cena": 10000, "vaha": 5},
    "monitor": {"cena": 2000, "vaha": 2},
    "konektor": {"cena": 100, "vaha": 1},
    "kabel": {"cena": 100, "vaha": 1},
}

import random

def create_binary_candidate(length):
    return [random.choice([0, 1]) for _ in range(length)]

# 1 = předmět byl ukraden, 0 = předmět nebyl ukraden
alpha = create_binary_candidate(len(predmety))
print(alpha)

def fitness_function(x, bp_max):
    fitness = 0
    sumvaha = 0
    for i in range(len(x)):
        sum(x)
        sumvaha += predmety[list(predmety.keys())[i]]["vaha"]
    print(x)
    if sumvaha <= bp_max:
        fitness = sum(x)
    return fitness

def gamma(alpha):
    x = [predmety[list(predmety.keys())[i]]["cena"] for i in range(len(alpha)) if alpha[i] == 1]
    return x

print(gamma(alpha))

alpha_fitness = fitness_function(gamma(alpha), 10)
print(alpha_fitness)

