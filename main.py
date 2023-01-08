import pygame

import os

# consts

# margin for upper left corner
TOP = 0
LEFT = 0
CELL_SIZE = 100
SIZE = WIDTH, HEIGHT = 800, 800

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def load_image(name, color_key=None):
    pygame.init()
    fullname = os.path.join('data', name)
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
    def __init__(self, file_name):
        self.map = []
        self.height = 0
        with open(file_name) as file:
            for line in file:
                self.map.append(list(line))
                self.height += 1
        self.width = len(self.map[0])
        self.left = LEFT
        self.top = TOP
        self.cell_size = CELL_SIZE
        self.pos_of_hero = None
        self.pos_of_enemy = None

    def render(self, scr):
        y = self.left
        for i in range(len(self.map)):
            x = self.top
            for j in range(len(self.map[i])):
                if self.map[i][j] == '#':
                    Tile('wall', j, i)
                elif self.map[i][j] == '.':
                    Tile('empty', j, i)
                elif self.map[i][j] == '@':
                    Tile('empty', j, i)
                    self.pos_of_hero = (j, i)
                elif self.map[i][j] == '!':
                    Tile('empty', j, i)
                    self.pos_of_enemy = (j, i)
                x += self.cell_size
            y += self.cell_size

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


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            CELL_SIZE * pos_x, CELL_SIZE * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(CELL_SIZE * pos_x, CELL_SIZE * pos_y)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y) # for table


    def render(self, pos_x, pos_y):
        self.rect = self.image.get_rect().move(CELL_SIZE * pos_x, CELL_SIZE * pos_y)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemy_group, all_sprites)
        self.image = enemy_image
        self.rect = self.image.get_rect().move(CELL_SIZE * pos_x, CELL_SIZE * pos_y)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        next_position = self.labyrinth.find_path_step(*self.pos, *self.labyrinth.pos_of_hero)


    def render(self, pos_x, pos_y):
        self.rect = self.image.get_rect().move(CELL_SIZE * pos_x, CELL_SIZE * pos_y)


class Game:
    def __init__(self, map_for_labyrinth):
        self.labyrinth = Labyrinth(map_for_labyrinth)
        self.labyrinth.render(screen)
        self.player = Player(*self.labyrinth.pos_of_hero)
        self.enemy = Enemy(*self.labyrinth.pos_of_enemy)
        self.pos = self.labyrinth.pos_of_hero

    def render(self, screen1):
        self.player.render(*self.player.pos)
        self.enemy.render(*self.enemy.pos)
        self.labyrinth.render(screen1)

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
                hero.move(x + 1, y)
                self.labyrinth.map[y][x] = '.'
                self.labyrinth.map[y][x + 1] = '@'



class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Game')

    all_sprites = pygame.sprite.Group()
    hero_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    tile_images = {'wall': pygame.transform.scale(load_image('texture\\box1.png'), (CELL_SIZE, CELL_SIZE)),
                   'empty': pygame.transform.scale(load_image('texture\\grass.png'), (CELL_SIZE, CELL_SIZE))}
    player_image = load_image('skin/Pink_Monster.png')
    player_image = pygame.transform.scale(player_image, (CELL_SIZE, CELL_SIZE))

    enemy_image = load_image('skin/Black_Monster.png')
    enemy_image = pygame.transform.scale(enemy_image, (CELL_SIZE, CELL_SIZE))

    game = Game("maps/map_1.txt")
    game.render(screen)

    clock = pygame.time.Clock()

    camera = Camera()
    running = True
    fps = 60

    while running:
        pygame.time.delay(40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        x, y = game.player.pos

        if keys[pygame.K_LEFT]:
            game.move(game.player, 'left')
        elif keys[pygame.K_RIGHT]:
            game.move(game.player, 'right')
        elif keys[pygame.K_UP]:
            game.move(game.player, 'up')
        elif keys[pygame.K_DOWN]:
            game.move(game.player, 'down')

        screen.fill(BLACK)

        camera.update(game.player)
        for sprite in all_sprites:
            camera.apply(sprite)

        tiles_group.draw(screen)
        hero_group.draw(screen)
        enemy_group.draw(screen)
        game.render(screen)

        pygame.display.flip()

        clock.tick(fps)
