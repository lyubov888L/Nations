import pygame

class tile():
    """A tile describing a location in the world"""
    def __init__(self,
                 xCoor = 0,
                 yCoor = 0,
                 terrain = -1,
                 population = 0,
                 food = 0,
                 energyProj = 0,
                 energyStr = 0,
                 infra = 0,
                 ore = 0,
                 water = 0,
                 wood = 0,
                 wealth = 0,
                 landProj = 0,
                 waterProj = 0,
                 airProj = 0,
                 landStr = 0,
                 waterStr = 0,
                 airStr = 0,
                 nationality = '',
                 econProj = 0,
                 econStr = 0,
                 roughness = 0,
                 color = pygame.Color(0, 0, 0),
                 neighbors = {},
                 biome = -1,
                 owner = None,
                 jobs = [],
                 readout = '',
                 foodStorage = 0,
                 oreStorage = 0,
                 woodStorage = 0):

        self.xCoor = xCoor
        self.yCoor = yCoor
        self.terrain = terrain
        self.population = population
        self.food = food
        self.energyProj = energyProj
        self.energyStr = energyStr
        self.infra = infra
        self.ore = ore
        self.water = water
        self.wood = wood
        self.wealth = wealth
        self.landProj = landProj
        self.waterProj = waterProj
        self.airProj = airProj
        self.landStr = landStr
        self.waterStr = waterStr
        self.airStr = airStr
        self.nationality = nationality
        self.econProj = econProj
        self.econStr = econStr
        self.roughness = roughness
        self.color = color
        self.neighbors = neighbors
        self.biome = biome
        self.owner = owner
        self.jobs = jobs
        self.readout = readout
        self.foodStorage = foodStorage
        self.oreStorage = oreStorage
        self.woodStorage = woodStorage

    #def updateAttrib(self, name, val):
    #    try:
    #        eval('self.' + name + ' = ' + val)
    #    except:
    #        print('Invalid name or value given')
    #        print('Name: ' + name)
    #        print('Value: ' + val)

    def calcTileColor(self, mode=0):
        """Updates the color of the tile"""
        red = 0
        green = 0
        blue = 0
        if mode == 0:
            #Geographical View
            if(self.population < 500):
                #Ungenerated
                if(self.terrain == -1):
                    pass
                #Grassland
                elif(self.terrain == 0):
                    green = 200
                #Desert
                elif(self.terrain == 1):
                    red = 200
                    green = 200
                #Forest
                elif(self.terrain == 2):
                    green = 110
                #Mountain
                elif(self.terrain == 3):
                    red = 149
                    green = 112
                    blue = 40
                #Water
                elif(self.terrain == 4):
                    blue = 200
                #Small Road
                if(self.infra > 10 and self.infra < 20):
                    red = 200
                    green = 110
                #Large Road
                elif(self.infra >= 20):
                    red = 70
                    green = 70
                    blue = 70
            else:
                red = 200
                green = 200
                blue = 200

        elif mode == 1:
            try:
                nationColor = self.owner.color
            except:
                nationColor = (0, 0, 0) #R G B
            #Political View
            if self.terrain == 4:
                #Water
                blue = 200
           #Ungenerated
            elif(self.terrain == -1):
                pass
            #Grassland
            elif(self.terrain == 0):
                green = 200               
            #Desert
            elif(self.terrain == 1):
                red = 200
                green = 200                
            #Forest
            elif(self.terrain == 2):
                green = 110
            #Mountain
            elif(self.terrain == 3):
                red = 149
                green = 112
                blue = 40
            #Water
            elif(self.terrain == 4):
                blue = 200
            #Small Road
            if(self.infra > 10 and self.infra < 20):
                red = 200
                green = 110
            #Large Road
            elif(self.infra >= 20):
                red = 70
                green = 70
                blue = 70

            if self.terrain != 4 and self.owner != None:
                red += nationColor[0] - 100
                green += nationColor[1] - 100
                blue += nationColor[2] - 100

            if red > 255:
                red = 255
            if red < 0:
                red = 0
            if green > 255:
                green = 255
            if green < 0:
                green = 0
            if blue > 255:
                blue = 255
            if blue < 0:
                blue = 0

        self.color = pygame.Color(red, green, blue)

    def updateTileReadout(self):
        self.readout += 'Air Projection: ' + str(self.airProj) + '\n'
        self.readout += 'Air Strength: ' + str(self.airStr) + '\n'
        self.readout += 'Biome: ' + str(self.biome) + '\n'
        self.readout += 'Color: ' + str(self.color) + '\n'
        self.readout += 'Economy Projecton: ' + str(self.econProj) + '\n'
        self.readout += 'Economy Strength: ' + str(self.econStr) + '\n'
        self.readout += 'Energy Projection: ' + str(self.energyProj) + '\n'
        self.readout += 'Energy Strength: ' + str(self.energyStr) + '\n'
        self.readout += 'Food: ' + str(self.food) + '\n'
        self.readout += 'Food Storage: ' + str(self.foodStorage) + '\n'
        self.readout += 'Infrastructure: ' + str(self.infra) + '\n'
        self.readout += 'Jobs: ' + str(self.jobs) + '\n'
        self.readout += 'Land Projection: ' + str(self.landProj) + '\n'
        self.readout += 'Land Strength: ' + str(self.landStr) + '\n'
        self.readout += 'Nationality: ' + str(self.nationality) + '\n'
        self.readout += 'Neighbors: ' + str(self.neighbors) + '\n'
        self.readout += 'Ore: ' + str(self.ore) + '\n'
        self.readout += 'Ore Storage: ' + str(self.oreStorage) + '\n'
        self.readout += 'Owner: ' + str(self.owner) + '\n'
        self.readout += 'Population: ' + str(self.population) + '\n'
        self.readout += 'Roughness: ' + str(self.roughness) + '\n'
        self.readout += 'Terrain: ' + str(self.terrain) + '\n'
        self.readout += 'Water: ' + str(self.water) + '\n'
        self.readout += 'Water Projection: ' + str(self.waterProj) + '\n'
        self.readout += 'Water Strength: ' + str(self.waterStr) + '\n'
        self.readout += 'Wealth: ' + str(self.wealth) + '\n'
        self.readout += 'Wood: ' + str(self.wood) + '\n'
        self.readout += 'Wood Storage: ' + str(self.woodStorage) + '\n'
        self.readout += 'X Coordinate: ' + str(self.xCoor) + '\n'
        self.readout += 'Y Coordinate: ' + str(self.yCoor) + '\n'

    def updateResources(self):
        if self.owner != None:
            self.wealth = (self.food + self.water + 2 * self.wood + 4 * self.ore + self.foodStorage) * (self.infra * self.econStr + .1) / (self.population + 1)*1.0
            self.foodStorage += (self.food * self.owner.tech) - self.population
            if self.foodStorage < 0:
                self.foodStorage = 0

            self.oreStorage += self.ore * self.owner.tech
            self.woodStorage += self.wood * self.owner.tech

    def updatePopulation(self):
        if self.population > self.foodStorage:
            self.population = int(self.foodStorage)
            self.foodStorage -= self.population
        else:
            self.population += int(self.foodStorage * .1)

    def updateMilitaryProjection(self):
        if self.owner != None:
            self.landProj = (self.landStr * self.owner.tech) / 10.0
            self.airProj = (self.airStr * self.owner.tech) / 3.0
            self.waterProj = (self.waterStr * self.owner.tech) 

    def buildFarm(self):
        if self.water < 1:
            return 0
        else:
            self.water -= 1
            self.food += 10
            return 1

    def buildRoad(self):
        if self.oreStorage < 1:
            return 0
        else:
            self.oreStorage -= 1
            self.infra += 1
            self.roughness = self.roughness / 1.1
            return 1

    def buildIrrigation(self):
        if self.wealth < 10:
            return 0
        else:
            self.wealth -= 10
            self.water += 10
            return 1

    def buildBarracks(self):
        if self.population < 10:
            return 0
        elif self.wealth < 50:
            return 0
        else:
            self.population -= 10
            self.wealth -= 50
            self.landStr += 10
            return 1

    def buildAirbase(self):
        if self.population < 10:
            return 0
        elif self.wealth < 100:
            return 0
        else:
            self.population -= 10
            self.wealth -= 100
            self.airStr += 10
            return 1

    def buildNavalbase(self):
        if self.population < 10 or self.water < 50 or self.biome != 1:
            return 0
        elif self.wealth < 200:
            return 0
        else:
            self.population -= 10
            self.wealth -= 200
            self.waterStr += 10
            return 1

    def buildMarket(self):
        if self.wood < 10:
            return 0
        else:
            self.wood -= 10
            self.econStr += 10
            return 1

    def buildMine(self):
        if self.wood < 1:
            return 0
        else:
            self.wood -= 1
            self.ore += 1.5
            return 1

    def buildGrove(self):
        if self.water < 1:
            return 0
        else:
            self.water -= 1
            self.wood += 1.5
            return 1

    def buildPowerplant(self):
        if self.ore < 3 or self.wood < 5 or self.water < 3:
            return 0
        else:
            self.ore -= 3
            self.wood -= 5
            self.water -= 3
            self.energyStr += 15
            return 1

    def doJob(self, job):
        if(job == 'buildFarm'):
            return self.buildFarm()
        elif(job == 'buildRoad'):
            return self.buildRoad()
        elif(job == 'buildIrrigation'):
            return self.buildIrrigation()
        elif(job == 'buildBarracks'):
            return self.buildBarracks()
        elif(job == 'buildAirbase'):
            return self.buildAirbase()
        elif(job == 'buildNavalbase'):
            return self.buildNavalbase()
        elif(job == 'buildMarket'):
            return self.buildMarket()
        elif(job == 'buildMine'):
            return self.buildMine()
        elif(job == 'buildGrove'):
            return self.buildGrove()
        elif(job == 'buildPowerplant'):
            return self.buildPowerplant()
        else:
            return 0

    def doJobs(self):
        remove = self.jobs.remove
        doJob = self.doJob

        if len(self.jobs) > 0:
            jobs = self.jobs.copy()
            #print('Doing', str(len(self.jobs)), ' jobs for tile', self.xCoor, self.yCoor)
    
            count = 1
            for job in self.jobs:
                #print(job, count, 'of', str(len(self.jobs)), 'jobs')
                count += 1
                if doJob(job) == 1:
                    #print(job, 'completed')
                    jobs.remove(job)

            self.jobs = jobs

        else:
            #print('No jobs to complete')
            return 0

        #print('All jobs completed')
        return