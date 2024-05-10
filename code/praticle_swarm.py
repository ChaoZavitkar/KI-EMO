import numpy as np
from pyswarm import pso
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define the objective function
def objective_function(x):
    # This function is a simple example (sphere function)
    return x[0]**2 + x[1]**2

# Define the bounds of the search space
lb = [-10, -10]  # Lower bounds for x and y
ub = [10, 10]    # Upper bounds for x and y

# Initialize a figure for visualization
fig, ax = plt.subplots()
ax.set_xlim(lb[0], ub[0])
ax.set_ylim(lb[1], ub[1])
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Particle Swarm Optimization (PSO)')

# Initialize an empty scatter plot for particles
particles, = ax.plot([], [], 'ro')

# Initialize an empty scatter plot for the global best
global_best_point, = ax.plot([], [], 'bo')

# Initialize PSO variables
num_particles = 30  # Number of particles
positions = np.random.uniform(low=lb, high=ub, size=(num_particles, 2))
velocities = np.zeros_like(positions)
personal_bests = positions.copy()
global_best = None
global_best_value = np.inf

# Function to update the positions and velocities of particles
def update_pso():
    global global_best, global_best_value

    # Iterate through particles
    for i in range(num_particles):
        # Evaluate fitness
        fitness = objective_function(positions[i])
        # Update personal bests
        if fitness < objective_function(personal_bests[i]):
            personal_bests[i] = positions[i].copy()
        # Update global best
        if fitness < global_best_value:
            global_best_value = fitness
            global_best = positions[i].copy()
    
    # Update velocities and positions of particles
    for i in range(num_particles):
        # Random factors
        r1, r2 = np.random.rand(2)
        # Update velocity
        velocities[i] = (w * velocities[i] +
                         c1 * r1 * (personal_bests[i] - positions[i]) +
                         c2 * r2 * (global_best - positions[i]))
        # Update position
        positions[i] += velocities[i]
        # Clip positions within bounds
        positions[i] = np.clip(positions[i], lb, ub)

# Parameters for PSO
w = 0.5  # Inertia weight
c1 = 1.5  # Cognitive weight
c2 = 1.5  # Social weight

# Animation function
def animate(frame):
    # Update PSO
    update_pso()
    # Update the scatter plot for particles
    particles.set_data(positions[:, 0], positions[:, 1])
    # Update the scatter plot for global best
    if global_best is not None:
        global_best_point.set_data(global_best[0], global_best[1])
    return particles, global_best_point

# Create animation
ani = FuncAnimation(fig, animate, frames=100, interval=100, blit=True)

# Show the animation
plt.show()
