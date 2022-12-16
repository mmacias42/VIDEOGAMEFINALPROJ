import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint

#this sets the basics of the menu 
WIDTH = 360
HEIGHT = 480
FPS = 30


#Establishes colors I will use
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# player settings
PLAYER_FRIC = -0.2
PLAYER_GRAV = 0.9
#Print empty string until player wins
POINTS = ""

vec = pg.math.Vector2


#this establishes the main menu as the first thing you will see 
gamestate = "main menu"

#makes a class for the user
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((16, 16))
        #color of user
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (25, 25)
        self.pos = vec(25, 25)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.hitx = 0
        self.hity = 0
        self.colliding = False

    # definining movement of player with keys
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.y = 0
            self.acc.x = -0.8
        if keys[pg.K_d]:
            self.acc.y = 0
            self.acc.x = 0.8
        if keys[pg.K_w]:
            self.acc.y = -0.8
        if keys[pg.K_s]:
            self.acc.y = 0.8
    # defines result of collisions
    def collide_with_walls(self, dir, platforms, win = False):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, platforms, False)
            if hits:
                self.colliding = True
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
                # print("xdif " + str(xdiff))
                # print("ydif " + str(ydiff))

                #explains what to do if sprite hits the barrier (loses) or reaches the end (wins)
                if hits[0].rect.centerx > self.rect.centerx and xdiff > ydiff:
                    self.pos.x = hits[0].rect.left - self.rect.width/2
                    if win: 
                        print('You win!')
                    else:
                        self.pos = vec(25, 25)  
                if hits[0].rect.centerx < self.rect.centerx and xdiff > ydiff:
                    self.pos.x = hits[0].rect.right + self.rect.width/2
                    if win: 
                        print('You win!')
                    else:
                        self.pos = vec(25, 25)                 
                self.vel.x = 0
                self.centerx = self.pos.x
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
            else:
                self.colliding = False

        # defines results of colisions
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, platforms, False)
            if hits:
                self.colliding = True
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
                # print("xdif " + str(xdiff))
                # print("ydif " + str(ydiff))

                #explains what to do if sprite hits the barrier (loses) or reaches the end (wins)
                if hits[0].rect.centery > self.rect.centery and xdiff < ydiff:
                    self.pos.y = hits[0].rect.top - self.rect.height/2
                    if win: 
                        print('You win!')
                    else:
                        self.pos = vec(25, 25)  
                if hits[0].rect.centery < self.rect.centery and xdiff < ydiff:
                    self.pos.y = hits[0].rect.bottom + self.rect.height/2
                    if win: 
                        print('You win!')
                    else:                        
                        self.pos = vec(25, 25)       
                self.vel.y = 0
                self.centery = self.pos.y
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
            else:
                self.colliding = False
# defines teleportation
    def warp(self):
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT
    def update(self):
        self.acc = vec(0,0)
        self.controls()
        self.warp()
        # friction
        self.rect.center = self.pos

        self.acc += self.vel * PLAYER_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.centerx = self.pos.x
        if gamestate == 'level one':
            platforms = lvl1all_platforms
        if gamestate == 'level two':
            platforms = lvl2all_platforms
        if gamestate == 'level three':
            platforms = lvl3all_platforms
        #sets up collisions
        self.collide_with_walls('x', platforms)
        self.rect.centery = self.pos.y
        self.collide_with_walls('y', platforms)
        self.rect.center = self.pos
        self.hitx = self.hitx
        self.hity = self.hity
        platforms = mobs 
        self.collide_with_walls('x', platforms, win = True)
        self.collide_with_walls('y', platforms, win = True)

# creates platforms
class Platform(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#creates class for the cube that's the goal
class Mob(Sprite):
    def __init__(self, x, y, w, h, color):
        Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        #sets up color and spawn
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 42
        self.rect.y = HEIGHT - 42
        self.speedx = 0
        self.speedy = 0
        self.inbounds = True
    def collide_with_walls(self, dir, platforms):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, platforms, False)
            if hits:
                self.colliding = True
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
                # print("xdif " + str(xdiff))
                # print("ydif " + str(ydiff))
                if hits[0].rect.centerx > self.rect.centerx and xdiff > ydiff:
                    self.speedx *= -1
                if hits[0].rect.centerx < self.rect.centerx and xdiff > ydiff:
                    self.speedx *= -1
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
            else:
                self.colliding = False

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, platforms, False)
            if hits:
                self.colliding = True
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
                # print("xdif " + str(xdiff))
                # print("ydif " + str(ydiff))

                #whathappens at colliisions
                if hits[0].rect.centery > self.rect.centery and xdiff < ydiff:
                    self.speedy *= -1
                if hits[0].rect.centery < self.rect.centery and xdiff < ydiff:
                    self.speedy *= -1
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
            else:
                self.colliding = False


    def boundscheck(self):
        if not self.rect.x > 0 or not self.rect.x < WIDTH:
            self.speedx *=-1
        if not self.rect.y > 0 or not self.rect.y < HEIGHT:
            self.speedy *= -1

    def update(self):
        self.boundscheck()
        if gamestate == 'level one':
            platforms = lvl1all_platforms
        elif gamestate == 'level two':
            platforms = lvl2all_platforms
        elif gamestate == 'level three':
            platforms = lvl3all_platforms

        self.collide_with_walls('x', platforms)
        self.collide_with_walls('y', platforms)
        self.rect.x += self.speedx
        self.rect.y += self.speedy

#defines draw text functions and its inputs
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('Hevittica')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

#defines what is used as the level select screen
def level_select():
    screen.fill((0, 0, 0))
    pg.draw.rect(screen, (0, 255, 0), (0, 200, 400, 30))
    pg.draw.rect(screen, (0, 255, 0), (0, 275, 400, 30))
    draw_text("Level 1", 40, (255, 255, 255), 55, 240)
    draw_text("Level 2", 40, (255, 255, 255), 180, 240)
    draw_text("Level 3", 40, (255, 255, 255), 310, 240)

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()

#defines what is used as the main menu screen
def main_menu():
    screen.fill((0, 0, 0))
    pg.draw.rect(screen, (0, 255, 0), (0, 140, 400, 80))
    draw_text("Maze Runner", 60, (255, 255, 255), 180, 160)
    draw_text("Level Select", 40, (255, 255, 255), 180, 280)
    draw_text("Quit", 40, (255, 255, 255), 180, 340)


#defines what level one looks like
def level_one():
    lvl1all_sprites.update()
    
    ############ Draw ################
    # draw the background screen

    screen.fill(BLACK)
    # draw all sprites
    lvl1all_sprites.draw(screen)
    draw_text(str(POINTS), 50, WHITE, WIDTH / 2, HEIGHT / 2)

#defines what level one looks like
def level_two():
    lvl2all_sprites.update()
    
    ############ Draw ################
    # draw the background screen

    screen.fill(BLACK)
    # draw all sprites
    lvl2all_sprites.draw(screen)
    draw_text(str(POINTS), 50, WHITE, WIDTH / 2, HEIGHT / 2)

#defines what level one looks like
def level_three():
    lvl3all_sprites.update()
    
    ############ Draw ################
    # draw the background screen

    screen.fill(BLACK)
    # draw all sprites
    lvl3all_sprites.draw(screen)
    draw_text(str(POINTS), 50, WHITE, WIDTH / 2, HEIGHT / 2)

#establishes all the different sprites for the different levels
lvl1all_sprites = pg.sprite.Group()
lvl1all_platforms = pg.sprite.Group()
lvl2all_sprites = pg.sprite.Group()
lvl2all_platforms = pg.sprite.Group()
lvl3all_sprites = pg.sprite.Group()
lvl3all_platforms = pg.sprite.Group()
mobs = pg.sprite.Group()
for i in range(8):
    # instantiate mob class repeatedly
    m = Mob(randint(0, WIDTH), randint(0,HEIGHT), 25, 25, (randint(0,255), randint(0,255) , randint(0,255)))
    lvl1all_sprites.add(m)
    mobs.add(m)

#boundaries
player = Player()
platR = Platform(WIDTH - 12.5, 0, 25, HEIGHT)
platL = Platform(-12.5, 0, 25, HEIGHT)
platT = Platform(0, -12.5, WIDTH, 25)
platB = Platform(0, HEIGHT - 12.5, WIDTH, 25)

#Vertical Lines
platV2 = Platform(0.8*WIDTH, 0.1*HEIGHT, 25, 0.9*HEIGHT)
platV1 = Platform(0.1*WIDTH, 0, 25, 0.9*HEIGHT)
platV3 = Platform(0.25*WIDTH, 0.1*HEIGHT, 25, 0.9*HEIGHT)
platV4 = Platform(0.4*WIDTH, 0, 25, 0.9*HEIGHT)
platV5 = Platform(0.55*WIDTH, 0.1*HEIGHT, 25, 0.9*HEIGHT)
platV6 = Platform(0.7*WIDTH, 0, 12.5, 0.9*HEIGHT)

#level one platforms
lvl1all_sprites.add(player)
lvl1all_sprites.add(platR)
lvl1all_sprites.add(platL)
lvl1all_sprites.add(platT)
lvl1all_sprites.add(platB)
lvl1all_sprites.add(platV2)
lvl1all_sprites.add(platV1)
lvl1all_sprites.add(platV3)
lvl1all_sprites.add(platV4)
lvl1all_sprites.add(platV5)
lvl1all_sprites.add(platV6)

# all_sprites.add(mob)
lvl1all_platforms.add(platR)
lvl1all_platforms.add(platL)
lvl1all_platforms.add(platT)
lvl1all_platforms.add(platB)
lvl1all_platforms.add(platV2)
lvl1all_platforms.add(platV1)
lvl1all_platforms.add(platV3)
lvl1all_platforms.add(platV4)
lvl1all_platforms.add(platV5)
lvl1all_platforms.add(platV6)

all_sprites = pg.sprite.Group()
all_platforms = pg.sprite.Group()
mobs = pg.sprite.Group()

platR = Platform(WIDTH - 12.5, 0, 25, HEIGHT)
platL = Platform(-12.5, 0, 25, HEIGHT)
platT = Platform(0, -12.5, WIDTH, 25)
platB = Platform(0, HEIGHT - 12.5, WIDTH, 25)

#Vertical Lines
lvl2platV2 = Platform(10, 50, 305, 20)
lvl2platV1 = Platform(45, 100, 305, 20)
lvl2platV3 = Platform(10, 150, 305, 20)
lvl2platV4 = Platform(45, 200, 305, 20)
lvl2platV5 = Platform(10, 250, 305, 20)
lvl2platV6 = Platform(45, 300, 305, 20)
lvl2platV7 = Platform(10, 350, 305, 20)
lvl2platV8 = Platform(45, 400, 305, 20)


# add instances to groups
lvl2all_sprites.add(player)
lvl2all_sprites.add(platR)
lvl2all_sprites.add(platL)
lvl2all_sprites.add(platT)
lvl2all_sprites.add(platB)
lvl2all_sprites.add(lvl2platV2)
lvl2all_sprites.add(lvl2platV1)
lvl2all_sprites.add(lvl2platV3)
lvl2all_sprites.add(lvl2platV4)
lvl2all_sprites.add(lvl2platV5)
lvl2all_sprites.add(lvl2platV6)
lvl2all_sprites.add(lvl2platV7)
lvl2all_sprites.add(lvl2platV8)

# all_sprites.add(mob)
lvl2all_platforms.add(platR)
lvl2all_platforms.add(platL)
lvl2all_platforms.add(platT)
lvl2all_platforms.add(platB)
lvl2all_platforms.add(lvl2platV2)
lvl2all_platforms.add(lvl2platV1)
lvl2all_platforms.add(lvl2platV3)
lvl2all_platforms.add(lvl2platV4)
lvl2all_platforms.add(lvl2platV5)
lvl2all_platforms.add(lvl2platV6)
lvl2all_platforms.add(lvl2platV7)
lvl2all_platforms.add(lvl2platV8)

# instantiate classes
lvl3player = Player()
lvl3platR = Platform(WIDTH - 12.5, 0, 25, HEIGHT)
lvl3platL = Platform(-12.5, 0, 25, HEIGHT)
lvl3platT = Platform(0, -12.5, WIDTH, 25)
lvl3platB = Platform(0, HEIGHT - 12.5, WIDTH, 25)

#Vertical Lines
lvl3platV2 = Platform(10, 50, 305, 20)
lvl3platV1 = Platform(45, 100, 305, 20)
lvl3platV3 = Platform(10, 150, 305, 20)
lvl3platV4 = Platform(45, 200, 305, 20)
lvl3platV5 = Platform(10, 250, 305, 20)
lvl3platV6 = Platform(45, 300, 20, 185)
lvl3platV7 = Platform(90, 250, 20, 185)
lvl3platV8 = Platform(140, 300, 20, 305)
lvl3platV9 = Platform(190, 250, 20, 185)
lvl3platV10 = Platform(240, 300, 20, 305)
lvl3platV11 = Platform(295, 250, 20, 185)


# add instances to groups
lvl3all_sprites.add(lvl3player)
lvl3all_sprites.add(lvl3platR)
lvl3all_sprites.add(lvl3platL)
lvl3all_sprites.add(lvl3platT)
lvl3all_sprites.add(lvl3platB)
lvl3all_sprites.add(lvl3platV2)
lvl3all_sprites.add(lvl3platV1)
lvl3all_sprites.add(lvl3platV3)
lvl3all_sprites.add(lvl3platV4)
lvl3all_sprites.add(lvl3platV5)
lvl3all_sprites.add(lvl3platV6)
lvl3all_sprites.add(lvl3platV7)
lvl3all_sprites.add(lvl3platV8)
lvl3all_sprites.add(lvl3platV9)
lvl3all_sprites.add(lvl3platV10)
lvl3all_sprites.add(lvl3platV11)

# all_sprites.add(mob)
lvl3all_platforms.add(lvl3platR)
lvl3all_platforms.add(lvl3platL)
lvl3all_platforms.add(lvl3platT)
lvl3all_platforms.add(lvl3platB)
lvl3all_platforms.add(lvl3platV2)
lvl3all_platforms.add(lvl3platV1)
lvl3all_platforms.add(lvl3platV3)
lvl3all_platforms.add(lvl3platV4)
lvl3all_platforms.add(lvl3platV5)
lvl3all_platforms.add(lvl3platV6)
lvl3all_sprites.add(lvl3platV7)
lvl3all_sprites.add(lvl3platV8)
lvl3all_sprites.add(lvl3platV9)
lvl3all_sprites.add(lvl3platV10)
lvl3all_sprites.add(lvl3platV11)




for i in range(8):
    # instantiate mob class repeatedly
    m = Mob(randint(0, WIDTH), randint(0,HEIGHT), 25, 25, (randint(0,255), randint(0,255) , randint(0,255)))
    lvl2all_sprites.add(m)
    m = Mob(randint(0, WIDTH), randint(0,HEIGHT), 25, 25, (randint(0,255), randint(0,255) , randint(0,255)))
    lvl3all_sprites.add(m)
    mobs.add(m)

#game loop
running = True
while running:
    dt = clock.tick(FPS)
    for event in pg.event.get():
            # check for closed window
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN: 
                if event.button == 1:
                    position = pg.mouse.get_pos()
                    print(position)
                    #what happens when you click on different parts of the screen
                    if gamestate == 'main menu':
                        if 153 < position[0] <210 and 221 < position[1] < 246:
                            print('play')
                        elif 97 < position[0] <262 and 281 < position[1] < 302:
                            gamestate = 'level select'
                        elif 151 < position[0] <210 and 341 < position[1] < 363:
                            running = False
                    if gamestate == 'level select':
                        if 9 < position[0] <97 and 241 < position[1] < 262:
                            gamestate = 'level one'
                        elif 134 < position[0] <227 and 240 < position[1] < 260:
                            gamestate = 'level two'
                        elif 265 < position[0] <357 and 240 < position[1] < 259:
                            gamestate = 'level three'
                            
# if the gamestate equals something, the screen goes there
    if gamestate == 'main menu':
        main_menu()
    elif gamestate == 'level select':
        level_select()
    elif gamestate == 'level one':
        level_one()
    elif gamestate == 'level two':
        level_two()
    elif gamestate == 'level three':
        level_three()
    pg.display.flip()

pg.quit() 
