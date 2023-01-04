import pygame

import os

pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Game')

def load_image(name, color_key=None):
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
        print(self.map)
        # значения по умолчанию


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        # значения по умолчаниюяё
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, scr):
        y = self.left
        for i in range(len(self.map)):
            x = self.top
            for j in range(len(self.map[i])):
                if self.map[i][j] == '#':
                    pygame.draw.rect(scr, (255, 255, 255), (x, y, self.cell_size, self.cell_size))
                if self.map[i][j] == '.':
                    pygame.draw.rect(scr, (0, 0, 0), (x, y, self.cell_size, self.cell_size))
                x += self.cell_size
            y += self.cell_size


class Game:
    def __init__(self, labyrinth):
        self.labyrinth = labyrinth

    def render(self, screen1):
        self.labyrinth.render(screen1)


hero_group = pygame.sprite.Group()
player_image = load_image('Pink_Monster.png')
tile_width = tile_height = 50


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
        self.rect = self.image.get_rect().move(pos_x + 10, pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(self.pos[0] + 10,
                                               self.pos[1] + 5)

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Game')
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    labyrinth = Labyrinth('maps/map_1.txt')
    labyrinth.set_view(0, 0, 50)
    game = Game(labyrinth)
    clock = pygame.time.Clock()
    running = True
    fps = 30
    board = Board(width, height)
    hero = Player(labyrinth.left, board.top)

    while running:
        pygame.time.delay(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        keys = pygame.key.get_pressed()
        x, y = hero.pos
        vel = board.cell_size
        if keys[pygame.K_LEFT]:
            hero.move(x - vel, y)
        if keys[pygame.K_RIGHT]:
            hero.move(x + vel, y)
        if keys[pygame.K_UP]:
            hero.move(x, y - vel)
        if keys[pygame.K_DOWN]:
            hero.move(x, y + vel)
        screen.fill((0, 0, 0))
        game.render(screen)
        clock.tick(fps)
        hero_group.draw(screen)
        pygame.display.flip()
