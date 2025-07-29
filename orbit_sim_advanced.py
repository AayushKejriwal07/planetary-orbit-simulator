import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)

# Celestial body class
class Body:
    def __init__(self, name, mass, pos, vel, color='b'):
        self.name = name
        self.mass = mass
        self.pos = np.array(pos, dtype='float64')  # [x, y]
        self.vel = np.array(vel, dtype='float64')  # [vx, vy]
        self.color = color
        self.traj_x = []
        self.traj_y = []

    def update_position(self, dt):
        self.pos += self.vel * dt
        self.traj_x.append(self.pos[0])
        self.traj_y.append(self.pos[1])

    def apply_force(self, force, dt):
        # a = F / m
        acc = force / self.mass
        self.vel += acc * dt

# Gravitational force calculation
def gravitational_force(body1, body2):
    r_vec = body2.pos - body1.pos
    r_mag = np.linalg.norm(r_vec)
    if r_mag == 0:
        return np.zeros(2)
    r_hat = r_vec / r_mag
    force_mag = G * body1.mass * body2.mass / r_mag**2
    return force_mag * r_hat

# Initialize bodies
sun = Body("Sun", 1.989e30, [0, 0], [0, 0], 'yellow')

earth = Body("Earth", 5.972e24, [1.496e11, 0], [0, 29780], 'blue')  # ~30 km/s
mars = Body("Mars", 6.39e23, [2.279e11, 0], [0, 24130], 'red')      # ~24 km/s

bodies = [sun, earth, mars]

# Plot setup
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_facecolor("black")
ax.set_xlim(-2.5e11, 2.5e11)
ax.set_ylim(-2.5e11, 2.5e11)
ax.set_title("Multi-Body Orbital Simulator", color='white')
ax.tick_params(colors='white')

# Create plot elements
scatters = [ax.plot([], [], 'o', color=body.color, label=body.name)[0] for body in bodies]
lines = [ax.plot([], [], '-', color=body.color, lw=0.8)[0] for body in bodies]
ax.legend(facecolor='black', edgecolor='white', labelcolor='white')

# Time step (1 hour)
dt = 60 * 60

def update(frame):
    forces = [np.zeros(2) for _ in bodies]

    # Calculate all forces
    for i, body in enumerate(bodies):
        for j, other in enumerate(bodies):
            if i != j:
                forces[i] += gravitational_force(body, other)

    # Apply forces and update positions
    for i, body in enumerate(bodies):
        body.apply_force(forces[i], dt)
        body.update_position(dt)
        scatters[i].set_data(body.pos[0], body.pos[1])
        lines[i].set_data(body.traj_x, body.traj_y)

    return scatters + lines

# Run animation
ani = FuncAnimation(fig, update, frames=1000, interval=20, blit=True)
plt.show()
