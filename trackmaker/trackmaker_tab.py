from typing import *
from tab import *
from geometry import *
import pygame as pg
from random import randint

def add_tuples(*tuples):
    size = len(tuples[0])
    result = [0 for _ in range(size)]

    for tuple_ in tuples:
        for i in range(size):
            result[i] += tuple_[i]
    
    return tuple(result)

def subtract_tuples(first_tuple, second_tuple, size=2):
    size = len(first_tuple)
    result = [0 for _ in range(size)]

    for i in range(size):
        result[i] += first_tuple[i]
    for i in range(size):
        result[i] -= second_tuple[i]
    
    return tuple(result)

def multiply_tuple(tuple_, scale):
    return (tuple_[0] * scale, tuple_[1] * scale)


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
        self.loops = pg.sprite.Group()

        self.points_visibility = True
        self.lines_visibility = True
        self.splines_visibility = True

        self.point_radius = default_point_radius
    
        self.to_connect_point: Point | None = None
        self.start_loop_point: Point | None = None
        self.dragged_point: Point | None = None

    def actions(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.dragged_point = get_point_under_mouse(self.points, add_tuples(event.pos, self.position))
            
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.dragged_point = None

        elif event.type == pg.MOUSEMOTION and self.dragged_point:
            self.dragged_point.move(event.rel)


        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:# and pg.key.get_pressed()[pg.K_LSHIFT]:
            this_point = get_point_under_mouse(self.points, event.pos)
            mouse_pos = add_tuples(event.pos, self.position)

            if not self.to_connect_point:
                first_color = generate_random_color(lower_bounds=(51,51,51))
                second_color = generate_random_color(lower_bounds=(51,51,51))
                
                this_spline = Spline(
                    (Point((mouse_pos[0], mouse_pos[1]), self.point_radius, first_color),
                    Point((mouse_pos[0] + 50, mouse_pos[1]), self.point_radius, first_color),
                    Point((mouse_pos[0] + 50, mouse_pos[1] + 50), self.point_radius, second_color),
                    Point((mouse_pos[0] + 100, mouse_pos[1] + 50), self.point_radius, second_color)),
                    generate_random_color(lower_bounds=(51,51,51)))
                
                self.points.add(this_spline.points)
                self.lines.add(this_spline.lines)
                self.splines.add(this_spline)

                self.start_loop_point = this_spline.start_point
                self.to_connect_point = this_spline.end_point

            elif not this_point:
                first_color = self.to_connect_point.get_color()
                second_color = generate_random_color(lower_bounds=(51,51,51))

                this_spline = Spline((self.to_connect_point,
                                      Point((mouse_pos[0] + 50, mouse_pos[1]), self.point_radius, first_color),
                                      Point((mouse_pos[0] + 50, mouse_pos[1] + 50), self.point_radius, second_color),
                                      Point((mouse_pos[0] + 100, mouse_pos[1] + 50), self.point_radius, second_color)),
                                    generate_random_color(lower_bounds=(51,51,51)))
                                      
                self.points.add(this_spline.points[1:])
                self.lines.add(this_spline.lines)
                self.splines.add(this_spline)

                self.to_connect_point = this_spline.end_point
            
            elif this_point is self.start_loop_point:
                first_color = self.to_connect_point.get_color()
                second_color = self.start_loop_point.get_color()

                this_spline = Spline((self.to_connect_point,
                                      Point((mouse_pos[0] + 50, mouse_pos[1]), self.point_radius, first_color),
                                      Point((mouse_pos[0] + 50, mouse_pos[1] + 50), self.point_radius, second_color),
                                      self.start_loop_point),
                                    generate_random_color(lower_bounds=(51,51,51)))
                                      
                self.points.add(this_spline.points[1:-1])
                self.lines.add(this_spline.lines)
                self.splines.add(this_spline)

                self.start_loop_point = None
                self.to_connect_point = None
        
        elif event.type == pg.MOUSEMOTION and pg.mouse.get_pressed()[1]:
            self.x += event.rel[0]
            self.y += event.rel[1]
            
        elif event.type == pg.KEYDOWN and pg.key.get_pressed()[pg.K_w]:
            self.y -= 100

        elif event.type == pg.KEYDOWN and pg.key.get_pressed()[pg.K_s]:
            self.y += 100
        
        elif event.type == pg.KEYDOWN and pg.key.get_pressed()[pg.K_a]:
            self.x -= 100

        elif event.type == pg.KEYDOWN and pg.key.get_pressed()[pg.K_d]:
            self.x += 100

        elif event.type == pg.KEYDOWN and pg.key.get_pressed()[pg.K_F1]:
            self.points_visibility = not self.points_visibility

        elif event.type == pg.KEYDOWN and pg.key.get_pressed()[pg.K_F2]:
            self.lines_visibility = not self.lines_visibility
        
        elif event.type == pg.KEYDOWN and pg.key.get_pressed()[pg.K_F3]:
            self.splines_visibility = not self.splines_visibility
        
        self.x = max(0, min(self.width, self.x))
        self.y = max(0, min(self.height, self.y))
    
    def render(self):
        canvas =  pg.Surface(self.screen.get_size())
        canvas.fill((0, 0, 0))

        for method, parameters in self.pre_processing:
            method(*parameters)

        if self.points_visibility:
            canvas.blits([(sprite.img, subtract_tuples(sprite.rect.topleft, self.position)) for sprite in self.points])
        if self.lines_visibility:
            canvas.blits([(sprite.img, subtract_tuples(sprite.rect.topleft, self.position)) for sprite in self.lines])
        if self.splines_visibility:
            canvas.blits([(sprite.img, subtract_tuples(sprite.rect.topleft, self.position)) for sprite in self.splines])

        for method, parameters in self.post_processing:
            method(*parameters)

        return canvas, self.rect
    
    """def save_splines(self):
        for spline in self.splines.sprites():"""