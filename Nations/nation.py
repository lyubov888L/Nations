import random
import queue
import math

class nation(object):
    """A nation that manages resources and expands"""

    def __init__(self,
                 color = (0, 0, 0),
                 population = 0,
                 food = 0,
                 wealth = 0,
                 energyStr = 0,
                 infra = 0,
                 ore = 0,
                 water = 0,
                 wood = 0,
                 landStr = 0,
                 airStr = 0,
                 waterStr = 0,
                 nationality = '',
                 econStr = 0,
                 tiles = [],
                 cities = [],
                 roads = [],
                 name = '',
                 borders = [],
                 world = None,
                 readout = '',
                 consQueue = [],
                 foodStorage = 0,
                 oreStorage = 0,
                 woodStorage = 0,
                 tech = 1.0):

        self.color = color
        self.population = population
        self.food = food
        self.wealth = wealth
        self.energyStr = energyStr
        self.infra = infra
        self.ore = ore
        self.water = water
        self.wood = wood
        self.landStr = landStr
        self.airStr = airStr
        self.waterStr = waterStr
        self.nationality = nationality
        self.econStr = econStr
        self.tiles = tiles
        self.cities = cities
        self.roads = roads
        self.name = name
        self.borders = borders
        self.world = world
        self.readout = readout
        self.consQueue = consQueue
        self.foodStorage = foodStorage
        self.oreStorage = oreStorage
        self.woodStorage = woodStorage
        self.tech = tech
    
                
    def claimTile(self, t):
        if t not in self.tiles and t.terrain != -1:
            if t.owner != self and t.owner != None:
                t.owner.tiles.remove(t)
            t.owner = self
            t.jobs = []
            self.tiles.append(t)

    def findCities(self):
        for t in self.tiles:
            if (t.population > self.population / 30) and (t not in self.cities):
                self.cities.append(t)

    def findLimitingResource(self):
        rgen = (self.food, self.water, self.wood, self.ore, self.econStr)
        minval = min(rgen)
        ind = rgen.index(minval)
        if ind == 0:
            return 'food'
        elif ind == 1:
            return 'water'
        elif ind == 2:
            return 'wood'
        elif ind == 3:
            return 'ore'
        elif ind == 4:
            return 'econStr'
        else:
            return -1
    
    def increaseResourceProduction(self, resource):
        command = ''
        if resource == 'food':
            command = 'buildFarm'
        elif resource == 'water':
            command = 'buildIrrigation'
        elif resource == 'wood':
            command = 'buildGrove'
        elif resource == 'ore':
            command = 'buildMine'
        elif resource == 'econStr':
            command = 'buildMarket'
        else:
            print(str(resource), 'is not a valid argument')
            return -1
        for t in self.tiles:
            t.jobs.append(command)
            
    def buildResources(self):
        self.increaseResourceProduction(self.findLimitingResource())

    def transferResources(self, start, end, resource, amount):
        if start not in self.cities:
            print('Startpoint', str(start), 'is not a city')
            return 0
        if end not in self.cities:
            print('Endpoint', str(end), 'is not a city')
            return 0
        if amount < 0:
            print(str(amount), 'is less than 0')
            return 0
        if start not in self.roads:
            print(str(start), 'is not connected to a road')
            return 0
        if end not in self.roads:
            print(str(end), 'is not connected to a road, queuing road')
            self.queueRoad(start, end)
            return 0
        if resource == 'food':
            if amount > start.food:
                print('Amount requested greater than amount available:', str(amount), resource)
                return 0
            else:
                start.food -= amount
                end.food += amount
                return 1
        elif resource == 'water':
            if amount > start.water:
                print('Amount requested greater than amount available:', str(amount), resource)
                return 0
            else:
                start.water -= amount
                end.water += amount
                return 1
        elif resource == 'ore':
            if amount > start.ore:
                print('Amount requested greater than amount available:', str(amount), resource)
                return 0
            else:
                start.ore -= amount
                end.ore += amount
                return 1
        elif resource == 'wealth':
            if amount > start.wealth:
                print('Amount requested greater than amount available:', str(amount), resource)
                return 0
            else:
                start.wealth -= amount
                end.wealth += amount
                return 1
        elif resource == 'wood':
            if amount > start.wood:
                print('Amount requested greater than amount available:', str(amount), resource)
                return 0
            else:
                start.wood -= amount
                end.wood += amount
                return 1
        elif resource == 'population':
            if amount > start.population:
                print('Amount requested greater than amount available:', str(amount), resource)
                return 0
            else:
                start.population -= amount
                end.population += amount
                return 1
        elif resource == 'energyStr':
            if amount > start.energyStr:
                print('Amount requested greater than amount available:', str(amount), resource)
                return 0
            else:
                start.energyStr -= amount
                end.energyStr += amount
                return 1
        elif resource == 'airStr':
            if amount > start.airStr:
                print('Amount requested greater than amount available:', str(amount), resource)
                return 0
            else:
                start.airStr -= amount
                end.airStr += amount
                return 1
        elif resource == 'waterStr':
            if amount > start.waterStr:
                print('Amount requested greater than amount available:', str(amount), resource)
                return 0
            else:
                start.waterStr -= amount
                end.waterStr += amount
                return 1
        elif resource == 'landStr':
            if amount > start.landStr:
                print('Amount requested greater than amount available:', str(amount), resource)
                return 0
            else:
                start.landStr -= amount
                end.landStr += amount
                return 1

    def buildMilitary(self):
        funding = self.wealth * .025
        if self.tech > 100:
            airfund = funding * .22
            landfund = funding * .3
            navalfund = funding * .234
            while (airfund > 100) or (landfund > 50) or (navalfund > 200):
                for c in self.cities:
                    if airfund > 100:
                        c.jobs.append('buildAirBase')
                        airfund -= 100
                    if landfund > 50:
                        c.jobs.append('buildBarracks')
                        landfund -= 50
                    if navalfund > 200:
                        c.jobs.append('buildNavalBase')
                        navalfund -= 200
        else:
            landfund = funding * .6
            navalfund = funding * .2
            while (landfund > 50) or (navalfund > 200):
                for c in self.cities:
                    if landfund > 50:
                        c.jobs.append('buildBarracks')
                        landfund -= 50
                    if navalfund > 200:
                        c.jobs.append('buildNavalBase')
                        navalfund -= 200

    def queueRoad(self, start, end):
        road = self.chartPath(start, end)
        if road == 0:
            return
        for t in road:
            t.jobs.append('buildRoad')
        self.roads.append(road)

    def queueRoads(self):
        maxDistance = 1000
        
        for c in self.cities:

            connected = False

            for r in self.roads:
                if c in r:
                    connected = True
                    
            if connected:
                pass

            else:
                Q = queue.PriorityQueue()

                for ci in self.cities:
                    if c == ci:
                        pass
                    else:
                        distance = abs(c.xCoor - ci.xCoor) + abs(c.yCoor - ci.yCoor)
                        if distance > maxDistance:
                            pass
                        else:
                            tiebreaker = random.random() * 100000000
                            Q.put((distance, tiebreaker, ci))

                if Q.empty():
                    pass
                else:
                    ci = Q.get()
                    self.queueRoad(c, ci)
                

    def upgradeRoad(self, road):
        for t in road:
            t.jobs.append('buildRoad')
    
    def chartPath(self, start, end):
        path = []
        Q = queue.PriorityQueue()
        visited = []
        t = start
        count = 0
        maxcount = 1000
        while((end[2] not in path) and (count < maxcount)):
            for neighbor in t.neighbors.values():
                if neighbor in visited:
                    pass
                else:
                    if neighbor == end[2]:
                        path.append(neighbor)
                    elif neighbor.terrain == 4:
                        visited.append(neighbor)
                    distance = ((neighbor.xCoor - end[2].xCoor)**2 + (neighbor.yCoor - end[2].yCoor)**2)**.5 + (neighbor.roughness * 10)
                    tiebreaker = random.random() * 100000000
                    Q.put((distance, tiebreaker, neighbor))
                    visited.append(t)
            
            path.append(t)            
            t = Q.get()
            if len(t) > 1:
                t = t[2]
            count += 1
        if (count >= maxcount) and (end[2] not in path):
            return 0
        return path

    def chartWaterPath(self, start, end):
        path = []
        Q = queue.PriorityQueue()
        visited = []
        t = start
        count = 0
        maxcount = 1000
        while((end[2] not in path) and (count < maxcount)):
            for neighbor in t.neighbors.values():
                if neighbor in visited:
                    pass
                else:
                    if neighbor == end[2]:
                        path.append(neighbor)
                    elif neighbor.terrain != 4:
                        visited.append(neighbor)
                    distance = ((neighbor.xCoor - end[2].xCoor)**2 + (neighbor.yCoor - end[2].yCoor)**2)**.5 + (neighbor.roughness * 10)
                    tiebreaker = random.random() * 100000000
                    Q.put((distance, tiebreaker, neighbor))
                    visited.append(t)
            
            path.append(t)            
            t = Q.get()
            if len(t) > 1:
                t = t[2]
            count += 1
        if (count >= maxcount) and (end[2] not in path):
            return 0
        return path

    def updateResources(self):

        self.food = 0
        self.wealth = 0
        self.energyStr = 0
        self.infra = 0
        self.ore = 0
        self.water = 0
        self.wood = 0
        self.landStr = 0
        self.airStr = 0
        self.waterStr = 0
        self.econStr = 0
        self.foodStorage = 0
        self.oreStorage = 0
        self.woodStorage = 0

        for t in self.tiles:
            self.food += t.food
            self.energyStr += t.energyStr
            self.infra += t.infra
            self.ore += t.ore
            self.water += t.water
            self.wood += t.wood
            self.landStr += t.landStr
            self.airStr += t.airStr
            self.waterStr += t.waterStr
            self.econStr += t.econStr * self.tech
            self.wealth += t.wealth
            self.foodStorage += t.foodStorage
            self.oreStorage += t.oreStorage
            self.woodStorage += t.woodStorage

    def research(self):
        funding = self.wealth * .02
        self.tech += funding * .01

    def updatePopulation(self):
        self.population = 0

        for t in self.tiles:
            self.population += t.population

    def attackCity(self, city, enemyCity):
        enemy = enemyCity.owner
        airDist = ((city.xCoor - enemyCity.xCoor)**2 + (city.yCoor - enemyCity.yCoor)**2)**.5
        navalpath =  self.chartWaterPath((city.xCoor, city.yCoor), (enemyCity.xCoor, enemyCity.yCoor))
        navalDist = len(navalpath)
        navalEnd = navalpath[-1]
        landpath = self.chartPath((city.xCoor, city.yCoor), (enemyCity.xCoor, enemyCity.yCoor))
        landDist = len(landpath)

        if enemyCity not in landpath:
            landDist = 999999999
        if (enemyCity not in navalpath) and (((navalEnd.xCoor - enemyCity.xCoor)**2 + (navalEnd.yCoor - enemyCity.yCoor)**2)**.5 > 50):
            navalDist = 99999999

        airPhase = 0
        navalPhase = 0
        landPhase = 0

        if airDist <= city.airProj:
            airPhase = enemyCity.airStr - city.airProj
            navalPhase += airPhase
        if navalDist <= city.waterProj:
            navalPhase += enemyCity.waterStr - city.waterProj
            landPhase += navalPhase
        if landDist <= city.landProj:
            landPhase += enemyCity.landStr - city.landProj
            
            
        if landPhase < 0:
            enemyCity.airStr = airPhase
            enemyCity.waterStr = navalPhase
            enemyCity.landStr = landPhase

            if enemyCity.airStr < 0:
                enemyCity.airStr = 0
            if enemyCity.waterStr < 0:
                enemyCity.waterstr = 0
            if enemyCity.landStr < 0:
                enemyCity.landStr = 0

            self.claimTile(enemyCity)

            for x in range(city.xCoor, int(city.landProj)):
                for y in range(city.yCoor, int(city.landProj)):
                    t = self.world.tiles[(x, y)]
                    dist = ((city.xCoor - x)**2 + (city.yCoor - y)**2)**.5
                    if t.owner == enemy and dist <= city.landproj and t not in enemy.cities:
                        self.claimTile(t)

            return 1
        else:
            return 0

    def updateReadout(self):

        self.readout = ''

        self.readout += 'Name: ' + str(self.name) + '\r\n'
        self.readout += 'Population: ' + str(self.population) + '\r\n'
        self.readout += 'Tech: ' + str(self.tech) + '\r\n'
        self.readout += 'Food: ' + str(self.food) + '\r\n'
        self.readout += 'Food Storage: ' + str(self.foodStorage) + '\r\n'
        self.readout += 'Wealth: ' + str(self.wealth) + '\r\n'
        self.readout += 'Energy Strength: ' + str(self.energyStr) + '\r\n'
        self.readout += 'Infrastructure: ' + str(self.infra) + '\r\n'
        self.readout += 'Ore: ' + str(self.ore) + '\r\n'
        self.readout += 'Ore Storage: ' + str(self.oreStorage) + '\r\n'
        self.readout += 'Water: ' + str(self.water) + '\r\n'
        self.readout += 'Wood: ' + str(self.wood) + '\r\n'
        self.readout += 'Wood Storage: ' + str(self.woodStorage) + '\r\n'
        self.readout += 'Land Strength: ' + str(self.landStr) + '\r\n'
        self.readout += 'Air Strength: ' + str(self.airStr) + '\r\n'
        self.readout += 'Water Strength: ' + str(self.waterStr) + '\r\n'
        self.readout += 'Nationality: ' + str(self.nationality) + '\r\n'
        self.readout += 'Economy Strength: ' + str(self.econStr) + '\r\n'
        self.readout += 'Tiles: ' + str(len(self.tiles)) + '\r\n'
        self.readout += 'Cities: ' + str(len(self.cities)) + '\r\n'
        self.readout += 'Roads: ' + str(len(self.roads)) + '\r\n'
        self.readout += 'Borders: ' + str(len(self.borders)) + '\r\n'
        self.readout += 'World: ' + str(self.world) + '\r\n'
        self.readout += 'Construction Queue: ' + str(self.consQueue) + '\r\n'
