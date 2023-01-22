from pygame import *
import blocks
import monsters
from const import *
import pyganim

ANIMATION_DELAY = 0.1
ICON_DIR = os.path.dirname(__file__)
COLOR = "#888888"

ANIMATION_RIGHT = [('%s/data/heroes/run_right/1.png' % ICON_DIR),
                   ('%s/data/heroes/run_right/2.png' % ICON_DIR),
                   ('%s/data/heroes/run_right/3.png' % ICON_DIR),
                   ('%s/data/heroes/run_right/4.png' % ICON_DIR),
                   ('%s/data/heroes/run_right/5.png' % ICON_DIR),
                   ('%s/data/heroes/run_right/6.png' % ICON_DIR)]

ANIMATION_LEFT = [('%s/data/heroes/run_left/1.png' % ICON_DIR),
                  ('%s/data/heroes/run_left/2.png' % ICON_DIR),
                  ('%s/data/heroes/run_left/3.png' % ICON_DIR),
                  ('%s/data/heroes/run_left/4.png' % ICON_DIR),
                  ('%s/data/heroes/run_left/5.png' % ICON_DIR),
                  ('%s/data/heroes/run_left/6.png' % ICON_DIR)]

ANIMATION_DEATH_RIGHT = [('%s/data/heroes/death_right/1.png' % ICON_DIR),
                         ('%s/data/heroes/death_right/2.png' % ICON_DIR),
                         ('%s/data/heroes/death_right/3.png' % ICON_DIR),
                         ('%s/data/heroes/death_right/4.png' % ICON_DIR),
                         ('%s/data/heroes/death_right/5.png' % ICON_DIR),
                         ('%s/data/heroes/death_right/6.png' % ICON_DIR),
                         ('%s/data/heroes/death_right/7.png' % ICON_DIR),
                         ('%s/data/heroes/death_right/8.png' % ICON_DIR), ]

ANIMATION_DEATH_LEFT = [('%s/data/heroes/death_left/1.png' % ICON_DIR),
                        ('%s/data/heroes/death_left/2.png' % ICON_DIR),
                        ('%s/data/heroes/death_left/3.png' % ICON_DIR),
                        ('%s/data/heroes/death_left/4.png' % ICON_DIR),
                        ('%s/data/heroes/death_left/5.png' % ICON_DIR),
                        ('%s/data/heroes/death_left/6.png' % ICON_DIR),
                        ('%s/data/heroes/death_left/7.png' % ICON_DIR),
                        ('%s/data/heroes/death_left/8.png' % ICON_DIR), ]

ANIMATION_STAY_LEFT = [('%s/data/heroes/stay_left/1.png' % ICON_DIR, 0.1)]

ANIMATION_STAY_RIGHT = [('%s/data/heroes/stay_right/1.png' % ICON_DIR, 0.1)]


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)

        self.xvel = 0
        self.startX = x
        self.startY = y
        self.yvel = 0
        self.image = Surface((WIDTH - 60, HEIGHT - 60))

        self.rect = Rect(x, y, WIDTH - 70, HEIGHT - 70)
        self.image.set_colorkey(Color(COLOR))
        self.winner = False
        self.stay_check = 0
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

        self.boltAnimStay_left = pyganim.PygAnimation(ANIMATION_STAY_LEFT)
        self.boltAnimStay_left.play()
        self.boltAnimStay_left.blit(self.image, (0, 0))

        self.boltAnimStay_right = pyganim.PygAnimation(ANIMATION_STAY_RIGHT)
        self.boltAnimStay_right.play()
        self.boltAnimStay_right.blit(self.image, (0, 0))


    def update(self, up, left, right, down, platforms):
        if up:
            self.yvel = -MOVE_SPEED
            if self.stay_check == 0:
                self.image.fill(Color(COLOR))
                self.boltAnimRight.blit(self.image, (0, 0))
            elif self.stay_check == 1:
                self.image.fill(Color(COLOR))
                self.boltAnimLeft.blit(self.image, (0, 0))

        if left:
            self.xvel = -MOVE_SPEED
            self.image.fill(Color(COLOR))
            self.boltAnimLeft.blit(self.image, (0, 0))
            self.stay_check = 1

        if right:
            self.xvel = MOVE_SPEED
            self.image.fill(Color(COLOR))
            self.boltAnimRight.blit(self.image, (0, 0))
            self.stay_check = 0

        if down:
            self.yvel = +MOVE_SPEED
            if self.stay_check == 0:
                self.image.fill(Color(COLOR))
                self.boltAnimRight.blit(self.image, (0, 0))
            elif self.stay_check == 1:
                self.image.fill(Color(COLOR))
                self.boltAnimLeft.blit(self.image, (0, 0))

        if not (up or down or left or right):
            self.xvel = 0
            self.yvel = 0
            if self.stay_check == 1:
                self.image.fill(Color(COLOR))
                self.boltAnimStay_left.blit(self.image, (0, 0))
            elif self.stay_check == 0:
                self.image.fill(Color(COLOR))
                self.boltAnimStay_right.blit(self.image, (0, 0))

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
