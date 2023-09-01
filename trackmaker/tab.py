from typing import *
import pygame as pg

class Tab:
    
    def __init__(self, width:int, height:int, forced_perspective=False, starting_position:Tuple[float, float]=(0, 0), starting_zoom:float=1.0) -> None:
        self.group:pg.sprite.Group = pg.sprite.Group()
        self.size = (width, height)
        self.forced_perspective = forced_perspective
        self.last_position= starting_position
        self.zoom = starting_zoom
        
        self.canvas = pg.Surface(self.size)
        self.pre_processing:List[Tuple[function, list]] = list()
        self.post_processing:List[Tuple[function, list]] = list()


    def append(self, sprite:pg.sprite.Sprite):
        self.group.add(sprite)
    

    def add_pre_processing(self, method, parameters):
        self.pre_processing.append((method, parameters))
    
    def add_post_processing(self, method, parameters):
        self.post_processing.append((method, parameters))

    def render(self):
        self.canvas.fill((255, 255, 255))

        for method, parameters in self.pre_processing:
            method(*parameters)

        self.canvas.blits([(sprite.img, sprite.rect) for sprite in self.group])

        for method, parameters in self.post_processing:
            method(*parameters)

        return self.canvas