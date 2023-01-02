import pygame


class Labyrinth:
    # создание карты
    def __init__(self, file_name, allow_to_go=0, exit_poit=-1, hero_start=2):
        self.map = []
        with open(file_name) as file:
            for line in file:
                self.map.append(list(line))
        print(self.map)
        # значения по умолчанию
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
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        screen.fill((0, 0, 0))
        game.render(screen)
        clock.tick(fps)
        pygame.display.flip()
