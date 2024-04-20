import pygame
from pgnote import event,page
import platform
import pycountry
import locale
import pytomlpp

class Center:
    def __init__(self,name='Pygame',size=None,tick=60):
        #data
        pygame.init()
        self.name = name
        self.tick = tick
        dpinfo = pygame.display.Info()
        if not size:
            self.size = (int(dpinfo.current_w*0.618), int(dpinfo.current_h*0.618))
        self.pages=[]
        #show information
        print('Center get information:')
        print('max window:('+str(dpinfo.current_w)+','+str(dpinfo.current_h)+')')
        fonts = pygame.font.get_fonts()
        if not fonts:
            print('fonts:not found(It is not an error, it may be caused by your system)')
        elif fonts.__len__()<10:
            first_fonts = fonts
            print('fonts:',first_fonts)
        else:
            first_fonts = fonts[0:10:1]
            print('fonts(top ten):',first_fonts)

        system = platform.system()
        print('system:'+system)
                
        self.language = locale.getdefaultlocale()[0]
        if self.language:
            print("language:", self.language)
        
        

        
        
    
    def run(self):
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.name)

        self.page_init()
        self.nowpage=self.pages[0]

        # 时钟
        self.clock = pygame.time.Clock()
        self.clock.tick(self.tick)
        
        global event
        self.QuitEvent=event.Event(func=event.exam_event.quit_event)
        
        while True:
            for event in pygame.event.get():
                self.nowpage.page_event(event)
                self.QuitEvent.devent(event)
            nowtime=pygame.time.get_ticks()
            self.nowpage.page_draw(nowtime)
            
            pygame.display.update()

    
    def page_init(self):
        if self.pages == []:
            self.pages.append(page.Page('runpage'))

        idlist=[]
        for i in self.pages:
            while i.id in idlist:
                i.id_change()
            idlist.append(i.id)
            

    def changepage(self,name=None,id=None):
        if name:
            for i in self.pages:
                if i.name==name:
                    self.nowpage=i
                    break
        elif id:
            for i in self.pages:
                if i.id==id:
                    self.nowpage=i
                    break
        else:
            self.nowpage=self.pages[self.nowpage.place+1]

    def jion_page(self,page):
        place=self.pages.__len__()
        page.jion(place)
        self.pages.append(page)
        


if __name__ == '__main__':
    c = Center()
    #c.run()
    
    
    