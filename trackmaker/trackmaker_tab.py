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

def generate_random_color(lower_bounds:Tuple[int,int,int]=(0,0,0), upper_bounds:Tuple[int,int,int]=(255,255,255)) -> Tuple[int,int,int]:
        return (randint(lower_bounds[0], upper_bounds[0]), randint(lower_bounds[1], upper_bounds[1]), randint(lower_bounds[2], upper_bounds[2]))


class TrackMakerTab(Tab):
    
    def __init__(self,
                 screen:pg.display,
                 width: int, 
                 height: int, 
                 forced_perspective=False, 
                 starting_position: Tuple[float, float] = (0, 0), 
                 starting_zoom: float = 1,
                 default_point_radius = 10) -> None:
        super().__init__(screen, width, height, forced_perspective, starting_position, starting_zoom)

        self.points = pg.sprite.Group()
        self.lines = pg.sprite.Group()
        self.splines = pg.sprite.Group()

        self.point_radius = default_point_radius
        first_color, second_color = generate_random_color(lower_bounds=(51,51,51)), generate_random_color(lower_bounds=(51,51,51))

        first_spline = Spline(
            (Point((50,50), self.point_radius, first_color),
            Point((50,150), self.point_radius, first_color),
            Point((150,150), self.point_radius, second_color),
            Point((350,150), self.point_radius, second_color)),
            generate_random_color(lower_bounds=(51,51,51)))
        
        self.points.add(first_spline.points)
        self.lines.add(first_spline.lines)
        self.splines.add(first_spline)

                
    
        self.to_connect_point: Point = list(self.splines)[-1].end_point
        self.dragged_point: Point | None = None

    def actions(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.dragged_point = get_point_under_mouse(self.points, event.pos)
            
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.dragged_point = None

        elif event.type == pg.MOUSEMOTION and self.dragged_point:
            self.dragged_point.move(event.rel)


        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:# and pg.key.get_pressed()[pg.K_LSHIFT]:
            this_point = get_point_under_mouse(self.points, event.pos)

            if not this_point:
                mouse_pos = pg.mouse.get_pos()
                first_half_color = self.to_connect_point.get_color()
                second_half_color = generate_random_color(lower_bounds=(51,51,51))

                this_spline = Spline((self.to_connect_point,
                                      Point((mouse_pos[0] + 40, mouse_pos[1]), self.point_radius, first_half_color),
                                      Point((mouse_pos[0] + 70, mouse_pos[1]), self.point_radius, second_half_color),
                                      Point((mouse_pos[0] + 100, mouse_pos[1]), self.point_radius, second_half_color)),
                                    generate_random_color(lower_bounds=(51,51,51)))
                                      
                self.points.add(this_spline.points[1:])
                
                self.lines.add(this_spline.lines)

                self.splines.add(this_spline)

                
                
                self.to_connect_point = this_spline.end_point
    
    def render(self):
        self.canvas.fill((0, 0, 0))

        for method, parameters in self.pre_processing:
            method(*parameters)

        self.canvas.blits([(sprite.img, sprite.rect) for sprite in self.points])
        self.canvas.blits([(sprite.img, sprite.rect) for sprite in self.lines])
        self.canvas.blits([(sprite.img, sprite.rect) for sprite in self.splines])

        for method, parameters in self.post_processing:
            method(*parameters)

        return self.canvas, self.rect