import pygame
import gui.colors as colors
from typing import Self
from abc import ABC, abstractmethod

fonts = {}

class UI_Element(ABC):
    elementSurface = None
    elementRect = None
    toUpdate = True
    
    def __init__(self, x: int, y: int, width: int, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        
        self.elementSurface = pygame.Surface((self.width, self.height))
        self.elementRect = pygame.Rect(self.x, self.y, self.width, self.height)

    def fill_normal(self):
        self.elementSurface.fill(self.fillColors["normal"])
    
    def set_to_update(self, update:bool=True):
        self.toUpdate = True
    
    @abstractmethod
    def process(self):
        pass
        
        
class Button(UI_Element):
    onclickfunction = None
    fonts = None
    is_hovering = False
    alreadyPressed = False

    def fill_normal(self):
        super().fill_normal()
        #add the text to the button
        self.elementSurface.blit(self.buttonText, [
                self.elementRect.width/2 - self.buttonText.get_rect().width/2,
                self.elementRect.height/2 - self.buttonText.get_rect().height/2
                ])
        self.set_to_update()


    def with_colors(self, normal, hover, pressed) -> Self:
        self.fillColors = {
            "normal": normal,
            "hover": hover,
            "pressed": pressed
        }
        return self
    def __init__(self, x, y, width, height, fonts, buttonText='Button', onclickFunction=None, onePress=False):
        super().__init__(x=x, y=y, width=width, height=height)
        self.fonts = fonts
        #add press functionallity to UI_Element
        
        self.onclickfunction = onclickFunction
        self.onePress=onePress
        self.fillColors['pressed'] = '#333333'
        self.buttonText = fonts["font40"].render(buttonText, True, colors.BLACK)

        
        self.fill_normal()
        
        
        
    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.fill_normal()
        #check hovering:
        if self.elementRect.collidepoint(mousePos): #mouse is hovering
            self.is_hovering = True
            self.elementSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.elementSurface.fill(self.fillColors['pressed'])
                self.set_to_update()
                if self.onePress:
                    self.onclickfunction()
                elif not self.alreadyPressed:
                    self.onclickfunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
                self.elementSurface.blit(self.buttonText, [
                    self.elementRect.width/2 - self.buttonText.get_rect().width/2,
                    self.elementRect.height/2 - self.buttonText.get_rect().height/2
                    ])
                self.set_to_update()
        else:
            if self.is_hovering:
                self.fill_normal()
                self.is_hovering = False
        

class Label(UI_Element):
    def __init__(self, x, y, width, height, font, labelText='Label'):
        super().__init__(x, y, width, height)      
        self.labelText = font.render(labelText, True, colors.WHITE)
        self.elementSurface.blit(self.labelText, [
                    self.elementRect.width/2 - self.labelText.get_rect().width/2,
                    self.elementRect.height/2 - self.labelText.get_rect().height/2
                    ])
        
    #processes things like events - ususally only used in buttons but we'll see
    def process(self):
        return super().process()
    