import pygame

import pygame
from pprint import pprint
from random import randint
from copy import deepcopy


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

    def get_cell(self, mouse_pos):
        if self.top < mouse_pos[0] < self.cell_size * self.width + self.top \
                and self.left < mouse_pos[1] < self.cell_size * self.height + self.left:
            d_x = (mouse_pos[0] - self.top) // self.cell_size
            d_y = (mouse_pos[1] - self.left) // self.cell_size
            return d_x, d_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def on_click(self, n_cell):
        if n_cell:
            x1, y1 = n_cell[0], n_cell[1]
            self.board[y1][x1] = 1

    def render(self, scr):
        y = self.left
        for i in range(len(self.board)):
            x = self.top
            for j in range(len(self.board[i])):
                pygame.draw.rect(scr, (255, 255, 255), (x, y, self.cell_size, self.cell_size), 1)
                x += self.cell_size
            y += self.cell_size




if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Game')
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    board = Board(32, 32)
    board.set_view(0, 0, 50)
    clock = pygame.time.Clock()
    running = True
    fps = 30
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.get_click(event.pos)
        screen.fill((0, 0, 0))
        board.render(screen)
        clock.tick(fps)
        pygame.display.flip()
