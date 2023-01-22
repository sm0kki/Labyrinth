from pygame import *
from const import *


class Monster(sprite.Sprite):
    def __init__(self, x, y, x_speed, y_speed, maxLengthLeft, maxLengthUp):
        sprite.Sprite.__init__(self)
        self.image = Surface((WIDTH, HEIGHT))
        self.image = image.load("%s/monsters/monster.png" % FILE_DIR)
        self.image = transform.scale(self.image, (WIDTH, HEIGHT))
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.startX = x
        self.startY = y
        self.maxLengthLeft = maxLengthLeft
        self.maxLengthUp = maxLengthUp
        self.xvel = x_speed
        self.yvel = y_speed

    def update(self, platforms):

        self.image.blit(self.image, (0, 0))

        self.rect.y += self.yvel
        self.rect.x += self.xvel

        self.collide(platforms)

        if abs(self.startX - self.rect.x) > self.maxLengthLeft:
            self.xvel = -self.xvel  # прошёл весь путь - разворот (по x)
        if abs(self.startY - self.rect.y) > self.maxLengthUp:
            self.yvel = -self.yvel  # прошёл весь путь - разворот (по y)

    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:  # если с чем-то или кем-то столкнулись
                self.xvel = - self.xvel  # то поворачиваем в обратную сторону
                self.yvel = - self.yvel
