import pygame as pg
from typing import *
from geometry import *

def get_point_under_mouse(points:List[Point], mouse_position:Tuple[int, int]):
    for point in points:
        if point.rect.collidepoint(mouse_position):
            return point
        
    return None


pg.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)

POINT_RADIUS = 10
get_new_point_color = lambda : (rd.randint(51, 204), rd.randint(51, 204), rd.randint(51, 204))
get_new_line_color = lambda : COLOR_WHITE

SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Trackmaker")

lines:list[LineBetweenPoints] = []
points:List[Point] = []

dragged_point: Point | None = None
to_connect_point: Point | None = None


clock = pg.time.Clock()
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and pg.key.get_pressed()[pg.K_ESCAPE]):
            running = False
            break


        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            dragged_point = get_point_under_mouse(points, event.pos)
            if not dragged_point and pg.key.get_pressed()[pg.K_LSHIFT]:
                points.append(Point(pg.mouse.get_pos(), radius=POINT_RADIUS, color=get_new_point_color()))
            else:
                to_connect_point = None
            
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            dragged_point = None

        elif event.type == pg.MOUSEMOTION and dragged_point:
            dragged_point.move(event.rel)

        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            this_point = get_point_under_mouse(points, event.pos)

            if this_point and to_connect_point and this_point != to_connect_point:
                lines.append(LineBetweenPoints(this_point, to_connect_point, get_new_line_color()))
                to_connect_point = None

            elif this_point and not to_connect_point:
                to_connect_point = this_point

            elif not this_point and to_connect_point:
                this_point = Point(pg.mouse.get_pos(), radius=POINT_RADIUS, color=get_new_point_color())
                points.append(this_point)
                lines.append(LineBetweenPoints(this_point, to_connect_point, get_new_line_color()))
                to_connect_point


    SCREEN.fill(COLOR_BLACK)
    
    for line in lines:
        line.draw(SCREEN)
    for point in points:
        point.draw(SCREEN)

    
    pg.display.update()
    clock.tick(60)

pg.quit()
