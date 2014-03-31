import os
import sys
import pygame
from pygame.locals import *

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

class PyManMain:
    """The main PyMan class - this class handles the main initialization and creating of the game"""

    def __init__(self, width=640, height=480):
        #Initialize the game
        pygame.init()
        self.fpsClock = pygame.time.Clock()
        #Set the window size
        self.width = width
        self.height = height
        #Change the screen
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Nations')
        #Define RGB
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)
        self.fontObj = pygame.font.Font('freesansbold.ttf', 32)
        msg = 'Nations Initialized'
        #Initialize Mouse position
        self.mousex, self.mousey = (0, 0)
        #Initialize Message
        self.msg = ''

    def MainLoop(self):
        """This is the main loop of the game"""
        clickX = 0
        clickY = 0
        timer = 0
        while True:
            if timer > 10000:
                timer = 0

            self.screen.fill(pygame.Color(0,0,0))

            msgSurfaceObj = self.fontObj.render(self.msg, False, self.blue)
            msgRectObj = msgSurfaceObj.get_rect()
            msgRectObj.topleft = (clickX, clickY)
            self.screen.blit(msgSurfaceObj, msgRectObj)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == MOUSEMOTION:
                    self.mousex, self.mousey = event.pos

                elif event.type == MOUSEBUTTONUP:
                    clickX, clickY = event.pos
                    if event.button == 1:
                        self.msg = 'left click'
                    elif event.button == 2:
                        self.msg = 'middle click'
                    elif event.button == 3:
                        self.msg = 'right click'
                    elif event.button == 4:
                        self.msg = 'scroll up'
                    elif event.button == 5:
                        self.msg = 'scroll down'

                elif event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        self.msg = 'left arrow key'
                    elif event.key == K_RIGHT:
                        self.msg = 'right arrow key'
                    elif event.key == K_UP:
                        self.msg = 'up arrow key'
                    elif event.key == K_DOWN:
                        self.msg = 'down arrow key'
                    elif event.key == K_a:
                        self.msg = 'a key'
                    elif event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT))
            pygame.display.update()
            self.fpsClock.tick(60)
            timer += 1

if __name__ == "__main__":
    MainWindow = PyManMain()
    MainWindow.MainLoop()