import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Gravitational Constant
G = 6.67430e-11  

# Simulation Parameters
num_steps = 1000
dt = 1e5  

# Masses of the bodies (in kilograms)
m1 = 5.972e24   # Earth mass
m2 = 7.348e22   # Moon mass
m3 = 1.989e30   # Sun mass

# Initial Positions (in meters)
r1 = np.array([1.496e11, 0.0])    # Earth initial position
r2 = np.array([1.496e11 + 3.844e8, 0.0])  # Moon initial position
r3 = np.array([0.0, 0.0])         # Sun at the origin

# Initial Velocities (in meters per second)
v1 = np.array([0.0, 29780.0])     # Earth initial velocity
v2 = np.array([0.0, 29780.0 + 1022.0])  # Moon initial velocity
v3 = np.array([0.0, 0.0])         # Sun initial velocity

# Store positions for plotting
positions1 = []
positions2 = []
positions3 = []

def calculate_accelerations(r1, r2, r3):
    r12 = r2 - r1
    r13 = r3 - r1
    r23 = r3 - r2

    dist12 = np.linalg.norm(r12)
    dist13 = np.linalg.norm(r13)
    dist23 = np.linalg.norm(r23)

    a1 = G * ((m2 * r12 / dist12**3) + (m3 * r13 / dist13**3))
    a2 = G * ((m1 * -r12 / dist12**3) + (m3 * r23 / dist23**3))
    a3 = G * ((m1 * -r13 / dist13**3) + (m2 * -r23 / dist23**3))

    return a1, a2, a3

positions = [(r1.copy(), v1.copy(), m1),
             (r2.copy(), v2.copy(), m2),
             (r3.copy(), v3.copy(), m3)]

# Simulation Loop
for _ in range(num_steps):
    r1, v1, m1 = positions[0]
    r2, v2, m2 = positions[1]
    r3, v3, m3 = positions[2]

    a1, a2, a3 = calculate_accelerations(r1, r2, r3)

    v1 += a1 * dt
    v2 += a2 * dt
    v3 += a3 * dt

    r1 += v1 * dt
    r2 += v2 * dt
    r3 += v3 * dt

    positions1.append(r1.copy())
    positions2.append(r2.copy())
    positions3.append(r3.copy())

    positions[0] = (r1, v1, m1)
    positions[1] = (r2, v2, m2)
    positions[2] = (r3, v3, m3)
    print(f"r1: {r1}, r2: {r2}, r3: {r3}")


positions1 = np.array(positions1)
positions2 = np.array(positions2)
positions3 = np.array(positions3)

# Plotting and Animation
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_facecolor('black')
ax.set_aspect('equal')
ax.set_xlim(-1.6e11, 1.6e11)
ax.set_ylim(-1.6e11, 1.6e11)
ax.set_xlabel('X Position (m)')
ax.set_ylabel('Y Position (m)')
ax.set_title('Three-Body Problem Simulation')

# Plot trajectories
line1, = ax.plot([], [], 'cyan', lw=0.5)
line2, = ax.plot([], [], 'orange', lw=0.5)
line3, = ax.plot([], [], 'yellow', lw=0.5)

# Plot bodies
body1, = ax.plot([], [], 'o', color='cyan', markersize=10)  
body2, = ax.plot([], [], 'o', color='orange', markersize=8) 
body3, = ax.plot([], [], 'o', color='yellow', markersize=15) 


def init():
    line1.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])
    body1.set_data([], [])
    body2.set_data([], [])
    body3.set_data([], [])
    return line1, line2, line3, body1, body2, body3

def animate(i):
    # Update trajectory lines
    line1.set_data(positions1[:i, 0], positions1[:i, 1])
    line2.set_data(positions2[:i, 0], positions2[:i, 1])
    line3.set_data(positions3[:i, 0], positions3[:i, 1])

    # Update body positions
    body1.set_data([positions1[i, 0]], [positions1[i, 1]])
    body2.set_data([positions2[i, 0]], [positions2[i, 1]])
    body3.set_data([positions3[i, 0]], [positions3[i, 1]])

    return line1, line2, line3, body1, body2, body3


ani = FuncAnimation(fig, animate, frames=num_steps, init_func=init,
                    interval=20, blit=True)

plt.show()
