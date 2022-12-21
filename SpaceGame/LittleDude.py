

import random

import pygame as pg

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800
SCREEN_COLOR = (0,0,0)

pg.mixer.init()

pg.init()

pg.mixer.music.load("Mercury.wav")
pg.mixer.music.play(-1)

explosion = pg.mixer.Sound('explosion.wav')

class Player(pg.sprite.Sprite):

    def __init__(self, startingPos) -> None:
        super(Player, self).__init__()

        self.surf = pg.image.load('Rocket.png').convert() #pg.Surface((75,25))
        self.surf.set_colorkey((0,0,0), pg.RLEACCEL)
        #self.surf.fill((255,255,0))
        self.rect = self.surf.get_rect()
        self.rect.move(startingPos)

    def update(self, pressed_keys):

        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            
# After Player declaration

class Enemy(pg.sprite.Sprite):
    """These enemies will spawn randomly on the play screen
    with varying random speeds towards the left. Once they 
    exit the screen they will be destroyed to prevent entity overload"""

    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pg.image.load("missle.png").convert()
        self.surf.set_colorkey((255,255,255), pg.RLEACCEL)
        #self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(3,10)


    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Star(pg.sprite.Sprite):

    def __init__(self) -> None:
        super(Star, self).__init__()

        self.surf = pg.Surface((2,2))

        self.surf.fill((255,255,255))

        #self.surf.set_colorkey((0,0,0), pg.RLEACCEL)

        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH+20, SCREEN_WIDTH+100),
                random.randint(0, SCREEN_HEIGHT)
            )   
        )

    def update(self):
        self.rect.move_ip(-15, 0)
        if self.rect.right < 0:
            self.kill()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

screen.fill((SCREEN_COLOR))

def menu():

    global screen

    running = True

    while running:

        screen.fill((0,0,0))

        pg.draw.circle(screen,(0,0,255),(400,400),100)

        font = pg.font.SysFont('calibri', 34)

        text = pg.font.Font.render(font, "Don't go splat! Press any key to continue. Press esc to quit!", False, (0,0,0),(127,127,127))

        screen.blit(text,(50, SCREEN_HEIGHT/2))

        pg.display.flip()

        for event in pg.event.get():

            if event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    running = False

                else:

                    game()

            elif event.type == QUIT:
                running = False
            
def game():

    global screen

    ADDENEMY = pg.USEREVENT + 1
    pg.time.set_timer(ADDENEMY, 250)

    GENERATESTARS = ADDENEMY + 1
    pg.time.set_timer(GENERATESTARS, 50)

    clock = pg.time.Clock()

    screen.fill(SCREEN_COLOR)

    p1 = Player((200, 400))

    enemies = pg.sprite.Group()
    all_sprites = pg.sprite.Group()
    all_sprites.add(p1)

    stars = pg.sprite.Group()

    screen.blit(p1.surf, (50,50))

    pg.draw.circle(screen,(0,0,255),(400,400),100)

    pg.display.flip()

    running = True

    while running:

        for event in pg.event.get():
            
            if event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    running = False

            elif event.type == QUIT:
                running = False

            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

            elif event.type == GENERATESTARS:
                new_star = Star()
                stars.add(new_star)
                all_sprites.add(new_star)

        pressed_keys = pg.key.get_pressed()

        p1.update(pressed_keys)

        enemies.update()

        stars.update()

        screen.fill(SCREEN_COLOR)

        pg.draw.circle(screen,(0,0,255),(400,400),100)

        for entity in all_sprites:

            screen.blit(entity.surf, entity.rect)

        if pg.sprite.spritecollideany(p1, enemies):
            p1.kill()
            explosion.play()
            running = False

        pg.display.flip()

        clock.tick(120)
        
menu()

pg.quit()