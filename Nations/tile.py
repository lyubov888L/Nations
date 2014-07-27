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
                 woodStorage = 0,
                 closestCity = 0,
                 gScore = 0,
                 fScore = 0,
                 cameFrom = None,
                 connectedCities = [],
                 improvements = [],
                 height = 0):

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
        self.closestCity = closestCity
        self.gScore = gScore # Used in A* pathfinding
        self.fScore = fScore # Used in A* pathfinding
        self.cameFrom = cameFrom # Used in A* pathfinding
        self.connectedCities = connectedCities
        self.improvements = improvements
        self.height = height

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
                if self in self.owner.borders:
                    red = 255
                    green = 0
                    blue = 0

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
        """Updates the readout of a tile"""
        self.readout = '\n'

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
        self.readout += 'Height: ' + str(self.height) + '\n'
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

    def findClosestCity(self):
        closestCity = self
        closestDistance = 9999999999
        for c in self.owner.cities:
            if c != self:
                distance = ((self.xCoor - c.xCoor)**2 + (self.yCoor - c.yCoor)**2)**.5
                if distance < closestDistance:
                    closestDistance = distance
                    closestCity = c
            else:
                pass

        return closestCity

    def updateResources(self):
        """Updates the amount of resources at a tile and sends them to the closest city"""
        self.gScore = 0
        self.fScore = 0
        self.cameFrom = None

        if self.owner != None:
            world = self.owner.world
            self.closestCity = self.findClosestCity()
            
            closestCity = self.closestCity
            closestCity.wealth = (self.foodStorage * world.FOOD_VAL + self.water * world.WATER_VAL + self.woodStorage * world.WOOD_VAL + self.oreStorage * world.ORE_VAL) * (1 + self.econStr * world.ECON_FACTOR) / (self.population + 1)*1.0
            closestCity.wealth -= self.airStr * world.AIR_COST + self.landStr * world.ARMY_COST + self.waterStr * world.NAVY_COST
            closestCity.foodStorage += (self.food * (1 + self.owner.tech * world.TECH_FACTOR)) - self.population
            
            if self.foodStorage < 0:
                self.foodStorage = 0

            closestCity.oreStorage += self.ore * (1 + self.owner.tech * world.TECH_FACTOR)
            closestCity.woodStorage += self.wood * (1 + self.owner.tech * world.TECH_FACTOR)

    def updatePopulation(self):
        """Updates the population level of the tile"""
        if self.population > self.foodStorage and self.owner != None:
            self.owner.transferResources(self.closestCity, self, 'food', (self.population - self.foodStorage))
            if self.population > self.foodStorage:
                self.population = int(self.foodStorage)
                self.foodStorage -= self.population
            else:
                self.population += int(self.foodStorage * .1)
        elif self.owner != None:
            self.population += int(self.foodStorage * .1)
        else:
            self.population = int(self.foodStorage)
            self.foodStorage -= self.population

    def updateMilitaryProjection(self):
        """Updates the military projection power of a tile"""
        if self.owner != None:
            self.landProj = (self.landStr * self.owner.tech) / 10.0
            self.airProj = (self.airStr * self.owner.tech) / 3.0
            self.waterProj = (self.waterStr * self.owner.tech) 

    def buildFarm(self):
        """Builds a farm with water"""
        world = self.owner.world
        #cost is cubic meters of water for farm 50 acres big.  50 acres * 8 cm * 12 = 194250 m^3 water
        if self.water < 194250:
            return 'water'
        elif self.wealth < 2950 * world.FOOD_VAL:
            return 'wealth'
        else:
            self.water -= 16187
            self.food += 2950
            self.improvements.append('farm')
            return 1

    def buildRoad(self):
        """Builds a road with ore"""
        world = self.owner.world
        if self.oreStorage < 7475:
            return 'ore'
        elif self.wealth < 4000000:
            return 'wealth'
        else:
            self.oreStorage -= 7475
            self.infra += 1
            self.wealth -= 4000000
            self.roughness = self.roughness / 1.1
            self.improvements.append('road')
            return 1

    def buildIrrigation(self):
        """Increases the amount of water in a tile with wealth"""
        world = self.owner.world
        if self.wealth < 10000 * world.WATER_VAL:
            return 'wealth'
        else:
            self.wealth -= 10
            self.water += 10000
            self.improvements.append('irrigation')
            return 1

    def buildBarracks(self):
        """Increases landStr in the tile with population and wealth"""
        world = self.owner.world
        if self.population < 10:
            return 'population'
        elif self.wealth < 10 * world.ARMY_COST:
            return 'wealth'
        else:
            self.population -= 10
            self.wealth -= 10 * world.ARMY_COST
            self.landStr += 10
            self.improvements.append('barracks')
            return 1

    def buildAirbase(self):
        """Increases airStr in the tile with population and wealth"""
        world = self.owner.world
        if self.population < 10:
            return 'population'
        elif self.wealth < 10 * world.AIR_COST:
            return 'wealth'
        else:
            self.population -= 10
            self.wealth -= 10 * world.AIR_COST
            self.airStr += 10
            self.improvements.append('airbase')
            return 1

    def buildNavalbase(self):
        """Increases waterStr in a tile with population and wealth"""
        world = self.owner.world
        if self.population < 10:
            return 'population'
        elif self.biome != 1:
            return 0
        elif self.wealth < 10 * world.NAVY_COST:
            return 'wealth'
        else:
            self.population -= 10
            self.wealth -= 10 * world.NAVY_COST
            self.waterStr += 10
            self.improvements.append('navalbase')
            return 1

    def buildMarket(self):
        """Increases the econStr of the tile with wood"""
        if self.woodStorage < 100:
            return 'wood'
        elif self.wealth < 100000:
            return 'wealth'
        else:
            self.wealth -= 100000
            self.woodStorage -= 100
            self.econStr += 1
            self.improvements.append('market')
            return 1

    def buildMine(self):
        """Increases the ore in a tile with wood and money"""
        if self.wood < 100:
            return 'wood'
        elif self.wealth < 100000000:
            return 'wealth'
        else:
            self.wood -= 100
            self.wealth -= 1000000
            self.ore += 224000000
            self.improvements.append('mine')
            return 1

    def buildGrove(self):
        """Increases the wood in a tile with water"""
        if self.water < 330932:
            return 'water'
        else:
            self.water -= 330932 # 2m radius circle * 12 inches * 1800 trees * 4 times a month * 12 months
            self.wood += 62640 # 1800 trees per hectacre * 34 hectacres (average tree farm size)
            self.improvements.append('grove')
            return 1

    def buildPowerplant(self):
        """Increases the energyStr in a tile with ore, water, and wood"""
        #Ignored for now
        if self.ore < 3:
            return 'ore'
        elif self.wood < 5:
            return 'wood'
        elif self.water < 3:
            return 'water'
        else:
            self.ore -= 3
            self.wood -= 5
            self.water -= 3
            self.energyStr += 15
            self.improvements.append('powerplant')
            return 1

    def doJob(self, job):
        """Attempts to do the selected job for the tile"""
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
        """Attempts to do all queued jobs in a tile"""
        if self.owner == None:
            return 0

        remove = self.jobs.remove
        doJob = self.doJob

        if len(self.jobs) > 0:
            jobs = self.jobs.copy()
            #print('Doing', str(len(self.jobs)), ' jobs for tile', self.xCoor, self.yCoor)
    
            count = 1
            for job in self.jobs:
                #print(job, count, 'of', str(len(self.jobs)), 'jobs')
                count += 1
                report = doJob(job)
                if report == 1:
                    #print(job, 'completed')
                    jobs.remove(job)
                else:
                    self.owner.transferResources(self, self.closestCity, report, 1000)
                    break

            self.jobs = jobs

        else:
            #print('No jobs to complete')
            return 0

        #print('All jobs completed')
        return