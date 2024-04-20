import pygame
import os
import pytomlpp
import locale

NEW_FILE={
    'language':locale.getdefaultlocale()[0],
    'static':{
        'path':'static',
        'font':'none',
        'icos':'none',
        'windowsico':'main',
        'pic':'none',
        'music':'none'
    },
    'debug':'True',
    'InternetData':'off',
    'SelfData':'off',
    'Page':{
        'ShowPageName':'off',
        'ShowPageId':'off',
        'ShowPages':'off'
    }
}
class FileData:
    def __init__(self,filename='pgnote_setting.toml'):
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                f.write(pytomlpp.dumps(NEW_FILE))
        
        with open(filename, "r") as f:
            self.data = pytomlpp.load(f)
    


if __name__ == '__main__':
    l=FileData()
    print(l.data)