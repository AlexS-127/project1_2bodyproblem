import pygame
import numpy as np

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("project1_2bodyproblem")

G = 100

m1 = 10
m2 = 10

dt = 0.1

def initialize_particles():
    r1 = np.array([WIDTH / 2 - 100.0, HEIGHT / 2])
    r2 = np.array([WIDTH / 2 + 100.0, HEIGHT / 2])

    v1 = np.array([1.0, 1.0])
    v2 = np.array([-1.0, -1.0])

    return r1, r2, v1, v2

def compute_force(r1, r2, m1, m2):
    displacement = r2 - r1
    r = (displacement[0]**2 + displacement[1]**2)**0.5
    force_magnitude = G * m1 * m2 / r**2
    force = force_magnitude * displacement / r
    return force, r

def update_positions_velocities(r1, r2, v1, v2, a1, a2, dt):
    r1_new = r1 + v1 * dt + 0.5 * a1 * dt**2
    r2_new = r2 + v2 * dt + 0.5 * a2 * dt**2

    grav_force_new, distance = compute_force(r1_new, r2_new, m1, m2)
    a1_new = grav_force_new / m1
    a2_new = -grav_force_new / m2

    v1_new = v1 + 0.5 * (a1 + a1_new) * dt
    v2_new = v2 + 0.5 * (a2 + a2_new) * dt

    return r1_new, r2_new, v1_new, v2_new, a1_new, a2_new, distance, grav_force_new

def draw_particles(screen, positions1, positions2):
    screen.fill((255, 255, 255))

    positions1_list = [pos.astype(int).tolist() for pos in positions1]
    positions2_list = [pos.astype(int).tolist() for pos in positions2]

    if len(positions1_list) > 1:
        pygame.draw.lines(screen, (200, 200, 200), False, positions1_list, 1)
    if len(positions2_list) > 1:
        pygame.draw.lines(screen, (200, 200, 200), False, positions2_list, 1)

    pygame.draw.circle(screen, (50, 50, 50), positions1_list[-1], 10)
    pygame.draw.circle(screen, (50, 50, 50), positions2_list[-1], 10)

def draw_info_table(screen, m1, m2, distance, F12_new):
    font = pygame.font.SysFont(None, 24)
    table_x = WIDTH - 200
    table_y = 10
    line_height = 20
    lines = [
        f"Mass 1: {m1}",
        f"Mass 2: {m2}",
        f"Distance: {distance:.2f}",
        f"Force on 1: ({F12_new[0]:.2f}, {F12_new[1]:.2f})",
        f"Force on 2: ({-F12_new[0]:.2f}, {-F12_new[1]:.2f})"
    ]
    for i, line in enumerate(lines):
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (table_x, table_y + i * line_height))

def main():
    clock = pygame.time.Clock()

    r1, r2, v1, v2 = initialize_particles()

    grav_force, distance = compute_force(r1, r2, m1, m2)
    a1 = grav_force / m1
    a2 = -grav_force / m2

    positions1 = [r1.copy()]
    positions2 = [r2.copy()]

    running = True
    while running:
        clock.tick(300)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        r1, r2, v1, v2, a1, a2, distance, F12_new = update_positions_velocities(r1, r2, v1, v2, a1, a2, dt)

        positions1.append(r1.copy())
        positions2.append(r2.copy())

        mid = (r1 + r2) / 2
        pygame.draw.circle(screen, (50, 50, 50), mid.astype(int).tolist(), 5)

        draw_particles(screen, positions1, positions2)
        draw_info_table(screen, m1, m2, distance, F12_new)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
