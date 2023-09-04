from typing import *
import pygame as pg

class Tab:
    
    def __init__(self, screen:pg.display, width:int, height:int, forced_perspective=False, starting_position:Tuple[float, float]=(0, 0), starting_zoom:float=1.0) -> None:
        self.screen = screen
        self.group:pg.sprite.Group = pg.sprite.Group()
        self.width = width
        self.height = height
        self.resolution = (width, height)
        self.forced_perspective = forced_perspective
        self.position = starting_position
        self.zoom = starting_zoom
        
        #self.canvas = pg.Surface(screen.get_size())
        self.pre_processing:List[Tuple[function, list]] = list()
        self.post_processing:List[Tuple[function, list]] = list()

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
        return pg.Rect(self.x, self.y, self.width, self.height)

    def append(self, sprite:pg.sprite.Sprite):
        self.group.add(sprite)
    

    def add_pre_processing(self, method, parameters):
        self.pre_processing.append((method, parameters))
    
    def add_post_processing(self, method, parameters):
        self.post_processing.append((method, parameters))

    def render(self):
        canvas =  pg.Surface(self.screen.get_size())
        canvas.fill((255, 255, 255))

        for method, parameters in self.pre_processing:
            method(*parameters)

        canvas.blits([(sprite.img, sprite.rect) for sprite in self.group])

        for method, parameters in self.post_processing:
            method(*parameters)

        return canvas, self.rect