from dataclasses import dataclass
from itertools import pairwise
import math

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

if __name__ == '__main__':
    dt = 1 / 60

    game = Game()
    game.set_up()

    while not all(enemy.at_end for enemy in game.enemies):
        game.print_enemy_positions()
        game.progress(dt)