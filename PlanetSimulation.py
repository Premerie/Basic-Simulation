import pygame
import math

pygame.init()
WIDTH, HEIGHT = 680, 680
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
surf = WIN.get_rect()
WIDTH, HEIGHT = surf.w, surf.h
pygame.display.set_caption("PLANET SIMULATION")

WHITE = (255, 255, 255)
POLE = (101, 83, 110)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
BLACK = (25, 25, 25)

FONT = pygame.font.SysFont("comicsans", 20)
START = pygame.font.SysFont("comicsans", 30)
HEADER = pygame.font.SysFont("comicsans", 40)

class Planet:
    AU = 149.6e9 # AU means Astronomical Unit
    G = 6.67428e-11
    SCALE = 200 / AU # 1AU = 100 pixels
    TIMESTEP = 3600 * 24
    
    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y
        
        self.radius = radius
        self.color = color
        self.mass = mass
        
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        
        self.x_vel = 0
        self.y_vel = 0
        
        self.name = name
        
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        
        updated_points = []
        if len(self.orbit) > 2:
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)
                
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))
            
    def show(self, win, y):
        if self.sun:
            text = HEADER.render(f"Orbits", 1, WHITE)
            win.blit(text, (text.get_width()/2, y - text.get_height()/2)) 
        if not self.sun:
            start, end = (20, y), (400, y)
            pygame.draw.line(win, self.color, start, end, 10)
        pygame.draw.circle(win, self.color, (680, y), self.radius/2)
        distance_text = FONT.render(f"{self.name}", 1, WHITE)
        win.blit(distance_text, (650 - distance_text.get_width(), y - distance_text.get_height()/2))
                
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)
        
        if other.sun:
            self.distance_to_sun = distance 
        
        # F = G * m1 * m2 / r²
        force = self.G * self.mass * other.mass / distance**2
        
        theta = math.atan2(distance_y, distance_x)
        
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
        
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        self.x_vel += total_fx / self.mass * self.TIMESTEP 
        self.y_vel += total_fy / self.mass * self.TIMESTEP 
        # f = m / a
        # a = m / f
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def run():
    run = True
    clock = pygame.time.Clock()
    
    sun = Planet(0, 0, 45, YELLOW, 1.98892 * 10**30, "Sun")
    sun.sun = True
    
    earth = Planet(-1 * Planet.AU, 0, 30, BLUE, 5.9742 * 10**24, "Earth")
    earth.y_vel = 29.783 *1000
    
    mars = Planet(-1.524 * Planet.AU, 0, 26, RED, 6.39 * 10**23, "Mars")
    mars.y_vel = 24.077 * 1000
    
    mercury = Planet(0.367 * Planet.AU, 0, 22, DARK_GREY, 3.30 * 10**23, "Mercury")
    mercury.y_vel = -47.4 * 1000
    
    venus = Planet(0.723 * Planet.AU, 0, 28, POLE, 4.8685 * 10**24, "Venus")
    venus.y_vel = -35.02 * 1000
    
    planets = [sun, earth, mars, mercury, venus]
    
    distances = [1250, 1300, 1350, 1400, 1450]
    
    while run:
        WIN.fill(BLACK)
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for planet, y in zip(planets, distances):
            planet.update_position(planets)
            planet.draw(WIN)
            planet.show(WIN, y)
        pygame.display.update()
    pygame.quit()

def start():
    WIN.fill(BLACK)
    
    text = HEADER.render(f"PLANET SIMULATOR", 300, WHITE)
    text2 = START.render(str("start").upper(), 300, WHITE) 
                  
    rect = pygame.Rect((0, 0), (150, 50))
    rect.center = (surf.w/2, surf.h/2 + 230)
      
    run = True
    touched = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect.collidepoint(event.pos):
                    touched = True
            elif event.type == pygame.MOUSEBUTTONUP:
                touched = False 
            elif event.type == pygame.QUIT:
                pygame.quit()
        if touched:
            run = False
        WIN.fill((BLUE), rect)
        WIN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
        WIN.blit(text2, (surf.w/2 - text2.get_width()/2, surf.h/2 - text2.get_height()/2 + 230))
        pygame.display.flip()
        
def main():
    start()
    run()

if __name__ == "__main__":                
    main()                
