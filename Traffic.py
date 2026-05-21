import pygame
import random
import sys
import time

pygame.init()
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Traffic Management - Optimized v2")
clock = pygame.time.Clock()

# Colors
DARK = (30, 30, 35)
ROAD = (65, 65, 70)
WHITE = (255, 255, 255)
RED = (255, 40, 40)
GREEN = (0, 225, 0)
YELLOW = (255, 220, 0)

signals = ["NS_GREEN", "NS_YELLOW", "EW_GREEN", "EW_YELLOW"]
current_signal = 0
signal_timer = 0
signal_duration = [48, 5, 48, 5]

vehicles_passed = 0
start_time = time.time()

lanes = [[] for _ in range(4)]  # 0N, 1E, 2S, 3W

class Vehicle:
    def __init__(self, dir):
        self.dir = dir
        self.pos = -80
        self.speed = random.randint(5, 7)
        self.color = random.choice([(200,50,50),(50,90,200),(220,160,40),(40,160,80),(140,40,180)])
    
    def draw(self):
        if self.dir == 0:    # North ↓
            pygame.draw.rect(screen, self.color, (WIDTH//2-95, self.pos, 42, 22), border_radius=8)
        elif self.dir == 1:  # East ←
            pygame.draw.rect(screen, self.color, (WIDTH - self.pos, HEIGHT//2-52, 22, 42), border_radius=8)
        elif self.dir == 2:  # South ↑
            pygame.draw.rect(screen, self.color, (WIDTH//2+53, HEIGHT-self.pos, 42, 22), border_radius=8)
        elif self.dir == 3:  # West →
            pygame.draw.rect(screen, self.color, (self.pos, HEIGHT//2+28, 22, 42), border_radius=8)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(DARK)

    # Roads
    pygame.draw.rect(screen, ROAD, (WIDTH//2 - 75, 0, 150, HEIGHT))
    pygame.draw.rect(screen, ROAD, (0, HEIGHT//2 - 75, WIDTH, 150))

    # Signal Timer
    signal_timer += 1
    if signal_timer > signal_duration[current_signal] * 60:
        signal_timer = 0
        current_signal = (current_signal + 1) % 4

    signal_name = signals[current_signal]

    # Spawn Vehicles (with limit)
    if random.random() < 0.055:
        d = random.randint(0, 3)
        if len(lanes[d]) < 18:        # Max 18 vehicles per lane
            lanes[d].append(Vehicle(d))

    # Update & Draw Vehicles - Highly Optimized
    for d in range(4):
        lane = lanes[d]
        green = (signal_name == "NS_GREEN" if d in (0,2) else signal_name == "EW_GREEN")
        stop_pos = 295
        i = 0
        while i < len(lane):
            v = lane[i]

            # Stop Logic
            if not green and v.pos >= stop_pos - 35:
                target_pos = stop_pos - 35 - (i * 48)
                if v.pos > target_pos:
                    v.pos = target_pos
            else:
                v.pos += v.speed

            # Draw
            v.draw()

            # Remove crossed vehicle
            if v.pos > WIDTH + 120:
                lane.pop(i)
                vehicles_passed += 1
                continue

            i += 1

    # Traffic Lights
    ns_color = GREEN if signal_name.startswith("NS_GREEN") else (YELLOW if signal_name.startswith("NS_YELLOW") else RED)
    ew_color = GREEN if signal_name.startswith("EW_GREEN") else (YELLOW if signal_name.startswith("EW_YELLOW") else RED)

    pygame.draw.circle(screen, ns_color, (WIDTH//2 - 170, HEIGHT//2 - 115), 34)
    pygame.draw.circle(screen, ew_color, (WIDTH//2 + 170, HEIGHT//2 + 115), 34)

    # Info
    font = pygame.font.SysFont("Arial", 34)
    texts = [
        f"Signal : {signal_name}",
        f"Vehicles Passed : {vehicles_passed}",
        f"Total Vehicles : {sum(len(l) for l in lanes)}"
    ]
    for i, t in enumerate(texts):
        screen.blit(font.render(t, True, WHITE), (20, 15 + i*48))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()