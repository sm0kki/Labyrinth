import pygame

from player import *
from monsters import *
from blocks import *

level = []
entities = pygame.sprite.Group()
monsters = pygame.sprite.Group()
walls = []


class Labyrinth:
    def __init__(self, file_name):
        self.map = []
        self.height = 0
        with open(file_name) as file:
            for line in file:
                self.map.append(list(line))
                self.height += 1
        self.width = len(self.map[0])
        self.pos_of_hero = None
        self.pos_of_enemy = None
        self.total_level_width = (len(self.map[0]) - 1) * WIDTH
        self.total_level_height = len(self.map) * HEIGHT
        self.hero = None
        self.fill_grass()
        self.render()

    def fill_grass(self):
        x = y = 0

        for row in self.map:
            for col in row:
                gr = Grass(x, y)
                entities.add(gr)
                x += WIDTH
            y += HEIGHT
            x = 0

    def render(self):
        x = y = 0

        for row in self.map:
            for col in row:
                if col == "#":
                    pf = Wall(x, y)
                    entities.add(pf)
                    walls.append(pf)
                if col == "*":
                    bd = BlockDie(x, y)
                    entities.add(bd)
                    walls.append(bd)
                if col == "X":
                    ex = Exit(x, y)
                    entities.add(ex)
                    walls.append(ex)
                if col == "H":
                    self.hero = Player(x, y)
                    entities.add(self.hero)
                if col == "M":
                    mn = Monster(x, y, 1, 0, 2000, 0)
                    entities.add(mn)
                    walls.append(mn)
                    monsters.add(mn)
                x += WIDTH
            y += HEIGHT
            x = 0

    def find_path_step(self, start, target):
        inf = 1000
        x, y = start
        distance = [[inf] * self.width for _ in range(self.height)]
        distance[y][x] = 0
        prev = [[None] * self.width for _ in range(self.height)]
        queue = [(x, y)]
        while queue:
            x, y = queue.pop(0)
            for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
                next_x, next_y = x + dx, y + dx
                if 0 <= next_x < self.width and 0 < next_y < self.height and \
                        self.map[next_y][next_x] == '.' and distance[next_y][next_x] == inf:
                    distance[next_y][next_x] = distance[y][x] + 1
                    prev[next_y][next_x] = (x, y)
                    queue.append((next_x, next_y))
        x, y = target
        if distance[y][x] == inf or start == target:
            return start
        while prev[y][x] != start:
            x, y = prev[y][x]
        return x, y


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не идём дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не идём дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не идём дальше нижней границы
    t = min(0, t)  # Не идём дальше верхней границы

    return Rect(l, t, w, h)
