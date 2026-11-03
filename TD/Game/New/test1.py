import pygame
import time
from dataclasses import dataclass
from itertools import pairwise
import math

background_colour = (155,255,200)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
(width, height) = (1500, 750)
path_points = [(000, 250), (300, 250), (600, 650), (1500, 750)]


def cart_dist(pos1, pos2):
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2) ** 0.5

def distance_to_line_segment(point, start, end):
    px,py = point
    x1,y1 = start
    x2,y2 = end
    dx = x2-x1
    dy = y2-y1
    length_squared = dx**2 + dy**2

    if length_squared == 0:
        return cart_dist(point, start)

    t = ((px-x1)*dx + (py-y1)*dy) / length_squared
    t = max(0, min(1, t))

    closest = (x1 + t*dx, y1 + t*dy)

    return cart_dist(point, closest)

@dataclass
class Position:
    x: float = 0
    y: float = 0

    def __repr__(self) -> str:
        return f"({self.x:.2f}, {self.y:.2f})"

def calc_euclidean_length(a: Position, b: Position) -> float:
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

class Line:
    def __init__(self, start: Position, end: Position):
        self.start = start
        self.end = end

    @property
    def length(self) -> float:
        return calc_euclidean_length(self.start, self.end)

    def __repr__(self) -> str:
        return f'(start={self.start}, end={self.end})'

class Path:
    def __init__(self, points: list[Position]):
        self.lines = [Line(a,b) for a, b in pairwise(points)]

class Enemy:
    def __init__(self, path: Path, line=0, line_progress=0, speed: float = 1.0):
        self.path = path
        self.line = line
        self.line_progress = line_progress
        self.speed = speed
        self.health = 30

    @property
    def position(self) -> Position:
        # position = (1 - progress) * start + progress * end
        x = ((1 - self.line_progress) * self.path.lines[self.line].start.x +
                self.line_progress * self.path.lines[self.line].end.x)
        y = ((1 - self.line_progress) * self.path.lines[self.line].start.y +
                self.line_progress * self.path.lines[self.line].end.y)
        return Position(x, y)

    @property
    def at_end(self) -> bool:
        if self.line >= len(self.path.lines) or (self.line == len(self.path.lines) - 1 and self.line_progress >=1):
            return True
        else:
            return False

    def progress(self, delta_time):
        self.line_progress += self.speed * delta_time / self.path.lines[self.line].length
        if self.line_progress >= 1:
            self.line_progress -= 1
            self.line += 1
        if self.at_end:
            self.line_progress = 1
            self.line = len(self.path.lines) - 1


    def __str__(self) -> str:
        return f'Enemy at {self.position}'

class Tower:
    def __init__(self, x, y, range=180, damage=10, fire_rate=1):
        self.x = x
        self.y = y
        self.range = range
        self.damage = damage
        self.fire_rate = fire_rate
        self.cooldown = 0

    @property
    def position(self):
        return (self.x, self.y)

    def can_shoot(self, enemies):
        targets = []

        # Find all enemies within range
        for enemy in enemies:
            if not enemy.at_end:
                distance = cart_dist(
                    self.position,
                    (enemy.position.x, enemy.position.y)
                )

                if distance <= self.range:
                    targets.append(enemy)

        # Find the closest enemy
        closest_enemy = None
        closest_distance = 99999999999999

        for enemy in targets:
            distance = cart_dist(
                self.position,
                (enemy.position.x, enemy.position.y)
            )

            if distance < closest_distance:
                closest_distance = distance
                closest_enemy = enemy

        return closest_enemy

    def update(self, dt, enemies, projectiles):
        self.cooldown -= dt

        if self.cooldown <= 0:
            target = self.can_shoot(enemies)

            if target is not None:
                projectiles.append(
                    Projectile(self.position, target, self.damage)
                )
                self.cooldown = 1 / self.fire_rate


class Projectile:
    def __init__(self, start, target, damage):
        self.x, self.y = start
        self.target = target
        self.damage = damage
        self.speed = 400
        self.dead = False

    def update(self, dt):
        if self.target.health <= 0:
            self.dead = True
            return

        if self.target.at_end:
            self.dead = True
            return

        target_pos = (self.target.position.x,self.target.position.y)
        dx = target_pos[0] - self.x
        dy = target_pos[1] - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance < self.speed * dt:
            self.target.health -= self.damage
            self.dead = True
            return

        self.x += (dx / distance) * self.speed * dt
        self.y += (dy / distance) * self.speed * dt


class Game:
    def __init__(self):
        self.tracks = []
        self.enemies = []

    def add_enemy(self, enemy: Enemy):
        self.enemies.append(enemy)
        if enemy.path not in self.tracks:
            self.tracks.append(enemy.path)

    def progress(self, delta_time):
        for enemy in self.enemies:
            enemy.progress(delta_time)

    def print_enemy_positions(self):
        for i, enemy in enumerate(self.enemies):
            print(f'Enemy {i} at {enemy.position};', end=' ')
        print()

    def set_up(self):
        game_path = Path([Position(0, 0),
                          Position(50, 0),
                          Position(50, 50),
                          Position(100, 100),
                          ])
        self.add_enemy(Enemy(game_path, speed=20))
        self.add_enemy(Enemy(game_path, line=1, speed=100))


class GameGUI:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('TD game')
        self.screen = pygame.display.set_mode([width, height])
        self.screen.fill(background_colour)
        self.pos = (0, 0)
        self.circle_list = []
        self.running = True
        self.clock = pygame.time.Clock()
        enemy_path = Path([Position(x, y) for x, y in path_points])
        self.enemies = [Enemy(enemy_path, speed=150)]
        self.towers = []
        self.projectiles = []

    def on_path(self, pos):
        path_width = 20

        for i in range(len(path_points) - 1):
            distance = distance_to_line_segment(
                pos,
                path_points[i],
                path_points[i + 1]
            )

            if distance < path_width:
                return True

        return False

    def math_function(self, option):
        pass

    def main_loop(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            self.handle_inputs()

            for enemy in self.enemies:
                enemy.progress(dt)
            for tower in self.towers:
                tower.update(dt, self.enemies, self.projectiles)
            for projectile in self.projectiles:
                projectile.update(dt)

            self.projectiles = [p for p in self.projectiles if not p.dead]
            self.enemies = [e for e in self.enemies if e.health > 0]

            self.draw()

        pygame.quit()

    def can_place_tower(self, pos):
        if self.on_path(pos):
            return False
        if any(cart_dist(pos, tower) < 25 for tower in self.circle_list):
            return False
        return True

    def handle_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if self.can_place_tower(pos):
                        self.circle_list.append(pos)
                        self.towers.append(Tower(*pos))
                    else:
                        print("Invalid")


    def handle_append(self):
        pass

    def draw(self):
        self.draw_background()
        self.draw_path()

        self.draw_range()
        self.draw_towers()
        self.draw_enemies()
        self.draw_projectiles()

        pygame.display.flip()

    def draw_background(self):
        self.screen.fill(background_colour)


    def draw_towers(self):
        self.pos = pygame.mouse.get_pos()
        for x, y in self.circle_list:
            pygame.draw.circle(self.screen, red, (x, y), 10)
        if self.can_place_tower(self.pos):
            preview_colour = green
        else:
            preview_colour = red
        pygame.draw.circle(
            self.screen,
            preview_colour,
            self.pos,
            10
        )

    def draw_range(self):
        for tower in self.towers:
            # Transparent range circle
            range_surface = pygame.Surface(
                (tower.range * 2, tower.range * 2),
                pygame.SRCALPHA
            )

            pygame.draw.circle(
                range_surface,
                (0, 0, 255, 35),
                (tower.range, tower.range),
                tower.range
            )

            self.screen.blit(
                range_surface,
                (tower.x - tower.range, tower.y - tower.range)
            )

    def draw_projectiles(self):
        for projectile in self.projectiles:
            pygame.draw.circle(
                self.screen,
                (0, 0, 0),
                (int(projectile.x), int(projectile.y)),
                5
            )

    def draw_path(self):
        pygame.draw.lines(self.screen, "yellow", False,path_points , 5)

    def draw_enemies(self):
        for enemy in self.enemies:
            pos = enemy.position

            pygame.draw.circle(
                self.screen,
                green,
                (int(pos.x), int(pos.y)),
                12
            )




if __name__ == "__main__":
    game = GameGUI()
    game.main_loop()