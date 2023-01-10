from pygame import *
import blocks
import monsters
from const import *


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.yvel = 0
        self.image = Surface((WIDTH - 3, HEIGHT - 3))

        self.rect = Rect(x + 3, y + 3, WIDTH - 3, HEIGHT - 3)
        self.image = image.load("%s/heroes/hero.png" % FILE_DIR)
        self.winner = False

    def update(self, up, left, right, down, platforms):
        if up:
            self.yvel = -MOVE_SPEED

        if left:
            self.xvel = -MOVE_SPEED

        if right:
            self.xvel = MOVE_SPEED

        if down:
            self.yvel = +MOVE_SPEED

        if not (up or down or left or right):
            self.xvel = 0
            self.yvel = 0

        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # пересечение платформы с игроком
                if isinstance(p, blocks.BlockDie) \
                        or isinstance(p,
                                      monsters.Monster):
                    self.die()
                elif isinstance(p, blocks.Exit):
                    self.winner = True  # победа
                    self.win()
                else:
                    if xvel > 0:
                        self.rect.right = p.rect.left

                    if xvel < 0:
                        self.rect.left = p.rect.right

                    if yvel > 0:
                        self.rect.bottom = p.rect.top

                    if yvel < 0:
                        self.rect.top = p.rect.bottom

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY

    def die(self):
        time.wait(500)
        self.teleporting(self.startX, self.startY)

    def win(self):
        time.wait(500)
        self.teleporting(self.startX, self.startY)