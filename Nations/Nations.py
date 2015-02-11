import os
import sys
import pygame
import pstats
from world import world
import tile
from pygame.locals import *

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

class PyManMain:
    """The main PyMan class - this class handles the main initialization and creating of the game"""

    def __init__(self, width=400, height=200):
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
        self.fontObj = pygame.font.Font('freesansbold.ttf', 24)
        msg = 'Nations Initialized'
        #Initialize Mouse position
        self.mousex, self.mousey = (0, 0)
        #Initialize Message
        self.msg = ''
        self.earth = world(width=self.width, height=self.height, viewMode = 1)

    def MainLoop(self):
        """This is the main loop of the game"""
        tiles = self.earth.tiles
        screen = self.screen

        clickX = 0
        clickY = 0
        timer = 0
        scale = 1
        camPos = [0, 0]

        w = self.width
        h = self.height

        screenArr = pygame.Surface((w, h))
        screen.fill(pygame.Color(0,0,0))

        while True:
            if timer > 10000:
                timer = 0

            #screen.fill(pygame.Color(0,0,0))
            
            #screenArr = pygame.PixelArray(screen)
            
            if scale == 1:
                camPos = [0, 0]

            pLength = int(w / scale)
            pHeight = int(h / scale)

            if camPos[0] > w - pLength:
                camPos[0] = w - pLength
            if camPos[1] > h - pHeight:
                camPos[1] = h - pHeight

            preScreen = [[0 for x in range(0, pHeight)] for x in range(0, pLength)]

            for x in range(int(camPos[0]), int(pLength + camPos[0]), 1):
                for y in range(int(camPos[1]), int(pHeight + camPos[1]), 1):
                    a = int(x - camPos[0])
                    b = int(y - camPos[1])
                    try:
                        preScreen[a][b] = tiles[(x, y)].color
                    except:
                        print('Exception at:', a, b, 'and', x, y)

            for x in range(0, pLength):
                for y in range(0, pHeight):
                    for a in range(x * scale, (x * scale) + scale):
                        for b in range(y * scale, (y * scale) + scale):
                            screenArr.set_at((a , b), preScreen[x][y])

            #del screenArr
            screen.blit(screenArr, (0, 0))

            msgSurfaceObj = self.fontObj.render(self.msg, False, self.red)
            msgRectObj = msgSurfaceObj.get_rect()
            msgRectObj.topleft = (clickX, clickY)
            screen.blit(msgSurfaceObj, msgRectObj)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == MOUSEMOTION:
                    self.mousex, self.mousey = event.pos

                elif event.type == MOUSEBUTTONUP:
                    clickX, clickY = event.pos
                    t = tiles[(int(camPos[0] + clickX/scale),int(camPos[1] + clickY/scale))]
                    if event.button == 1:
                        #Left Click
                        #self.msg = 'Biome: ' + str(t.biome)
                        print('Biome', str(t.biome))
                    elif event.button == 2:
                        #Middle Click
                        try:
                            #self.msg = t.owner.readout
                            t.owner.updateReadout()
                            print(t.owner.readout)
                        except:
                            #self.msg = 'Unclaimed Land'
                            print('Unclaimed Land')
                    elif event.button == 3:
                        #Right Click
                        #self.msg = 'Terrain: ' + str(t.terrain)
                        t.updateTileReadout()
                        print(t.readout)
                    elif event.button == 4:
                        #Scroll up
                        self.earth.changeViewMode(0)
                    elif event.button == 5:
                        #Scroll down
                        self.earth.changeViewMode(1)

                elif event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        camPos[0] -= 10
                        if camPos[0] < 0:
                            camPos[0] = 0
                    elif event.key == K_RIGHT:
                        camPos[0] += 10
                        if camPos[0] > self.width - self.width / scale:
                            camPos[0] = self.width - self.width / scale
                    elif event.key == K_UP:
                        camPos[1] -= 10
                        if camPos[1] < 0:
                            camPos[1] = 0
                    elif event.key == K_DOWN:
                        camPos[1] += 10
                        if camPos[1] > self.height - self.height / scale:
                            camPos[1] = self.height - self.height / scale
                    elif event.key == K_a:
                        print('Simulating 10 years')
                        self.earth.updateYears(10)
                        self.earth.changeViewMode(1)
                    elif event.key == K_LSHIFT:
                        scale += 1
                    elif event.key == K_LCTRL:
                        scale -= 1
                        if scale < 1:
                            scale = 1
                    elif event.key == K_RETURN:
                        self.earth.updateWorld()
                        self.earth.changeViewMode(1)      
                    elif event.key == K_BACKQUOTE:
                        command = input('\n')
                        while command != 'quit':
                            try:
                                eval(command)
                                command = input('\n')
                            except:
                                print('Exception executing command')
                                command = input('\n')
                    elif event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT))

            pygame.display.update()
            self.fpsClock.tick(30)
            timer += 1

if __name__ == "__main__":
    MainWindow = PyManMain()
    MainWindow.MainLoop()