

import pygame as pg

from pygame.locals import QUIT, K_LEFT, K_RIGHT, K_UP, K_ESCAPE, KEYDOWN

class Dwarf(pg.sprite.Sprite):

    def __init__(self, pos) -> None:
        super(Dwarf, self).__init__()

        self.dir = 'LEFT'

        self.images = [pg.image.load('Dwarf1.png').convert(), pg.image.load('Dwarf2.png').convert()]

        self.value = 0

        self.animate()

        self.rect = self.surf.get_rect(center=pos)

    def animate(self):

        if self.value > 1:

            self.value = 0

        self.surf = self.images[self.value]

        self.value += 1

    def update(self):

        if self.dir == 'LEFT':

            self.rect.move_ip(-5, 0)

        if self.dir == 'RIGHT':

            self.rect.move_ip(5, 0)

        if self.rect.left < 32:
            self.rect.left = 32
            self.rect.move_ip(0, 32)
            self.dir = 'RIGHT'
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH-32
            self.rect.move_ip(0,32)
            self.dir = 'LEFT'
        if self.rect.top <= 32:
            self.rect.top = 32
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT-32

class Wall(pg.sprite.Sprite):

    def __init__(self, side, pos) -> None:
        super(Wall, self).__init__()

        if side == 'LEFT':

            self.surf = pg.image.load('imgs/LeftWall.png').convert()

        elif side == 'RIGHT':

            self.surf = pg.image.load('imgs/RightWall.png').convert()

        elif side == 'TOP':

            self.surf = pg.image.load('imgs/TopWall.png').convert()

        elif side == 'BOTTOM':

            self.surf = pg.image.load('imgs/LowerWall.png').convert()

        self.rect = self.surf.get_rect(center=(pos[0], pos[1]))

class Player(pg.sprite.Sprite):

    def __init__(self) -> None:
        super(Player, self).__init__()

        self.surf = pg.Surface((20,40))

        self.rect = self.surf.get_rect()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

pg.init()

pg.mixer.music.load('mushroom dance_0.ogg')
pg.mixer.music.play(-1)

animatable_sprites = pg.sprite.Group()
wall = pg.sprite.Group()
all_sprites = pg.sprite.Group()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ANIMATEEVENT = pg.USEREVENT + 1

pg.time.set_timer(ANIMATEEVENT, 500)

for i in range(25):

    new_wall = Wall('LEFT', (0, 32*i))
    wall.add(new_wall)

for i in range(1,25):

    new_wall = Wall('RIGHT', (768, 32*i))
    wall.add(new_wall)

for i in range(25):
    
    new_wall = Wall('TOP', (32*i, 0))
    wall.add(new_wall)

for i in range(25):

    new_wall = Wall('BOTTOM', (32*i, 768))
    wall.add(new_wall)

player = Player()

all_sprites.add(player)

def game():

    running = True

    for i in range(10):

        new_dwarf = Dwarf((800+(i*32), 32))

        animatable_sprites.add(new_dwarf)
        all_sprites.add(new_dwarf)


    while running:

        for entity in all_sprites:
            entity.update()

        for event in pg.event.get():

            if event.type == ANIMATEEVENT:
                for sprite in animatable_sprites:
                    sprite.animate()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            elif event.type == QUIT:
                running = False

game()

pg.quit()