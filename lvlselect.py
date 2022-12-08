import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint

WIDTH = 360
HEIGHT = 480
FPS = 30

def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('Hevittica')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()

pg.draw.rect(screen, (0, 255, 0), (0, 200, 400, 30))
pg.draw.rect(screen, (0, 255, 0), (0, 275, 400, 30))
draw_text("Level 1", 40, (255, 255, 255), 55, 240)
draw_text("Level 2", 40, (255, 255, 255), 180, 240)
draw_text("Level 3", 40, (255, 255, 255), 310, 240)

running = True
while running:

    for event in pg.event.get():
            # check for closed window
            if event.type == pg.QUIT:
                running = False
    pg.display.flip()

pg.quit() 