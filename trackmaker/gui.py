import pygame as pg
from typing import *
from tab import *
from trackmaker_tab import *


class Camera():
    
    def __init__(self, width:int, height:int, position:Tuple[float, float] = (0, 0), zoom:float = 1.0) -> None:
        self.resolution = (width, height)
        self.position = position
        self._zoom = zoom
        self.current_tab: None | Tab = None
        self.tabs:List[Tab] = list()

        pg.init()
    
        self.screen = pg.display.set_mode(self.resolution)


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
    def zoom(self):
        return self._zoom ** 2

    def zoom_in(self, delta_zoom:float):
        self._zoom += delta_zoom
    
    def append(self, tab:Tab):
        if not self.current_tab:
            self.current_tab = tab
        
        self.tabs.append(tab)
    
    def actions(self, event):
        self.current_tab.actions(event)


    def move(self, delta_position:Tuple[float, float] | List[float]):
        self.x += delta_position[0]
        self.y += delta_position[1]

    def update(self):
        if not self.current_tab:
            return None
        
        tab = self.current_tab
        
        render, rect = tab.render()
        self.screen.blit(render, rect)
        pg.display.update(rect)
        
