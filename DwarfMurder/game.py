
import random
import pygame as pg

from pygame.locals import QUIT, K_LEFT, K_RIGHT, K_UP, K_ESCAPE, KEYDOWN

class Dwarf(pg.sprite.Sprite):

    def __init__(self, pos) -> None:
        super(Dwarf, self).__init__()

        self.dir = 'LEFT'

        self.images = [pg.image.load('Dwarf1.png').convert(), pg.image.load('Dwarf2.png').convert()]

        self.images[0].set_colorkey((0,0,0), pg.RLEACCEL)

        self.images[1].set_colorkey((0,0,0), pg.RLEACCEL)

        self.value = 0

        self.animate()

        self.rect = self.surf.get_rect(center=(pos[0], pos[1]))

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

    def changeDir(self):

        if self.dir == 'LEFT':
            self.dir = 'RIGHT'
        else:
            self.dir = 'LEFT'

        """if self.rect.left < 32:
            self.rect.left = 32
            self.rect.move_ip(0, 32)
            self.dir = 'RIGHT'
        if self.rect.right > SCREEN_WIDTH-32:
            self.rect.right = SCREEN_WIDTH-32
            self.rect.move_ip(0,-32)
            self.dir = 'LEFT'
        if self.rect.top <= 32:
            self.rect.top = 32
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT-32"""

class Wall(pg.sprite.Sprite):

    def __init__(self, side, pos) -> None:
        super(Wall, self).__init__()

        if side == 'LEFT':

            self.surf = pg.image.load('LeftWall.png').convert()

        elif side == 'RIGHT':

            self.surf = pg.image.load('RightWall.png').convert()

        elif side == 'TOP':

            self.surf = pg.image.load('TopWall.png').convert()

        elif side == 'BOTTOM':

            self.surf = pg.image.load('LowerWall.png').convert()

        self.rect = self.surf.get_rect(center=(pos[0]+16, pos[1]+16))

class Player(pg.sprite.Sprite):

    def __init__(self) -> None:
        super(Player, self).__init__()

        self.surf = pg.Surface((40,20))

        self.rect = self.surf.get_rect(center=(400,768))

    def update(self, pressed_keys):

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 32:
            self.rect.left = 32
        if self.rect.right > 768:
            self.rect.right = 768

class Box(pg.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.surf = pg.image.load('Box.png')
        self.rect = self.surf.get_rect(
            center=(
                random.randint(96,704),
                random.randint(96,704)
            )
        )

class Bullet(pg.sprite.Sprite):

    def __init__(self, player_rect) -> None:
        super().__init__()

        self.surf = pg.Surface((4,7))
        self.surf.fill((0,0,125))

        self.rect = self.surf.get_rect(center=player_rect.center)

    def update(self):

        self.rect.move_ip(0, -10)

        if self.rect.bottom < 0:
            self.kill()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_COLOR = (128,75,50)

pg.init()

pg.mixer.music.load('mushroom dance_0.ogg')
pg.mixer.music.play(-1)

bullet_sound = pg.mixer.Sound('Laser2.wav')
box_break_sound = pg.mixer.Sound('Explosion.wav')
dwarf_die_sound = pg.mixer.Sound('die2.wav')

animatable_sprites = pg.sprite.Group()
wall = pg.sprite.Group()
all_sprites = pg.sprite.Group()
dwarves = pg.sprite.Group()
projectiles = pg.sprite.Group()
obstacles = pg.sprite.Group()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

screen.fill(SCREEN_COLOR)

ANIMATEEVENT = pg.USEREVENT + 1

pg.time.set_timer(ANIMATEEVENT, 500)

for i in range(25):

    new_wall = Wall('LEFT', (0, 32*i))
    wall.add(new_wall)
    screen.blit(new_wall.surf, new_wall.rect)

for i in range(3,25):

    new_wall = Wall('RIGHT', (768, 32*i))
    wall.add(new_wall)
    screen.blit(new_wall.surf, new_wall.rect)

for i in range(25):
    
    new_wall = Wall('TOP', (32*i, 0))
    wall.add(new_wall)
    screen.blit(new_wall.surf, new_wall.rect)

for i in range(25):

    new_wall = Wall('BOTTOM', (32*i, 768))
    wall.add(new_wall)
    screen.blit(new_wall.surf, new_wall.rect)

player = Player()

all_sprites.add(player)

clock = pg.time.Clock()

running = True

score = 0

def game():

    gameLoop = True

    global score

    global running
    global bullet_sound
    global dwarf_die_sound
    global box_break_sound

    for i in range(10):

        new_dwarf = Dwarf((800+(i*32), 64))

        animatable_sprites.add(new_dwarf)
        all_sprites.add(new_dwarf)
        dwarves.add(new_dwarf)

    for i in range(25):

        new_box = Box()

        all_sprites.add(new_box)
        obstacles.add(new_box)

    while gameLoop:

        for event in pg.event.get():

            if event.type == ANIMATEEVENT:
                for sprite in animatable_sprites:
                    sprite.animate()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    gameLoop = False

                elif event.key == K_UP and len(projectiles) <5:
                    pg.key.set_repeat(500,500)

                    bullet_sound.play()

                    new_bullet = Bullet(player.rect)
                    projectiles.add(new_bullet)
                    all_sprites.add(new_bullet)



            elif event.type == QUIT:
                running = False
                gameLoop = False

        for projectile in projectiles:
            if pg.sprite.spritecollideany(projectile, obstacles):

                for obstacle in obstacles:

                    if pg.sprite.spritecollideany(obstacle, projectiles):

                        box_break_sound.play()

                        obstacle.kill()

                score += 10

                projectile.kill()

        for dwarf in dwarves:
            if pg.sprite.spritecollideany(dwarf, wall):
                dwarf.rect.move_ip(0,32)
                dwarf.changeDir()

            if pg.sprite.spritecollideany(dwarf, obstacles):
                dwarf.rect.move_ip(0,32)
                dwarf.changeDir()

            if pg.sprite.spritecollideany(dwarf, projectiles):

                for projectile in projectiles:

                    if pg.sprite.spritecollideany(projectile, dwarves):

                        projectile.kill()

                dwarf_die_sound.play()
                score += 100

                dwarf.kill()

        pressed_keys = pg.key.get_pressed()

        player.update(pressed_keys)

        dwarves.update()

        projectiles.update()

        screen.fill(SCREEN_COLOR)

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        for block in wall:
            screen.blit(block.surf, block.rect)

        screen.blit(pg.font.Font.render(pg.font.SysFont('calibri', 36), f'{score}', False, (255,255,255)), (0,0))

        pg.display.flip()

        if len(dwarves) == 0:
            gameLoop = False

        clock.tick(30)

while running:

    game()

pg.quit()