import pygame
import sys
from pgnote.event import exam_event

class Event:
    def __init__(self,func=None,use=True):
        self.func=func
        self.use=use
        
    def devent(self,event):
        if self.use and self.func:
            self.func(event)

    
    