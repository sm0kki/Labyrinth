from pygame import *
from const import *


class Wall(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((WIDTH, HEIGHT))
        self.image = image.load("%s/blocks/rock.png" % FILE_DIR)
        self.rect = Rect(x, y, WIDTH, HEIGHT)


class BlockDie(Wall):
    def __init__(self, x, y):
        Wall.__init__(self, x, y)
        self.image = image.load("%s/blocks/dieBlock.png" % FILE_DIR)


class Exit(Wall):
    def __init__(self, x, y):
        Wall.__init__(self, x, y)
        self.image = image.load("%s/blocks/exit.png" % FILE_DIR)


class Grass(Wall):
    def __init__(self, x, y):
        Wall.__init__(self, x, y)
        self.image = image.load("%s/blocks/grass.png" % FILE_DIR)
