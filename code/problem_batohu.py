import random

# Funkce pro generování náhodného předmětu
def generate_random_item():
    # Náhodný název předmětu (např. "předmět1", "předmět2", atd.)
    name = f"předmět{random.randint(1, 1000)}"
    # Náhodná cena mezi 100 a 10000
    cena = random.randint(100, 10000)
    # Náhodná hmotnost mezi 1 a 10
    vaha = random.uniform(0.5, 5)
    return name, {"cena": cena, "vaha": round(vaha, 2)}

# Generování více předmětů
def generate_items(num_items):
    predmety = {}
    for _ in range(num_items):
        name, details = generate_random_item()
        predmety[name] = details
    return predmety

# Generování 20 náhodných předmětů
num_items = 20
predmety = generate_items(num_items)

# Vytištění vygenerovaných předmětů
for name, details in predmety.items():
    print(f"{name}: Cena = {details['cena']}, Váha = {details['vaha']}")


# Parametry genetického algoritmu
populace_size = 5
generations = 10
mutation_rate = 0.1
backpack_capacity = 20  # Maximální kapacita batohu v kg

# Vytvoření náhodného binárního chromozomu (kandidáta)
def create_binary_candidate(length):
    return [random.choice([0, 1]) for _ in range(length)]

# Fitness funkce
def fitness_function(candidate):
    total_value = 0
    total_weight = 0
    for i in range(len(candidate)):
        if candidate[i] == 1:
            predmet = list(predmety.values())[i]
            total_value += predmet["cena"]
            total_weight += predmet["vaha"]
    
    # Pokud hmotnost přesáhne kapacitu batohu, je fitness nulová
    if total_weight > backpack_capacity:
        return 0
    
    return total_value

# Výběr rodičů pomocí turnajového výběru
def tournament_selection(population):
    tournament_size = 3
    selected = random.sample(population, tournament_size)
    selected.sort(key=lambda x: x['fitness'], reverse=True)
    return selected[0]['candidate']

# Křížení (crossover) dvou rodičů
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

# Mutace
def mutate(candidate, mutation_rate):
    for i in range(len(candidate)):
        if random.random() < mutation_rate:
            candidate[i] = 1 - candidate[i]

# Hlavní funkce genetického algoritmu
def genetic_algorithm():
    # Vytvoření počáteční populace
    population = [{'candidate': create_binary_candidate(len(predmety)), 'fitness': 0} for _ in range(populace_size)]
    
    # Vyhodnocení počáteční populace
    for individual in population:
        individual['fitness'] = fitness_function(individual['candidate'])
    
    # Hlavní cyklus genetického algoritmu
    for generation in range(generations):
        # Vytvoření nové populace
        new_population = []
        
        # Výběr, křížení a mutace
        while len(new_population) < populace_size:
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child1, child2 = crossover(parent1, parent2)
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            
            # Vyhodnocení fitness nových potomků
            new_population.append({'candidate': child1, 'fitness': fitness_function(child1)})
            new_population.append({'candidate': child2, 'fitness': fitness_function(child2)})
        
        # Nahrazení staré populace novou
        population = new_population
        
        # Tisk nejlepšího řešení v každé generaci
        best_individual = max(population, key=lambda x: x['fitness'])
        print(f'Generace {generation + 1}, Nejlepší řešení: {best_individual["candidate"]}, Hodnota: {best_individual["fitness"]}')
    
    # Výstup nejlepšího řešení z poslední generace
    best_individual = max(population, key=lambda x: x['fitness'])
    return best_individual

# Spuštění genetického algoritmu
best_solution = genetic_algorithm()
print('Nejlepší řešení:', best_solution['candidate'], 's hodnotou:', best_solution['fitness'])
