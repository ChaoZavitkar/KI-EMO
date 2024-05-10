import pygame
import random
import math

# Konstanty
WIDTH, HEIGHT = 800, 600
NUM_AGENTS = 50
AGENT_WIDTH = 6  # Šířka obdélníka agenta
AGENT_HEIGHT = 3  # Výška obdélníka agenta
SWARM_SPEED = 10
BG_COLOR = (30, 30, 30)
AGENT_COLOR = (255, 255, 255)
# Definujte konstantu pro vzdálenost odpuzování
REPULSION_DISTANCE = 20  # Vzdálenost, při které se agenti začínají odpuzovat

# Definice třídy Agent
class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Inicializace směru agenta
        self.angle = random.uniform(0, 360)
        # Vytvoření obdélníka reprezentujícího agenta
        self.original_rect = pygame.Surface((AGENT_WIDTH, AGENT_HEIGHT))
        self.original_rect.fill(AGENT_COLOR)
    
    def apply_repulsion_force(self, other_agent):
        # Vypočítání vzdálenosti mezi tímto agentem a jiným agentem
        dx = other_agent.x - self.x
        dy = other_agent.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Pokud je vzdálenost menší než vzdálenost odpuzování, aplikujte odpuzující sílu
        if distance > 0 and distance < REPULSION_DISTANCE:
            # Inverzní vztah mezi vzdáleností a silou
            force = REPULSION_DISTANCE / distance
            # Vypočítání vektoru odpuzující síly
            repulsion_x = -force * (dx / distance)
            repulsion_y = -force * (dy / distance)
            
            # Aplikujte odpuzující sílu
            self.x += repulsion_x
            self.y += repulsion_y
    
    def move(self):
        # Vypočítání pohybového vektoru
        move_x = math.cos(math.radians(self.angle)) * SWARM_SPEED
        move_y = math.sin(math.radians(self.angle)) * SWARM_SPEED
        
        # Aktualizace polohy agenta
        self.x += move_x
        self.y += move_y
        
        # Náhodně upravte úhel pro přidání náhodnosti do pohybu
        self.angle += random.uniform(-5, 5)
        
        # Ujistěte se, že agent zůstává v hranicích obrazovky
        self.x = max(0, min(WIDTH, self.x))
        self.y = max(0, min(HEIGHT, self.y))
    
    def move_towards(self, target_x, target_y):
        # Vypočítání úhlu směrem k cílovému bodu
        dx = target_x - self.x
        dy = target_y - self.y
        self.angle = math.degrees(math.atan2(dy, dx))
        
        # Vypočítání pohybového vektoru
        move_x = math.cos(math.radians(self.angle)) * SWARM_SPEED
        move_y = math.sin(math.radians(self.angle)) * SWARM_SPEED
        
        # Aktualizace polohy agenta
        self.x += move_x
        self.y += move_y
    
    def draw(self, screen):
        # Otočte původní obdélník podle aktuálního úhlu
        rotated_rect = pygame.transform.rotate(self.original_rect, -self.angle)
        # Získejte ohraničující rámeček otočeného obdélníka
        rotated_rect_rect = rotated_rect.get_rect(center=(self.x, self.y))
        
        # Vykreslete otočený obdélník na obrazovku
        screen.blit(rotated_rect, rotated_rect_rect)

# Definice třídy Swarm
class Swarm:
    def __init__(self, num_agents):
        # Inicializace agentů na náhodných pozicích v rámci obrazovky
        self.agents = [Agent(random.uniform(0, WIDTH), random.uniform(0, HEIGHT)) for _ in range(num_agents)]
        # Inicializace cílového bodu pro roj (zpočátku žádný)
        self.target_x = None
        self.target_y = None
    
    def update(self):
        # Pokud je nastaven cílový bod, pohybujte každého agenta směrem k němu
        if self.target_x is not None and self.target_y is not None:
            for agent in self.agents:
                agent.move_towards(self.target_x, self.target_y)
        
        # Aplikujte odpuzující sílu mezi agenty
        for i in range(NUM_AGENTS):
            for j in range(i + 1, NUM_AGENTS):
                agent1 = self.agents[i]
                agent2 = self.agents[j]
                
                # Aplikujte odpuzující sílu od agenta2 k agentovi1 a naopak
                agent1.apply_repulsion_force(agent2)
                agent2.apply_repulsion_force(agent1)
        
        # Náhodně pohybujte každého agenta (pokud není nastaven cíl)
        if self.target_x is None and self.target_y is None:
            for agent in self.agents:
                agent.move()
    
    def draw(self, screen):
        # Vykreslete každého agenta na obrazovce
        for agent in self.agents:
            agent.draw(screen)
    
    def set_target_point(self, x, y):
        # Aktualizujte cílový bod pro roj
        self.target_x = x
        self.target_y = y

# Inicializujte pygame a vytvořte obrazovku
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Swarm Simulation")

# Vytvoření roje
swarm = Swarm(NUM_AGENTS)

# Hlavní smyčka
running = True
while running:
    # Zkontrolujte události
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Když je myš kliknuta, nastavte cílový bod pro roj
            mouse_x, mouse_y = event.pos
            swarm.set_target_point(mouse_x, mouse_y)
    
    # Aktualizujte roj
    swarm.update()
    
    # Vyčistěte obrazovku
    screen.fill(BG_COLOR)
    
    # Vykreslete roj
    swarm.draw(screen)
    
    # Aktualizujte zobrazení
    pygame.display.flip()
    
    # Ovládejte snímkovou frekvenci
    pygame.time.delay(50)

# Ukončete pygame
pygame.quit()
