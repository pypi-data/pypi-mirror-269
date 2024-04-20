import pygame
import random
import string

class Page:
    def __init__(self,name):
        self.name=name
        self.id = random.sample(string.ascii_letters + string.digits,8)
        self.place=-1

        self.events = []

    def id_change(self):
        self.id = random.sample(string.ascii_letters + string.digits,8)

    def jion(self,place):
        self.place=place

    def addevent(self,event):
        self.events.append(event)
    
    def page_event(self,event):
        for i in self.events:
            i.devent(event)

    def page_draw(self,time):
        pass
        