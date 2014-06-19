import pygame
from pygame.locals import *
 
class CEvent:
    def on_exit(self):
        pass
    def on_event(self, event):
        if event.type == KEYDOWN:
            print(chr(event.__dict__['key']))
#            while len(key)>1:
#                key.pop()
#            key.append(chr(event.__dict__['key']))
        elif event.type == QUIT:
            self.on_exit()
 
if __name__ == "__main__" :
    event = CEvent()


