from tile import tile
import pygame
import random
from nation import nation
import cProfile as profile
import time

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
                 fuzzing = 1,
                 viewMode = 0,
                 unclaimed = [],
                 year = 0):

        self.width = width
        self.height = height
        self.tiles = tiles
        self.nations = nations
        self.biomes = biomes
        self.biomeSize = biomeSize
        self.subBiomeSize = subBiomeSize
        self.biomeStrength = biomeStrength
        self.fuzzing = fuzzing
        self.viewMode = viewMode
        self.unclaimed = unclaimed
        self.year = year
        self.createWorld()

    def createWorld(self):
        print('Creating tiles')
        generateTile = self.generateTile
        for x in range(0, self.width + 1):
            for y in range(0, self.height + 1):
               generateTile(x, y)

        print('Determining biomes')
        self.determineBiomes()
        print('Determining sub biomes')
        self.determineSubBiomes()
        altStagGenerate = self.altStagGenerate 
        for z in range(0, self.fuzzing):
            print('Fuzzing layer:', str(z + 1), 'of', self.fuzzing)
            altStagGenerate()
            
        print('Generating Resources')
        self.generateResources()
        print('Finding Nations')
        self.findNations()
        print('World Generation Complete')

    def generateTile(self, xC, yC):
        """Creates a generic tile"""
        t = tile(xCoor = xC, yCoor = yC)
        self.tiles[(xC, yC)] = t
        t.jobs = []

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
            grass = .01 
            forest = .01 
            desert = .01 
            mountain = .01 
            water = .01 
        #Land biome effect
        elif(t.biome == 0):
            grass = .0005 
            forest = .0004 
            desert = .0001 
            mountain = .0002 
            water = .0001 
        #Water biome effect 
        elif(t.biome == 1):
            grass = .00001 
            forest = .00001 
            desert = .00001 
            mountain = .00001 
            water = .01 
        #Grass biome effect
        elif(t.biome == 2):
            grass = .01 
            forest = .001 
            desert = .001 
            mountain = .001 
            water = .001 
        #Desert biome effect
        elif(t.biome == 3):
            grass = .0001 
            forest = .000001 
            desert = .01 
            mountain = .0005 
            water = .000001 
        #Forest biome effect
        elif(t.biome == 4):
            grass = .005 
            forest = .01 
            desert = .0000001 
            mountain = .0005 
            water = .0001 

        #Mountain biome effect
        elif(t.biome == 5):
            grass = .000001 
            forest = .005 
            desert = .001 
            mountain = .01 
            water = .000001

        #Lake biome effect
        elif(t.biome == 6):
            grass = .005 
            forest = .005 
            desert = .00000001 
            mountain = .0001 
            water = .01 

        else:
            #print(t.biome)
            grass = .1 
            forest = .1
            desert = .1
            mountain = .1 
            water = .1 

        grass = grass * self.biomeStrength
        forest = forest * self.biomeStrength
        desert = desert * self.biomeStrength
        mountain = mountain * self.biomeStrength
        water = water * self.biomeStrength

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

    def spiralGenerateBiome(self, origin = (-1, -1), length = -1, biome = -2):
        #print('Generating biome at', str(origin))
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
        generateTileTerrain = self.generateTileTerrain

        for x in range(0, self.width + 1):
            for y in range(0, self.height + 1, 2):
                generateTileTerrain(x, y)
            for y in range(1, self.height + 1, 2):
                generateTileTerrain(x, y)

    def stagGenerateLine(self, xS, yS, xE, yE):
        generateTileTerrain = self.generateTileTerrain

        if(yS == yE):
            if(xS > xE):
                for x in range(xS, xE, -2):
                    generateTileTerrain(x, yS)
                for x in range(xS + 1, xE, -2):
                    generateTileTerrain(x, yS)

            else:
                for x in range(xS, xE, 2):
                    generateTileTerrain(x, yS)
                for x in range(xS + 1, xE, 2):
                    generateTileTerrain(x, yS)
        
        elif(xS == xE):
            if(yS > yE):
                for y in range(yS, yE, -2):
                    generateTileTerrain(xS, y)
                for y in range(yS + 1, yE, -2):
                    generateTileTerrain(xS, y)

            else:
                for y in range(yS, yE, 2):
                    generateTileTerrain(xS, y)
                for y in range(yS + 1, yE, 2):
                    generateTileTerrain(xS, y)
        else:
            print('Line is diaganol')

    def altStagGenerate(self):
        stagGenerateLine = self.stagGenerateLine

        xS = 0
        xE = self.width - 1
        for y in range(0, self.height, 2):
            stagGenerateLine(xS, y, xE, y)
        for y in range(1, self.height, 2):
            stagGenerateLine(xE, y, xS, y)

    def determineBiomes(self):
        determineBiome = self.determineBiome
        spiralGenerateBiome = self.spiralGenerateBiome

        for x in range(0, self.width, int(self.biomeSize / 2)):
            for y in range(0, self.height, int(self.biomeSize / 2)):
                
                biome = determineBiome()
                spiralGenerateBiome((x, y), (self.biomeSize * self.biomeSize), biome)


    def determineSubBiomes(self):
        determineSubBiome = self.determineSubBiome
        spiralGenerateBiome = self.spiralGenerateBiome

        for t in self.tiles.values():
            if t.biome == 0:
                biome = determineSubBiome(t.biome)
                spiralGenerateBiome((t.xCoor, t.yCoor), self.subBiomeSize * self.subBiomeSize, biome)

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

    def generateResources(self):
        generateTileResources = self.generateTileResources

        for t in self.tiles.values():
            generateTileResources(t)

    def generateTileResources(self, t):
        if t.terrain == 4:
            #Water effect
            t.population = 0
            t.food = 100
            t.water = 100

        elif t.terrain == 0:
            #Grasslands effect
            roll = 2*random.random()
            t.population = int(20 * roll)
            roll = 2*random.random()
            t.food = 10 * roll
            roll = 2*random.random()
            t.ore = 1 * roll
            roll = 2*random.random()
            t.water = 10 * roll
            roll = 2*random.random()
            t.wood = 5 * roll
            roll = 2*random.random()
            t.roughness = 5 * roll

        elif t.terrain == 1:
            #Desert Effect
            roll = 2*random.random()
            t.population = int(.5 * roll)
            roll = 2*random.random()
            t.food = int(.5 * roll)
            roll = 2*random.random()
            t.ore = 15 * roll
            roll = 2*random.random()
            t.water = int(.5 * roll)
            roll = 2*random.random()
            t.wood = 0
            t.roughness = 30 * roll

        elif t.terrain == 2:
            #Forest Effect
            roll = 2*random.random()
            t.population = int(5 * roll)
            roll = 2*random.random()
            t.food = 5 * roll
            roll = 2*random.random()
            t.ore = 5 * roll
            roll = 2*random.random()
            t.water = 15 * roll
            roll = 2*random.random()
            t.wood = 40 * roll
            roll = 2*random.random()
            t.roughness = 40 * roll

        elif t.terrain == 3:
            #Mountain Effect
            roll = 2*random.random()
            t.population = int(3 * roll)
            roll = 2*random.random()
            t.food = 3 * roll
            roll = 2*random.random()
            t.ore = 30 * roll
            roll = 2*random.random()
            t.water = 5 * roll
            roll = 2*random.random()
            t.wood = 5 * roll
            roll = 2*random.random()
            t.roughness = 50 * roll

    def changeViewMode(self, mode):
        for t in self.tiles.values():
            t.calcTileColor(mode)

    def findNations(self):
        for t in self.tiles.values():
            if t.population >= 39 and t.owner == None:
                r = int(random.random() * 255)
                g = int(random.random() * 255)
                b = int(random.random() * 255)
                n = nation(world = self,
                           name = str((t.xCoor, t.yCoor)),
                           color = (r, g, b),
                           tiles = [],
                           cities = [],
                           roads = [],
                           borders = [],
                           consQueue = []
                           )
                n.claimTile(t)
                self.nations.append(n)
                for nb in t.neighbors.values():
                    if nb.owner == None:
                        n.claimTile(nb)
                #print('Nation found at', str(t.xCoor) + ',', str(t.yCoor), 'with population', str(t.population)) 
                #for a in range(t.xCoor - 3, t.xCoor + 3):
                #    if a < 0 or a > self.width:
                #        pass
                #    else:
                #        for b in range(t.yCoor - 3, t.yCoor + 3):
                #            if b < 0 or b > self.height:
                #                pass
                #            else:
                #                ti = self.tiles[(a, b)]
                #                if (ti not in n.tiles) and ti.owner == None:
                #                    n.claimTile(ti)
                                    
    def updateUnclaimedLand(self):
        for t in self.tiles.values():
            if t.owner != None:
                pass
            elif t.terrain == 4:
                pass
            else:
                for n in t.neighbors.values():
                    if n.owner == None:
                        pass
                    else:
                        roll = random.random()
                        posMod = n.infra + n.population
                        negMod = n.roughness + 1
                        total = posMod + negMod
                        chance = posMod / total
                        if roll < chance:
                            n.owner.claimTile(t)

    def updateBorders(self):
        for t in self.tiles.values():
            if t.owner == None:
                pass
            elif t.terrain == 4:
                pass
            else:
                border = False
                for n in t.neighbors:
                    neighbor = self.tiles[n]
                    if neighbor.owner == None:
                        border = True
                        break
                if border:
                    t.owner.borders.append(t)
                elif t in t.owner.borders and border == False:
                    t.owner.borders.remove(t)

    def updateTiles(self):
        for t in self.tiles.values():
            if t.terrain == 4:
                pass
            else:
                t.updateTileReadout()
                t.updateResources()
                t.updatePopulation()

    def checkNation(self, country):
        
        if country.population < 1:
            print('Nation', country.name, 'was destroyed by famine')
            for t in country.tiles:
                t.owner = None
                country.tiles.remove(t)
            self.nations.remove(country)

        country.updateReadout()
            

    def updateNations(self):
        checkNation = self.checkNation
        for n in self.nations:
            n.updatePopulation()
            n.updateResources()
            n.buildMilitary()
            n.research()
            checkNation(n)
            n.findCities()

            try:
                n.queueRoads()
            except:
                n.queueRoads()

            n.buildResources()

    def updateJobs(self):
        for t in self.tiles.values():
            t.doJobs()

    def famine(self, country):
        if country.population < country.foodStorage:
            return
        else:
            count = 0
            while(count < len(country.tiles) and country.food < country.population):
                t = country.tiles[count]
                if t.food < t.population and t.foodStorage <= 0:
                    t.population -= 1
                    country.population -= 1
                count += 1
            if country.population == 0:
                print('Nation', country.name, 'was destroyed by famine')
                for t in country.tiles:
                    t.owner = None
                    country.tiles.remove(t)
                self.nations.remove(country)

    def updateWorld(self):
        t0 = time.clock()
        print('')
        print('Updating year', self.year)
        self.year += 1
        print('Updating unclaimed land')
        self.updateUnclaimedLand()
        print('Updating borders')
        self.updateBorders()
        print('Updating tiles')
        self.updateTiles()
        print('Updating nations')
        self.updateNations()
        print('Updating jobs')
        self.updateJobs()
        print('Update complete in ', time.clock() - t0, 'seconds')

    def updateYears(self, years):
        updateWorld = self.updateWorld
        for x in range(0, years):
            updateWorld()
