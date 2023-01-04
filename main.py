import pygame

import os

# consts

# margin for upper left corner
TOP = 0
LEFT = 0
CELL_SIZE = 50
SIZE = WIDTH, HEIGHT = 800, 800

MAX_X = None
MAX_Y = None

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def load_image(name, color_key=None):
    pygame.init()
    fullname = os.path.join('data/skin', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


class Labyrinth:
    # создание карты
    def __init__(self, file_name, allow_to_go=0, exit_poit=-1, hero_start=2):
        self.map = []
        with open(file_name) as file:
            for line in file:
                self.map.append(list(line))
        self.left = LEFT
        self.top = TOP
        self.cell_size = CELL_SIZE
        self.pos_of_hero = None

    def render(self, scr):
        y = self.left
        for i in range(len(self.map)):
            x = self.top
            for j in range(len(self.map[i])):
                if self.map[i][j] == '#':
                    pygame.draw.rect(scr, WHITE, (x, y, self.cell_size, self.cell_size))
                if self.map[i][j] == '.':
                    pygame.draw.rect(scr, BLACK, (x, y, self.cell_size, self.cell_size))
                if self.map[i][j] == '@':
                    self.pos_of_hero = (j, i)
                x += self.cell_size
            y += self.cell_size


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(CELL_SIZE * pos_x, CELL_SIZE * pos_y)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)  # for table
        self.rect = self.image.get_rect().move(CELL_SIZE * x,
                                               CELL_SIZE * y)  # draw it


class Game:
    def __init__(self, map_for_labyrinth):
        self.labyrinth = Labyrinth(map_for_labyrinth)
        self.hero = None

    def render(self, screen1):
        self.labyrinth.render(screen1)
        self.hero = Player(*self.labyrinth.pos_of_hero)

    def move(self, hero, movement):
        x, y = hero.pos
        level_map = self.labyrinth.map

        if movement == 'up':
            if y > 0 and level_map[y - 1][x] == '.':
                hero.move(x, y - 1)
                self.labyrinth.map[y][x] = '.'
                self.labyrinth.map[y - 1][x] = '@'
        elif movement == 'down':
            if level_map[y + 1][x] == '.':
                hero.move(x, y + 1)
                self.labyrinth.map[y][x] = '.'
                self.labyrinth.map[y + 1][x] = '@'
        elif movement == 'left':
            if x > 0 and level_map[y][x - 1] == '.':
                hero.move(x - 1, y)
                self.labyrinth.map[y][x] = '.'
                self.labyrinth.map[y][x - 1] = '@'
        elif movement == 'right':
            if level_map[y][x + 1] == '.':
                self.labyrinth.map[y][x] = '.'
                self.labyrinth.map[y][x + 1] = '@'
                hero.move(x + 1, y)


if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Game')

    hero_group = pygame.sprite.Group()
    player_image = load_image('Pink_Monster.png')

    game = Game("maps/map_1.txt")
    game.render(screen)

    clock = pygame.time.Clock()
    running = True
    fps = 30

    while running:
        pygame.time.delay(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        keys = pygame.key.get_pressed()
        x, y = game.hero.pos

        if keys[pygame.K_LEFT]:
            game.move(game.hero, 'left')
        if keys[pygame.K_RIGHT]:
            game.move(game.hero, 'right')
        if keys[pygame.K_UP]:
            game.move(game.hero, 'up')
        if keys[pygame.K_DOWN]:
            game.move(game.hero, 'down')
        screen.fill(BLACK)
        hero_group.draw(screen)
        game.render(screen)
        clock.tick(fps)
        pygame.display.flip()
