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
                 enemies = [],
                 name = '',
                 borders = [],
                 world = None,
                 readout = '',
                 consQueue = [],
                 foodStorage = 0,
                 oreStorage = 0,
                 woodStorage = 0,
                 tech = 1.0,
                 strength = 0):

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
        self.enemies = enemies
        self.strength = strength
    
                
    def claimTile(self, t):
        """Claims a tile for the nation"""
        if t not in self.tiles and t.terrain != -1:
            if t.owner != self and t.owner != None:
                t.owner.tiles.remove(t)
            t.owner = self
            t.jobs = []
            self.tiles.append(t)

    def findCities(self):
        """Scans tiles in nation and finds the 30 most populous cities"""
        for t in self.tiles:
            if (t.population > self.population / 30) and (t not in self.cities):
                self.cities.append(t)

    def findLimitingResource(self):
        """Finds the lowest producing resource"""
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
        """Increases resource production of selected resource"""
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
        """Builds necessary resources for the nation"""
        self.increaseResourceProduction(self.findLimitingResource())

    def transferResources(self, start, end, resource, amount, country = 0):
        """Transports a resource from a start point to an end point via roads"""
        if start not in self.cities and country == 0:
            print('Startpoint', str(start), 'is not a city')
            return 0
        elif start not in self.cities and start not in country.cities:
            print('Startpoint', str(start), 'is not a city')
            return 0
        if end not in self.cities and country == 0:
            print('Endpoint', str(end), 'is not a city')
            return 0
        elif end not in self.cities and end not in country.cities:
            print('Endpoint', str(end), 'is not a city')
            return 0
        if amount < 0:
            print(str(amount), 'is less than 0')
            return 0
        if start not in self.roads and country == 0:
            print(str(start), 'is not connected to a road, queuing road')
            self.queueRoad(start, end)
            return 0
        elif start not in self.roads and start not in country.roads:
            print(str(start), 'is not connected to a road, queuing road')
            self.queueRoad(start, end)
            country.queueRoad(start, end)
            return 0
        if end not in self.roads and country == 0:
            print(str(end), 'is not connected to a road, queuing road')
            self.queueRoad(start, end)
            return 0
        elif end not in self.roads and end not in country.roads:
            print(str(end), 'is not connected to a road, queuing road')
            self.queueRoad(start, end)
            country.queueRoad(start, end)
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
        """Manages the construction of military resources"""
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
        """Queues a road from a start point to an end point"""
        road = self.chartPath(start, end)
        if road == 0:
            return
        for t in road:
            t.jobs.append('buildRoad')
        self.roads.append(road)

    def queueRoads(self):
        """Queues road construction jobs for the nation"""
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
        """Upgrades an existing road"""
        for t in road:
            t.jobs.append('buildRoad')
    
    def chartPath(self, start, end):
        """Charts a path across land and returns a list of tiles"""
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
        """Charts a path through water and returns a list of tiles"""
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
        """Updates the record of resources within a nation"""

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

        self.strength = self.airStr + self.landStr + self.waterStr

    def research(self):
        """Increases tech level of nation based on wealth"""
        funding = self.wealth * .02
        self.tech += funding * .01

    def updatePopulation(self):
        """Updates the record of the total number of people living in the nation"""
        self.population = 0

        for t in self.tiles:
            self.population += t.population

    def attackCity(self, city, enemyCity):
        """Commences a battle from one city to another"""
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
            chance = city.airStr / city.airStr + enemyCity.airStr
            while (city.airStr > 0 and enemyCity.airStr > 0):
                battle = random.random()
                if battle <= chance:
                    enemyCity.airStr -= 1
                else:
                    city.airStr -= 1

            airPhase = enemyCity.airStr - city.airStr

            navalPhase += airPhase
        if navalDist <= city.waterProj:
            chance = city.waterStr / city.waterStr + enemyCity.waterStr
            while (city.waterStr > 0 and enemyCity.waterStr > 0):
                battle = random.random()
                if battle <= chance:
                    enemyCity.waterStr -= 1
                else:
                    city.waterStr -= 1

            navalPhase += enemyCity.waterStr - city.waterStr
            landPhase += navalPhase
        if landDist <= city.landProj:
            chance = city.landStr / city.landStr + enemyCity.landstr
            while (city.landStr > 0 and enemyCity.landStr > 0):
                battle = random.random()
                if battle <= chance:
                    enemyCity.landStr -= 1
                else:
                    city.landStr -= 1

            landPhase += enemyCity.landStr - city.landStr
            
            
        if landPhase < 0:

            if enemyCity.airStr < 0:
                enemyCity.airStr = 0
            if enemyCity.waterStr < 0:
                enemyCity.waterstr = 0
            if enemyCity.landStr < 0:
                enemyCity.landStr = 0

            self.claimTile(enemyCity)
            self.cities.append(enemyCity)

            for x in range(enemyCity.xCoor - int(enemyCity.landProj), enemyCity.xCoor + int(enemyCity.landProj)):
                for y in range(enemyCity.yCoor - int(enemyCity.landProj), enemyCity.yCoor + int(enemyCity.landProj)):
                    t = self.world.tiles[(x, y)]
                    dist = ((city.xCoor - x)**2 + (city.yCoor - y)**2)**.5
                    edist = ((enemyCity.xCoor - x)**2 + (enemyCity.yCoor - y)**2)**.5
                    if t.owner == enemy and dist <= city.landproj and (t not in enemy.cities) and edist <= enemyCity.landProj:
                        self.claimTile(t)

            return 1
        else:
            return 0

    def wageWar(self):
        """Wages a war against all enemies"""
        for e in self.enemies:
            for c in self.cities:
                for ec in e.cities:
                    self.attackCity(c, ec)

    def gatherIntel(self, country):
        """Estimates military strength of target country as a function of distance"""
        startCity = self.cities[0]
        endCity = country.cities[0]
        p = self.chartPath(startCity, endCity)
        distance = 0
        strength = 0
        if p == 0:
            sx = startCity.xCoor
            sy = startCity.yCoor
            ex = endCity.xCoor
            ey = endCity.yCoor
            distance = ((sx - ex)**2 + (sy - ey)**2)**.5
            for t in country.tiles:
                chance = 1.0 / (distance / 100.0 + 1.0 - self.tech / 1000)
                nature = random.random()
                if nature <= chance:
                    strength += t.airStr + t.landStr + t.waterStr
                else:
                    noise = random.random() + .5
                    strength += (t.airStr + t.landStr + t.waterStr) * noise

        else:
            distance = len(p)
            for t in country.tiles:
                chance = 1.0 / (distance / 500.0 + 1.0 - self.tech / 1000)
                nature = random.random()
                if nature <= chance:
                    strength += t.airStr + t.landStr + t.waterStr
                else:
                    noise = random.random() + .5
                    strength += (t.airStr + t.landStr + t.waterStr) * noise
        return strength

    def calcWarOdds(self, eStrength):
        """Calculates odds of winning a war against target country"""
        odds = self.strength / (self.strength + eStrength)
        return odds

    def calcWarCost(self, eStrength):
        """Calculates the cost of a war between two countries"""
        aCost = eStrength * 2 * 125
        bCost = self.strength * 2 * 125

        if aCost > self.strength * 2 * 125:
            aCost = self.strength * 2 * 125
        if bCost > eStrength * 2 * 125:
            bCost = eStrength * 2 * 125

        return (aCost, bCost)

    def updateReadout(self):
        """Updates the readout of a nation"""

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
