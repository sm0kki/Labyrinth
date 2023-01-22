from labyrinth import *
from const import *


def main_window(path):
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Labyrinth")
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))
    bg.fill(Color(BACKGROUND_COLOR))
    mixer.music.load('%s/sounds/back_ground.mp3' % FILE_DIR)
    mixer.music.play(-1)
    left = right = up = down = False

    timer = pygame.time.Clock()

    labyrinth = Labyrinth(path % FILE_DIR)

    camera = Camera(camera_configure, labyrinth.total_level_width, labyrinth.total_level_height)

    hero = labyrinth.hero
    running = True
    while running:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == QUIT:
                running = False

            if e.type == KEYDOWN:
                if e.key == K_UP:
                    up = True
                elif e.key == K_LEFT:
                    left = True
                elif e.key == K_RIGHT:
                    right = True
                elif e.key == K_DOWN:
                    down = True

            if e.type == KEYUP:
                if e.key == K_UP:
                    up = False
                elif e.key == K_LEFT:
                    left = False
                elif e.key == K_RIGHT:
                    right = False
                elif e.key == K_DOWN:
                    down = False

        screen.blit(bg, (0, 0))

        monsters.update(walls)
        camera.update(hero)
        hero.update(up, left, right, down, walls)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()


if __name__ == "__main__":
    main_window('%s/levels/map_2.txt')
