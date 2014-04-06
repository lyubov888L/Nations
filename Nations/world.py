from tile import tile
import pygame
import random

class world():
    """This is the world in which the simulation takes place"""
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

        self.determineBiomes()

        #x = int(self.width / 2)
        #y = int(self.height / 2)
        self.smallSpiralGenerate()

    def generateTile(self, xC, yC):
        """Creates a generic tile"""
        t = tile(xCoor = xC, yCoor = yC)
        self.tiles[(xC, yC)] = t

    def generateTileTerrain(self, xC, yC):
        """Determines the terrain type for a tile"""
        t = self.tiles[(xC, yC)]
        type = random.random()
        if(xC == 0 or yC == 0 or xC == self.width or yC == self.height):
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
        if(t.biome == 0):
            grass = .004
            forest = .003
            desert = .002
            mountain = .002
            water = .002
        else:
            grass = .00001
            forest = .00001
            desert = .00001
            mountain = .00001
            water = 1
        for adj in t.neighbors.values():
            if adj.terrain == -1:
                pass
            else:
                #Grass effect
                if adj.terrain == 0:
                    grass += 84
                    desert += .5
                    forest += 4.5
                    mountain += 1
                    water += .5
                #Desert effect
                elif adj.terrain == 1:
                    grass += 10
                    desert += 70
                    mountain += 20
                #Forest effect
                elif adj.terrain == 2:
                    grass += 4.5
                    forest += 94.025
                    mountain += .975
                    water += .5
                #Mountain effect
                elif adj.terrain == 3:
                    grass += 1
                    desert += 20
                    forest += .975
                    mountain += 77.525
                    water += .5
                #Water effect
                elif adj.terrain == 4:
                    grass += .5
                    forest += .5
                    mountain += .5
                    water += 98.5

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

    def spiralGenerateBiome(self, origin, length, biome):
        vX = 1
        vY = 0
        sL = 1

        pX = origin[0]
        pY = origin[1]
        sP = 0

        for k in range(0, length + 1):

            #print('Generating Terrain at ' + str(pX) + ', ' + str(pY))
            try:
                self.tiles[(pX, pY)].biome = biome
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
            except:
                pass

    def stagGenerate(self):
        for x in range(0, self.width + 1):
            for y in range(0, self.height + 1, 2):
                self.generateTileTerrain(x, y)
            for y in range(1, self.height + 1, 2):
                self.generateTileTerrain(x, y)

    def stagGenerateLine(self, xS, yS, xE, yE):
        if(yS == yE):
            for x in range(xS, xE + 1, 2):
                self.generateTileTerrain(x, yS)
            for x in range(xS + 1, xE + 1, 2):
                self.generateTileTerrain(x, yS)
        
        elif(xS == xE):
            for y in range(yS, yE + 1, 2):
                self.generateTileTerrain(xS, y)
            for y in range(yS + 1, yE + 1, 2):
                self.generateTileTerrain(xS, y)
        else:
            pass

    def altStagGenerate(self):
        total = self.width * self.height
        gen = 0
        x = 0
        y = 0
        xE = self.width
        yE = 0
        while(gen < total):
            self.stagGenerateLine(x, y, xE, yE)
            gen += 1
            y += 1
            xE = x
            yE = self.height
            self.stagGenerateLine(x, y, xE, yE)
            gen += 1
            x += 1
            yE = y
            xE = self.width

    def smallSpiralGenerate(self):
        for x in range(1, self.width, 3):
            for y in range(1, self.height, 3):
                self.spiralGenerate((x, y), 8)

    def determineBiomes(self):
        biomeSize = 200

        for x in range(biomeSize, self.width, int(biomeSize / 2)):
            for y in range(biomeSize, self.height, int(biomeSize / 2)):
                biome = self.determineBiome()
                self.spiralGenerateBiome((x, y), biomeSize * biomeSize, biome)


    def determineBiome(self):

        biome = random.random()

        land = 3
        water = 7
        
        total = land + water
        
        landP = land / total
        waterP = water / total

        if(biome < landP):
            biome = 0
        else:
            biome = 1

        return biome

