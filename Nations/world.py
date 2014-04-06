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

        for x in range(0, self.width + 1):
            for y in range(0, self.height + 1):
                self.generateTileTerrain(x, y)

    def generateTile(self, xC, yC):
        """Creates a generic tile"""
        t = tile(xCoor = xC, yCoor = yC)
        self.tiles[(xC, yC)] = t

    def generateTileTerrain(self, xC, yC):
        """Determines the terrain type for a tile"""
        t = self.tiles[(xC, yC)]
        type = random.random()
        if(xC == 0 and yC == 0):
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
        grass = 0.0
        forest = 0.0
        desert = 0.0
        mountain = 0.0
        water = 0.0
        for adj in t.neighbors.values():
            if adj.terrain == -1:
                pass
            else:
                #Grass effect
                if adj.terrain == 0:
                    grass += 95.95
                    desert += .5
                    forest += 2.5
                    mountain += 1
                    water += .05
                #Desert effect
                elif adj.terrain == 1:
                    grass += .5
                    desert += 95
                    mountain += 4.5
                #Forest effect
                elif adj.terrain == 2:
                    grass += 2.5
                    forest += 95.5
                    mountain += 1.975
                    water += .025
                #Mountain effect
                elif adj.terrain == 3:
                    grass += 1
                    desert += 4.5
                    forest += 1.975
                    mountain += 92.5
                    water += .025
                #Water effect
                elif adj.terrain == 4:
                    grass += .05
                    forest += .025
                    mountain += .025
                    water += 99.9

        total = grass + forest + desert + mountain + water
        if total == 0:
            pass
        grassP = grass / total
        forestP = forest / total + grassP
        desertP = desert / total + forestP
        mountainP = mountain / total + desertP
        waterP = water / total + mountainP

        if(terrain <= grassP):
            terrain = 0
        elif(terrain <= forestP and terrain > grassP):
            terrain = 1
        elif(terrain <= desertP and terrain > forestP):
            terrain = 2
        elif(terrain <= mountainP and terrain > desertP):
            terrain = 3
        elif(terrain <= waterP and terrain > mountainP):
            terrain = 4
        else:
            terrain = 4

        return terrain

                