import pygame
from pgnote import obj

class Object:
    def __init__(self,type):
        self.type=type

    def draw(self):
        pass

    def draw_w(self):
        if self.type == obj.types.WORD:
            pass
        elif self.type == obj.types.LETTER:
            pass
        elif self.type == obj.types.SENTENCE:
            pass
        elif self.type == obj.types.TEXT:
            pass
        elif self.type == obj.types.LONG_TEXT:
            pass
        else:
            pass

    def draw_p(self):
        pass

    def draw_d(self):
        pass

    
        

        
    

