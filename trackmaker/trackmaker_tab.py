from typing import *
from tab import *
from geometry import *
import pygame as pg
from random import randint

def get_point_under_mouse(points, mouse_position:Tuple[int, int]):
    for point in points:
        if point.rect.collidepoint(mouse_position):
            return point
        
    return None

class TrackMakerTab(Tab):
    
    def __init__(self, 
                 width: int, 
                 height: int, 
                 forced_perspective=False, 
                 starting_position: Tuple[float, float] = (0, 0), 
                 starting_zoom: float = 1,
                 default_point_radius = 10) -> None:
        super().__init__(width, height, forced_perspective, starting_position, starting_zoom)

        self.points = pg.sprite.Group()
        self.lines = pg.sprite.Group()

        self.point_radius = default_point_radius
        self.generate_random_color = lambda upper_bounds=(255,255,255), lower_bounds=(0,0,0): tuple(randint(lower_bounds[i], upper_bounds[i]) for i in range(3))
    
        self.to_connect_point: BezierPoint = BezierPoint((self.point_radius, self.point_radius), self.point_radius, color=self.generate_random_color(lower_bounds=(51,51,51)))
        self.dragged_point: Point | None = None

        self.points.add(self.to_connect_point)

    def actions(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.dragged_point = get_point_under_mouse(self.points, event.pos)
            
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.dragged_point = None

        elif event.type == pg.MOUSEMOTION and self.dragged_point:
            self.dragged_point.move(event.rel)


        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3 and pg.key.get_pressed()[pg.K_LSHIFT]:
            this_point = get_point_under_mouse(self.points, event.pos)

            if not this_point:
                this_point = BezierPoint(pg.mouse.get_pos(), radius=self.point_radius, color=self.generate_random_color(lower_bounds=(51,51,51)))
                self.points.add(this_point)

                self.lines.add(LineBetweenPoints(this_point, self.to_connect_point, color=self.generate_random_color(lower_bounds=(51,51,51))))
                
                self.to_connect_point.spawn_mirror_child()
                self.to_connect_point = this_point
    
    def render(self):
        self.canvas.fill((255, 255, 255))

        for method, parameters in self.pre_processing:
            method(*parameters)

        self.canvas.blits([(sprite.img, sprite.rect) for sprite in self.lines])
        self.canvas.blits([(sprite.img, sprite.rect) for sprite in self.points])

        for method, parameters in self.post_processing:
            method(*parameters)

        return self.canvas