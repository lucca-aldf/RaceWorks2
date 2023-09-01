import pygame as pg
import random as rd
from typing import *
from geometry import *
from gui import *
from tab import *
from trackmaker_tab import *


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)

camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
race_tab = TrackMakerTab(1200, 800)
race_tab.add_pre_processing(race_tab.canvas.fill, [COLOR_BLACK])

camera.append(race_tab)


POINT_RADIUS = 31
get_new_point_color = lambda : (rd.randint(51, 204), rd.randint(51, 204), rd.randint(51, 204))
get_new_line_color = lambda : COLOR_WHITE

pg.display.set_caption("Trackmaker")

clock = pg.time.Clock()
running = True
while running:
    
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and pg.key.get_pressed()[pg.K_ESCAPE]):
            running = False
            break
        
        else:
            camera.actions(event)


        

    camera.update()
    clock.tick(60)
    
pg.quit()
