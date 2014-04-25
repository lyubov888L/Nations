from tile import tile
import pygame
import random

class world():
    """This is the world in which the simulation takes place"""
    def __init__(self, width=100, 
                 height=100, 
                 tiles={}, 
                 nations=[], 
                 biomes={}, 
                 biomeSize = 200, 
                 subBiomeSize = 30, 
                 biomeStrength = .5,
                 fuzzing = 1):
        self.width = width
        self.height = height
        self.tiles = tiles
        self.nations = nations
        self.biomes = biomes
        self.biomeSize = biomeSize
        self.subBiomeSize = subBiomeSize
        self.biomeStrength = biomeStrength
        self.fuzzing = fuzzing
        self.createWorld()

    def createWorld(self):
        for x in range(0, self.width + 1):
            for y in range(0, self.height + 1):
               self.generateTile(x, y)

        self.determineBiomes()
        self.determineSubBiomes() 
        for z in range(0, self.fuzzing):
            print('Fuzzing layer:', str(z + 1), 'of', self.fuzzing)
            self.altStagGenerate() 

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
        #Ungenerated Biome effect
        if(t.biome == -1):
            grass = .01 * self.biomeStrength
            forest = .01 * self.biomeStrength
            desert = .01 * self.biomeStrength
            mountain = .01 * self.biomeStrength
            water = .01 * self.biomeStrength
        #Land biome effect
        elif(t.biome == 0):
            grass = .0005 * self.biomeStrength
            forest = .0004 * self.biomeStrength
            desert = .0001 * self.biomeStrength
            mountain = .0002 * self.biomeStrength
            water = .0001 * self.biomeStrength
        #Water biome effect 
        elif(t.biome == 1):
            grass = .00001 * self.biomeStrength
            forest = .00001 * self.biomeStrength
            desert = .00001 * self.biomeStrength
            mountain = .00001 * self.biomeStrength
            water = .01 * self.biomeStrength
        #Grass biome effect
        elif(t.biome == 2):
            grass = .01 * self.biomeStrength
            forest = .001 * self.biomeStrength
            desert = .001 * self.biomeStrength
            mountain = .001 * self.biomeStrength
            water = .001 * self.biomeStrength
        #Desert biome effect
        elif(t.biome == 3):
            grass = .0001 * self.biomeStrength
            forest = .000001 * self.biomeStrength
            desert = .01 * self.biomeStrength
            mountain = .0005 * self.biomeStrength
            water = .000001 * self.biomeStrength
        #Forest biome effect
        elif(t.biome == 4):
            grass = .005 * self.biomeStrength
            forest = .01 * self.biomeStrength
            desert = .0000001 * self.biomeStrength
            mountain = .0005 * self.biomeStrength
            water = .0001 * self.biomeStrength

        #Mountain biome effect
        elif(t.biome == 5):
            grass = .000001 * self.biomeStrength
            forest = .005 * self.biomeStrength
            desert = .001 * self.biomeStrength
            mountain = .01 * self.biomeStrength
            water = .000001 * self.biomeStrength

        #Lake biome effect
        elif(t.biome == 6):
            grass = .005 * self.biomeStrength
            forest = .005 * self.biomeStrength
            desert = .00000001 * self.biomeStrength
            mountain = .0001 * self.biomeStrength
            water = .01 * self.biomeStrength

        else:
            #print(t.biome)
            grass = .1 * self.biomeStrength
            forest = .1 * self.biomeStrength
            desert = .1 * self.biomeStrength
            mountain = .1 * self.biomeStrength
            water = .1 * self.biomeStrength

        for adj in t.neighbors.values():
            if adj.terrain == -1:
                pass
            else:
                #Grass effect
                if adj.terrain == 0:
                    grass += 84.49
                    desert += .5
                    forest += 4.5
                    mountain += 1
                    water += .01
                #Desert effect
                elif adj.terrain == 1:
                    grass += 10
                    desert += 70
                    mountain += 20
                #Forest effect
                elif adj.terrain == 2:
                    grass += 4.5
                    forest += 94.415
                    mountain += .975
                    water += .01
                #Mountain effect
                elif adj.terrain == 3:
                    grass += 1
                    desert += 20
                    forest += .975
                    mountain += 78.015
                    water += .01
                #Water effect
                elif adj.terrain == 4:
                    grass += .01
                    forest += .01
                    mountain += .01
                    water += 99.97

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

    def spiralGenerateBiome(self, origin = (-1, -1), length = -1, biome = -2):
      
        vX = 1
        vY = 0
        sL = 1

        pX = origin[0]
        pY = origin[1]
        sP = 0

        for k in range(0, length + 1):

            try:
                t = self.tiles[(pX, pY)]
                t.biome = biome
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
            if(xS > xE):
                for x in range(xS, xE, -2):
                    self.generateTileTerrain(x, yS)
                for x in range(xS + 1, xE, -2):
                    self.generateTileTerrain(x, yS)

            else:
                for x in range(xS, xE, 2):
                    self.generateTileTerrain(x, yS)
                for x in range(xS + 1, xE, 2):
                    self.generateTileTerrain(x, yS)
        
        elif(xS == xE):
            if(yS > yE):
                for y in range(yS, yE, -2):
                    self.generateTileTerrain(xS, y)
                for y in range(yS + 1, yE, -2):
                    self.generateTileTerrain(xS, y)

            else:
                for y in range(yS, yE, 2):
                    self.generateTileTerrain(xS, y)
                for y in range(yS + 1, yE, 2):
                    self.generateTileTerrain(xS, y)
        else:
            print('Line is diaganol')

    def altStagGenerate(self):
        xS = 0
        xE = self.width - 1
        for y in range(0, self.height, 2):
            self.stagGenerateLine(xS, y, xE, y)
        for y in range(1, self.height, 2):
            self.stagGenerateLine(xE, y, xS, y)

    def smallSpiralGenerate(self):
        for x in range(1, self.width, 3):
            for y in range(1, self.height, 3):
                self.spiralGenerate((x, y), 8)

    def determineBiomes(self):

        for x in range(0, self.width, int(self.biomeSize / 2)):
            for y in range(0, self.height, int(self.biomeSize / 2)):
                biome = self.determineBiome()
                self.spiralGenerateBiome((x, y), (self.biomeSize * self.biomeSize), biome)

        print('Biomes Generated')

    def determineSubBiomes(self):
        
        for x in range(0, self.width, int(self.subBiomeSize)):
            for y in range(0, self.height, int(self.subBiomeSize)):
                t = self.tiles[(x, y)]
                biome = self.determineSubBiome(t.biome)
                self.spiralGenerateBiome((x, y), self.subBiomeSize * self.subBiomeSize, biome)
        print('Subbiomes Generated')

    def determineSubBiome(self, biome):
        if biome == 1:
            return 1
        else:
            biome = random.random()

            grass = 3.0
            desert = 3.3
            forest = 2.0
            mountain = 2.4
            water = .01

            total = grass + desert + forest + mountain + water
            grassP = grass / total
            desertP = desert / total + grassP
            forestP = forest / total + desertP
            mountainP = mountain / total + forestP
            waterP = water / total + mountainP

            if(biome < grassP):
                biome = 2
            elif(biome < desertP and biome >= grassP):
                biome = 3
            elif(biome < forestP and biome >= desertP):
                biome = 4
            elif(biome < mountainP and biome >= forestP):
                biome = 5
            elif(biome < waterP and biome >= mountainP):
                biome = 6
            else:
                biome = 6

            return biome

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

