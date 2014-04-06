from tile import tile
import pygame
import random

class world():
    """This will create a world in which the simulation takes place"""
    def __init__(self, width=100, height=100, tiles={}, nations=[]):
        self.width = width
        self.height = height
        self.tiles = tiles
        self.nations = nations
        self.createWorld()

    def createWorld(self):
        for x in range(0, self.width + 1):
            for y in range(0, self.height + 1):
               self.generateTile(x, y)

        x = int(self.width / 2)
        y = int(self.height / 2)
        self.stagGenerate()

    def generateTile(self, xC, yC):
        """Creates a generic tile"""
        t = tile(xCoor = xC, yCoor = yC)
        self.tiles[(xC, yC)] = t

    def generateTileTerrain(self, xC, yC):
        """Determines the terrain type for a tile"""
        t = self.tiles[(xC, yC)]
        type = random.random()
        if(xC == self.width / 2 and yC == self.height / 2):
            t.terrain = 4
            t.calcTileColor()
        else:
            t.neighbors = self.findNeighbors(xC, yC)
            t.terrain = self.determineTerrain(t)
            t.calcTileColor()

    def findNeighbors(self, xC, yC):
        """Finds the neighbors of a tile"""
        neighbors = {}
        for x in range(xC - 1, xC + 2):
            for y in range(yC - 1, yC + 2):
                if(x == xC and y == yC):
                    pass
                else:
                   if(x > self.width):
                       x = 0
                   elif(x < 0):
                       x = self.width
                   if(y > self.height):
                       y = 0
                   elif(y < 0):
                       y = self.height
                    
                   neighbors[(x, y)] = self.tiles[(x, y)]

        return neighbors

    def determineTerrain(self, t):
        terrain = random.random()
        grass = 0.001
        forest = 0.001
        desert = 0.001
        mountain = 0.001
        water = 0.001
        for adj in t.neighbors.values():
            if adj.terrain == -1:
                pass
            else:
                #Grass effect
                if adj.terrain == 0:
                    grass += 82.5
                    desert += .5
                    forest += 4.5
                    mountain += 1
                    water += 2
                #Desert effect
                elif adj.terrain == 1:
                    grass += 10
                    desert += 70
                    mountain += 20
                #Forest effect
                elif adj.terrain == 2:
                    grass += 4.5
                    forest += 92.525
                    mountain += .975
                    water += 2
                #Mountain effect
                elif adj.terrain == 3:
                    grass += 1
                    desert += 20
                    forest += .975
                    mountain += 76.025
                    water += 2
                #Water effect
                elif adj.terrain == 4:
                    grass += 2
                    forest += 2
                    mountain += 2
                    water += 94

        total = grass + forest + desert + mountain + water
        if total == 0:
            pass
        grassP = grass / total
        desertP = desert / total + grassP
        forestP = forest / total + desertP
        mountainP = mountain / total + forestP
        waterP = water / total + mountainP

        if(terrain <= grassP):
            terrain = 0
        elif(terrain <= desertP and terrain > grassP):
            terrain = 1
        elif(terrain <= forestP and terrain > desertP):
            terrain = 2
        elif(terrain <= mountainP and terrain > forestP):
            terrain = 3
        elif(terrain <= waterP and terrain > mountainP):
            terrain = 4
        else:
            terrain = 4

        return terrain

    def spiralGenerate(self, origin, length):
        vX = 1
        vY = 0
        sL = 1

        pX = origin[0]
        pY = origin[1]
        sP = 0

        for k in range(0, length + 1):

            #print('Generating Terrain at ' + str(pX) + ', ' + str(pY))
            self.generateTileTerrain(pX, pY)
            pX += vX
            pY += vY
            sP += 1
                
            if (sP == sL):
                sP = 0

                buffer = vX
                vX = -vY
                vY = buffer

                if (vY == 0):
                    sL += 1

    def stagGenerate(self):
        for x in range(0, self.width + 1):
            for y in range(0, self.height + 1, 2):
                self.generateTileTerrain(x, y)
            for y in range(1, self.height + 1, 2):
                self.generateTileTerrain(x, y)