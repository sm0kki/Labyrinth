from pygame import *
from const import *


class Wall(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((WIDTH, HEIGHT))
        self.image = image.load("%s/blocks/wall4.png" % FILE_DIR)
        self.image = transform.scale(self.image, (WIDTH, HEIGHT))
        self.rect = Rect(x, y, WIDTH, HEIGHT)


class BlockDie(Wall):
    def __init__(self, x, y):
        Wall.__init__(self, x, y)
        self.image = image.load("%s/blocks/dieBlock3.png" % FILE_DIR)
        self.image = transform.scale(self.image, (WIDTH, HEIGHT))


class Exit(Wall):
    def __init__(self, x, y):
        Wall.__init__(self, x, y)
        self.image = image.load("%s/blocks/exit4.png" % FILE_DIR)
        self.image = transform.scale(self.image, (WIDTH, HEIGHT))


class Grass(Wall):
    def __init__(self, x, y):
        Wall.__init__(self, x, y)
        self.image = image.load("%s/blocks/grass2.png" % FILE_DIR)
        self.image = transform.scale(self.image, (WIDTH, HEIGHT))
