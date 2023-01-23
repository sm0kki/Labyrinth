from pygame import *
from const import *
import pyganim

ANIMATION_DELAY = 0.1
ICON_DIR = os.path.dirname(__file__)
COLOR = "#888888"

ANIMATION_RIGHT = [('%s/data/monsters/run_right/1.png' % ICON_DIR),
                   ('%s/data/monsters/run_right/2.png' % ICON_DIR),
                   ('%s/data/monsters/run_right/3.png' % ICON_DIR),
                   ('%s/data/monsters/run_right/4.png' % ICON_DIR),
                   ('%s/data/monsters/run_right/5.png' % ICON_DIR),
                   ('%s/data/monsters/run_right/6.png' % ICON_DIR)]

ANIMATION_LEFT = [('%s/data/monsters/run_left/1.png' % ICON_DIR),
                  ('%s/data/monsters/run_left/2.png' % ICON_DIR),
                  ('%s/data/monsters/run_left/3.png' % ICON_DIR),
                  ('%s/data/monsters/run_left/4.png' % ICON_DIR),
                  ('%s/data/monsters/run_left/5.png' % ICON_DIR),
                  ('%s/data/monsters/run_left/6.png' % ICON_DIR)]


class Monster(sprite.Sprite):
    def __init__(self, x, y, x_speed, y_speed, maxLengthLeft, maxLengthUp):
        sprite.Sprite.__init__(self)
        self.image = Surface((WIDTH, HEIGHT))
        self.image = image.load("%s/monsters/stay_right/1.png" % FILE_DIR)

        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.image.set_colorkey(Color(COLOR))
        self.startX = x
        self.startY = y
        self.maxLengthLeft = maxLengthLeft
        self.maxLengthUp = maxLengthUp
        self.xvel = x_speed
        self.yvel = y_speed
        boltAnim1 = []
        boltAnim2 = []

        for anim in ANIMATION_RIGHT:
            boltAnim1.append((anim, ANIMATION_DELAY))
            self.boltAnimRight = pyganim.PygAnimation(boltAnim1)
            self.boltAnimRight.play()

        for anim in ANIMATION_LEFT:
            boltAnim2.append((anim, ANIMATION_DELAY))
            self.boltAnimLeft = pyganim.PygAnimation(boltAnim2)
            self.boltAnimLeft.play()

        self.boltAnimCurrent = self.boltAnimRight

    def update(self, platforms):

        self.image.blit(self.image, (0, 0))

        self.rect.y += self.yvel
        self.rect.x += self.xvel

        self.image.fill(Color(COLOR))
        self.boltAnimCurrent.blit(self.image, (0, 0))

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
                if self.boltAnimCurrent == self.boltAnimRight:
                    self.boltAnimCurrent = self.boltAnimLeft
                elif self.boltAnimCurrent == self.boltAnimLeft:
                    self.boltAnimCurrent = self.boltAnimRight
