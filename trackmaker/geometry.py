from typing import *
import pygame as pg
import pygame.gfxdraw as gfxdraw # EXPERIMENTAL !!!
import random as rd

class Element:

    def __init__(self) -> None:
        pass


class  Point(Element):
    
    def __init__(self, position:Tuple[float, float], radius:int=1, color:Tuple[int, int, int]=(-1, -1, -1)) -> None:
        super().__init__()
        self.position = position
        self.display_radius = radius
        self.color = color
    

    def move(self, movement:Tuple[float, float] | List[float]):
        self.x += movement[0]
        self.y += movement[1]

    @property
    def x(self):
        return self.position[0]
    
    @x.setter
    def x(self, value:int):
        self.position = (value, self.y)

    @property
    def y(self):
        return self.position[1]

    @y.setter
    def y(self, value:int):
        self.position = (self.x, value)

    @property
    def rect(self):
        return pg.Rect((self.x - self.display_radius, self.y - self.display_radius), (self.display_radius * 2, self.display_radius * 2))

    def draw(self, surface:pg.surface.Surface):
        gfxdraw.filled_circle(surface, self.x, self.y, self.display_radius, self.color)


class LineBetweenPoints:

    def __init__(self, this_point, the_other_point, color:Tuple[int, int, int] = (0, 0, 0)) -> None:
        self.points = [this_point, the_other_point]
        self.color = color

    def draw(self, surface:pg.surface.Surface):
        first_point, second_point = self.points
        gfxdraw.line(surface, first_point.x, first_point.y, second_point.x, second_point.y, self.color)

