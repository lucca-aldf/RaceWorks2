from typing import *
import pygame as pg
import pygame.gfxdraw as gfxdraw # EXPERIMENTAL !!!
import random as rd

class Element(pg.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()


class  Point(Element):
    
    def __init__(self, position:Tuple[float, float], radius:int=1, color:Tuple[int, int, int]=(-1, -1, -1)) -> None:
        super().__init__()
        self.position = position
        self.display_radius = radius
        self.color = color

        self.img = pg.Surface((self.display_radius * 2 + 1, self.display_radius * 2 + 1), pg.SRCALPHA)
        self.img.set_colorkey((0, 0, 0))
        gfxdraw.filled_circle(self.img, self.display_radius, self.display_radius, self.display_radius, self.color)

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
    
    def move(self, movement:Tuple[float, float] | List[float]):
        self.x += movement[0]
        self.y += movement[1]


class ChildPoint(Point):
    # Possible states of existence
    C0 = 'C0'
    C1 = 'C1'
    G1 = 'G1'

    def __init__(self, parent:Point, position: Tuple[float, float], radius: int = 1, color: Tuple[int, int, int] = (-1, -1, -1)) -> None:
        super().__init__(position, radius, color)

        self.parent = parent
        self.state = ChildPoint.C0
        
        self.img = pg.Surface((self.display_radius * 2, self.display_radius * 2), pg.SRCALPHA)
        radius = self.display_radius
        i = 0
        while radius > 2 and i < 3:
            gfxdraw.circle(self.img, self.x, self.y, radius, self.color)
            radius -= 1
            i += 1
        gfxdraw.filled_circle(self.img, self.x, self.y, radius, (255, 255, 255))

class BezierPoint(Point):

    def __init__(self, position: Tuple[float, float], radius: int = 1, color: Tuple[int, int, int] = (-1, -1, -1)) -> None:
        super().__init__(position, radius, color)

        self.children_points:List[ChildPoint] = [ChildPoint(parent=self, position=position, radius=radius, color=color)]
    
    def spawn_mirror_child(self):
        mirror_x = 2 * self.x - self.children_points[0].x
        mirror_y = 2 * self.y - self.children_points[0].y
        mirror_position = (mirror_x, mirror_y)
        self.children_points.append(ChildPoint(parent=self, position=mirror_position, radius=self.display_radius, color=self.color))

class LineBetweenPoints(Element):

    def __init__(self, this_point, the_other_point, color:Tuple[int, int, int] = (0, 0, 0)) -> None:
        super().__init__()
        self.points = [this_point, the_other_point]
        self.color = color

    @property
    def img(self):
        width = abs(self.points[0].x - self.points[1].x)
        height = abs(self.points[0].y - self.points[1].y)
        img = pg.Surface((width + 2, height + 2), pg.SRCALPHA)
        leftmost_point, rightmost_point = self.points

        if leftmost_point.x > rightmost_point.x:
            rightmost_point, leftmost_point = leftmost_point, rightmost_point


        gfxdraw.line(img, 
                     0, 
                     max(0,leftmost_point.y - rightmost_point.y), 
                     rightmost_point.x - leftmost_point.x, 
                     max(0,rightmost_point.y - leftmost_point.y), 
                     self.color)
        return img
    
    @property
    def rect(self):
        return pg.Rect(
            (min(self.points[0].x, self.points[1].x)),
            min(self.points[0].y, self.points[1].y),
            abs(self.points[0].x - self.points[1].x),
            abs(self.points[0].y - self.points[1].y))

