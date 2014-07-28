import random
import queue
import math
from operator import itemgetter, attrgetter

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
                 roads = set(),
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
                 strength = 0,
                 foodDeficit = 0,
                 waterDeficit = 0,
                 oreDeficit = 0,
                 woodDeficit = 0,
                 wealthDeficit = 0,
                 offers = [],
                 pendingOffers = [],
                 neighbors = dict()):

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
        self.foodDeficit = foodDeficit
        self.waterDeficit = waterDeficit
        self.oreDeficit = oreDeficit
        self.woodDeficit = woodDeficit
        self.wealthDeficit = wealthDeficit
        self.offers = offers
        self.pendingOffers = pendingOffers
        self.neighbors = neighbors
    
                
    def claimTile(self, t):
        """Claims a tile for the nation"""
        if t not in self.tiles and t.terrain != -1:
            if t.owner != self and t.owner != None:
                if t in t.owner.cities:
                    t.owner.cities.remove(t)
                t.owner.tiles.remove(t)
            t.owner = self
            t.jobs = []
            self.tiles.append(t)

    def findCities(self):
        """Scans tiles in nation and finds the most populous cities"""
        maxCities = int(len(self.tiles) / 700)
        if maxCities < 1:
            maxCities = 1
        for t in self.tiles:
            if (t.population > self.population / 30) and (t not in self.cities) and len(self.cities) < maxCities:
                if self.cities == []:               
                    self.cities.append(t)
                    self.roads.add(t)
                    t.improvements.append('road')
                else:
                    distance = ((t.closestCity.xCoor - t.xCoor)**2 + (t.closestCity.yCoor - t.yCoor)**2)**.5
                    if distance > 25:
                        self.cities.append(t)
                        self.roads.add(t)
                        t.improvements.append('road')

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
        for t in self.cities:
            if command not in t.jobs:
                t.jobs.append(command)
                self.consQueue.append(command)
            
    def buildResources(self):
        """Builds necessary resources for the nation"""
        self.increaseResourceProduction(self.findLimitingResource())

    def transferResources(self, start, end, resource, amount, country = 0):
        """Transports a resource from a start point to an end point via roads"""
        if start == end:
            #cannot transfer resources to itself.
            return 0
        
        try:
            start.xCoor
        except:
            #print('Start must be a tile')
            return 0

        try:
            end.xCoor
        except:
            #print('End must be a tile')
            return 0

        distance = ((end.xCoor - end.closestRoad.xCoor)**2 + (end.yCoor - end.closestRoad.yCoor)**2)**.5

        if amount < 0:
            print(str(amount), 'is less than 0')
            return 0
        if start not in self.roads and distance > 20 and country == 0 and end not in self.roads:
            #print(str(start), 'is not connected to a road, queuing road')
            self.queueRoad(start, end)
            return 0
        elif start not in self.roads and distance > 20 and country == 0:
            self.queueRoad(start, start.closestRoad)
            return 0
        elif start not in self.roads and distance > 20 and start not in country.roads:
            #print(str(start), 'is not connected to a road, queuing road')
            self.queueRoad(start, end)
            country.queueRoad(start, end)
            return 0
        if end not in self.roads and distance > 20 and country == 0:
            #print(str(end), 'is not connected to a road, queuing road')
            self.queueRoad(end, end.closestRoad)
            return 0
        elif end not in self.roads and distance > 20 and end not in country.roads:
            #print(str(end), 'is not connected to a road, queuing road')
            self.queueRoad(start, end)
            country.queueRoad(start, end)
            return 0
        if resource == 'food':
            if amount > start.foodStorage:
                #print('Amount requested greater than amount available:', str(amount), resource)
                return 0
            else:
                start.foodStorage -= amount
                end.foodStorage += amount
                return 1
        elif resource == 'water':
            if amount > start.water:
                #print('Amount requested greater than amount available:', str(amount), resource)
                return 0
            else:
                start.water -= amount
                end.water += amount
                return 1
        elif resource == 'ore':
            if amount > start.oreStorage:
                #print('Amount requested greater than amount available:', str(amount), resource)
                return 0
            else:
                start.oreStorage -= amount
                end.oreStorage += amount
                return 1
        elif resource == 'wealth':
            if amount > start.wealth:
                #print('Amount requested greater than amount available:', str(amount), resource)
                return 0
            else:
                start.wealth -= amount
                end.wealth += amount
                return 1
        elif resource == 'wood':
            if amount > start.woodStorage:
                #print('Amount requested greater than amount available:', str(amount), resource)
                return 0
            else:
                start.woodStorage -= amount
                end.woodStorage += amount
                return 1
        elif resource == 'population':
            if amount > start.population:
                #print('Amount requested greater than amount available:', str(amount), resource)
                return 0
            else:
                start.population -= amount
                end.population += amount
                return 1
        elif resource == 'energyStr':
            if amount > start.energyStr:
                #print('Amount requested greater than amount available:', str(amount), resource)
                return 0
            else:
                start.energyStr -= amount
                end.energyStr += amount
                return 1
        elif resource == 'airStr':
            if amount > start.airStr:
                #print('Amount requested greater than amount available:', str(amount), resource)
                return 0
            else:
                start.airStr -= amount
                end.airStr += amount
                return 1
        elif resource == 'waterStr':
            if amount > start.waterStr:
                #print('Amount requested greater than amount available:', str(amount), resource)
                return 0
            else:
                start.waterStr -= amount
                end.waterStr += amount
                return 1
        elif resource == 'landStr':
            if amount > start.landStr:
                #print('Amount requested greater than amount available:', str(amount), resource)
                return 0
            else:
                start.landStr -= amount
                end.landStr += amount
                return 1

    def buildMilitary(self):
        """Manages the construction of military resources"""
        world = self.world
        funding = self.wealth * .025
        if self.tech > 100:
            airfund = funding * .22
            landfund = funding * .3
            navalfund = funding * .234
            while (airfund > 10 * world.AIR_COST) or (landfund > 10 * world.ARMY_COST) or (navalfund > 10 * world.NAVY_COST):
                for c in self.cities:
                    if airfund > 10 * world.AIR_COST:
                        c.jobs.append('buildAirBase')
                        self.consQueue.append('buildAirBase')
                        airfund -= 10 * world.AIR_COST
                    if landfund > 10 * world.ARMY_COST:
                        c.jobs.append('buildBarracks')
                        self.consQueue.append('buildBarracks')
                        landfund -= 10 * world.ARMY_COST
                    if navalfund > 10 * world.NAVY_COST:
                        c.jobs.append('buildNavalBase')
                        self.consQueue.append('buildNavalBase')
                        navalfund -= 10 * world.NAVY_COST
        else:
            landfund = funding * .6
            navalfund = funding * .2
            while (landfund > 10 * world.ARMY_COST) or (navalfund > 10 * world.NAVY_COST):
                for c in self.cities:
                    if landfund > 10 * world.ARMY_COST:
                        c.jobs.append('buildBarracks')
                        self.consQueue.append('buildBarracks')
                        landfund -= 10 * world.ARMY_COST
                    if navalfund > 10 * world.NAVY_COST:
                        c.jobs.append('buildNavalBase')
                        self.consQueue.append('buildNavalBase')
                        navalfund -= 10 * world.NAVY_COST

    def queueRoad(self, start, end, path = 0):
        """Queues a road from a start point to an end point"""

        if path == 0:
            road = self.searchPath(start, end, False)
        else:
            road = path

        if road == None:
            return

        for t in road:
            t.jobs.append('buildRoad')
            self.consQueue.append('buildRoad')
            self.roads.add(t)

    def queueRoads(self):
        """Queues road construction jobs for the nation"""
        maxDistance = 1000
        
        for c in self.cities:

            for ci in self.cities:
                
                if ci not in c.connectedCities and ci != c:
                    path = self.searchPath(c, ci, False)     
                    current = path[0]
                    while('road' in current.improvements):
                        path.remove(current)
                        current = path[0]
                    self.queueRoad(current, ci, path)
                    c.connectedCities.append(ci)
                    ci.connectedCities.append(c)

    def upgradeRoad(self, road):
        """Upgrades an existing road"""
        for t in road:
            t.jobs.append('buildRoad')
            self.consQueue.append('buildRoad')

    def searchPath(self, start, end, water):

        def heuristic(start, end):
            distance = ((start.xCoor - end.xCoor)**2 + (start.yCoor - end.yCoor)**2)**.5
            return distance

        def tracePath(current):
             path = []
             while current.cameFrom:
                path.append(current)
                current = current.cameFrom
                path.append(current)
                return path[::-1]

        openset = set()
        closedset = set()
        current = start
        openset.add(current)

        fScoreTup = []

        start.gScore = 0
        start.fScore += heuristic(start, end)

        fScoreTup.append((start, start.fScore))

        while openset:
            #current = min(openset, key=lambda o:o.fScore)
            current = min(fScoreTup, key=itemgetter(1))[0]
            if current == end:
               return tracePath(current)
            openset.remove(current)
            fScoreTup.remove((current, current.fScore))
            closedset.add(current)

            for neighbor in current.neighbors.values():
                if neighbor.terrain == 4 and not water:
                    closedset.add(neighbor)
                if neighbor in closedset:
                    continue
                
                new_g = current.gScore + heuristic(current, neighbor) + neighbor.roughness * 10
                
                if neighbor not in openset or new_g < neighbor.gScore:
                    neighbor.cameFrom = current
                    neighbor.gScore = new_g
                    if neighbor in openset:
                        fScoreTup.remove((neighbor, neighbor.fScore))
                    neighbor.fScore = neighbor.gScore + heuristic(neighbor, end)
                    fScoreTup.append((neighbor, neighbor.fScore))


                    if neighbor not in openset:
                        openset.add(neighbor)
                       
                    
               
        return None

    def updateResources(self):
        """Updates the record of resources within a nation"""
        world = self.world
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

        self.foodDeficit = 0
        self.waterDeficit = 0
        self.woodDeficit = 0
        self.oreDeficit = 0
        self.wealthDeficit = 0

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

        for j in self.consQueue:

            if(j == 'buildFarm'):
                self.waterDeficit += 194250
                self.wealthDeficit += 2950 * world.FOOD_VAL
            elif(j == 'buildRoad'):
                self.oreDeficit += 7475
                self.wealthDeficit += 4000000
            elif(j == 'buildIrrigation'):
                self.wealthDeficit += 10000 * world.WATER_VAL
            elif(j == 'buildBarracks'):
                self.wealthDeficit += 10 * world.ARMY_COST
            elif(j == 'buildAirbase'):
                self.wealthDeficit += 10 * world.AIR_COST
            elif(j == 'buildNavalbase'):
                self.wealthDeficit += 10 * world.NAVY_COST
            elif(j == 'buildMarket'):
                self.woodDeficit += 100
                self.wealthDeficit += 100000
            elif(j == 'buildMine'):
                self.woodDeficit += 100
                self.wealthDeficit += 100000000
            elif(j == 'buildGrove'):
                self.waterDeficit += 330932
            elif(j == 'buildPowerplant'):
                self.oreDeficit += 3
                self.waterDeficit += 3
                self.woodDeficit += 5
            else:
                pass

            self.waterDeficit -= self.water
            self.oreDeficit -= self.oreStorage + self.ore
            self.woodDeficit -= self.woodStorage + self.wood
            self.wealthDeficit -= self.wealth

        if self.waterDeficit < 0:
            self.waterDeficit = 0
        if self.oreDeficit < 0:
            self.oreDeficit = 0
        if self.woodDeficit < 0:
            self.woodDeficit = 0
        if self.wealthDeficit < 0:
            self.wealthDeficit = 0

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
        #print('Commencing battle')
        airDist = 0
        navalDist = 0
        landDist = 0
        navalpath = []
        landpath = []
        navalEnd = 0
        if city.airStr > 0:
            airDist = ((city.xCoor - enemyCity.xCoor)**2 + (city.yCoor - enemyCity.yCoor)**2)**.5
        else:
            airDist = 99999999999
        if city.waterStr > 0:
            navalpath =  self.searchPath(city, enemyCity, True)
            if navalpath != None:
                navalDist = len(navalpath)
                navalEnd = navalpath[-1]
            else:
                navalDist = 99999999
        else:
            navalDist = 999999999
        if city.landStr > 0:
            landpath = self.searchPath(city, enemyCity, False)
            if landpath != None:
                landDist = len(landpath)
            else:
                landDist = 99999999
        else:
            landDist = 99999999

        if enemyCity not in landpath:
            landDist = 999999999
        if enemyCity not in navalpath:
            navalDist = 99999999

        airPhase = 0
        navalPhase = 0
        landPhase = 0

        if airDist <= city.airProj:
            #print('Beginning air phase')
            chance = city.airStr / (city.airStr + enemyCity.airStr + .001)
            while (city.airStr > 0 and enemyCity.airStr > 0):
                battle = random.random()
                if battle <= chance:
                    enemyCity.airStr -= 1
                else:
                    city.airStr -= 1

            airPhase = enemyCity.airStr - city.airStr
            #print('Air phase complete.  Result:', airPhase)

            navalPhase += airPhase
        if navalDist <= city.waterProj:
            #print('Beginning naval phase')
            chance = city.waterStr / (city.waterStr + enemyCity.waterStr + .001)
            while (city.waterStr > 0 and enemyCity.waterStr > 0):
                battle = random.random()
                if battle <= chance:
                    enemyCity.waterStr -= 1
                else:
                    city.waterStr -= 1

            navalPhase += enemyCity.waterStr - city.waterStr
            #print('Naval phase complete.  Result:', navalPhase)
            landPhase += navalPhase
        if landDist <= city.landProj:
            #print('Beginning land phase')
            chance = city.landStr / (city.landStr + enemyCity.landStr + .001)
            while (city.landStr > 0 and enemyCity.landStr > 0):
                battle = random.random()
                if battle <= chance:
                    enemyCity.landStr -= 1
                else:
                    city.landStr -= 1

            landPhase += enemyCity.landStr - city.landStr
            #print('Land phase complete.  Result:', landPhase)
            
            
        if landPhase < 0:
            #print(self.name, 'wins battle!  Claiming land for', self.name)
            if enemyCity.airStr < 0:
                enemyCity.airStr = 0
            if enemyCity.waterStr < 0:
                enemyCity.waterstr = 0
            if enemyCity.landStr < 0:
                enemyCity.landStr = 0

            self.claimTile(enemyCity)
            self.cities.append(enemyCity)

            for t in enemyCity.owner.tiles:
                if t.closestCity == enemyCity:
                    self.claimTile(t)

            if enemy.cities == []:
                print(enemy.name, 'has been destroyed by', self.name)
                self.enemies.remove(enemy)
                self.world.checkNation(enemy)

            return 1
        else:
            return 0

    def wageWar(self):
        """Wages a war against all enemies"""
        if self.enemies != []:
            print('Waging war for', self.name)

        for e in self.enemies:
            if e.cities == []:
                self.enemies.remove(e)
                e.enemies.remove(self)

        for e in self.enemies:
            for c in self.cities:
                if c.airStr + c.waterStr + c.landStr > 0:
                    #print(self.name, 'is launching an attack against the city', '(' + str(ec.xCoor) + ', ' + str(ec.yCoor) + ')')
                    if e.cities != []:
                        self.attackCity(c, e.cities[0])

    def gatherIntel(self, country):
        """Estimates military strength of target country as a function of distance"""
        if country.strength == 0:
            strength = 0
            self.neighbors[country] = (strength, self.world.year)
            return strength
        elif country not in self.neighbors.keys() or self.world.year - self.neighbors[country][1] > 2:
            startCity = self.cities[0]
            endCity = country.cities[0]
            p = self.searchPath(startCity, endCity, False)
            distance = 0
            strength = 0
            if p == None:
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
            self.neighbors[country] = (strength, self.world.year)
            return strength
        else:
            strength = self.neighbors[country][0]
            return strength

    def calcWarOdds(self, eStrength):
        """Calculates odds of winning a war against target country"""
        odds = self.strength / (self.strength + eStrength + .0001)
        return odds

    def calcWarCost(self, eStrength):
        """Calculates the cost of a war between two countries"""
        world = self.world
        aCOR = (world.AIR_COST + world.ARMY_COST + world.NAVY_COST / 3.0) #Average cost of replacement
        aCost = eStrength * 2 * aCOR
        bCost = self.strength * 2 * aCOR

        if aCost > self.strength * 2 * aCOR:
            aCost = self.strength * 2 * aCOR
        if bCost > eStrength * 2 * aCOR:
            bCost = eStrength * 2 * aCOR

        return (aCost, bCost)

    def trade(self):
        """Examines deficits and attempts to trade with other nations, going to war for the resources if necessary"""
        if self.world.year < 2 or self.cities == []:
            return
        else:
            pass
        
        neighbors = []
        for n in self.world.nations:
            if n != self and n.cities != [] and self.cities != [] and n not in self.enemies:
                start = self.cities[0]
                end = n.cities[0]
                distance = ((start.xCoor - end.xCoor)**2 + (start.yCoor - end.yCoor)**2)**.5
                neighbors.append((n, distance))
                
        neighbors = sorted(neighbors, key=itemgetter(1))
        closeNations = [x[0] for x in neighbors]
        neighbors = closeNations

        if self.foodDeficit > 0:
            for n in neighbors:
                if n.foodStorage >= self.foodDeficit:
                    self.bargain(n, 'food')
                    break
        if self.waterDeficit > 0:
            for n in neighbors:
                if n.water >= self.waterDeficit:
                    self.bargain(n, 'water')
                    break
        if self.woodDeficit > 0:
            for n in neighbors:
                if n.woodStorage >= self.woodDeficit:
                    self.bargain(n, 'wood')
                    break
        if self.oreDeficit > 0:
            for n in neighbors:
                if n.oreStorage >= self.oreDeficit:
                    self.bargain(n, 'ore')
                    break
        if self.wealthDeficit > 0:
            for n in neighbors:
                if n.wealth >= self.wealth:
                    self.bargain(n, 'wealth')
                    break

        self.readOffers()

    def bargain(self, country, resource):
        """Calculates an acceptable offer for the desired resource"""
        #print(self.name, 'is bargaining with', country.name, 'for', resource)
        world = self.world
        #print(self.name, 'is gathering intel on', country.name)
        eStrength = self.gatherIntel(country)
        #print('Collection complete')
        odds = self.calcWarOdds(eStrength)
        
        costs = self.calcWarCost(eStrength)
        ourCost = costs[0]
        for e in self.enemies:
            ourCost += self.calcWarCost(e.strength)[0]
        theirCost = costs[1]
        value = 0

        if resource == 'wood':
            value = country.woodStorage * world.WOOD_VAL
        elif resource == 'water':
            value = country.water * world.WATER_VAL
        elif resource == 'food':
            value = country.food * world.FOOD_VAL
        elif resource == 'ore':
            value = country.oreStorage * world.ORE_VAL
        elif resource == 'wealth':
            value = country.wealth

        middleVal = odds * value
        upperBound = middleVal + theirCost
        lowerBound = middleVal - ourCost

        offer = upperBound

        self.sendOffer(offer = offer, resource = resource, country = country, status = 0)
        #print('Offer sent to', country.name)

    def sendOffer(self, offer = 0, resource = 0, country = 0, status = 0, prevOffer = 0):
        """Sends an offer for the set price for the desired resource to another country"""
        if country == 0:
            #print('No recipient for offer')
            return
        
        if prevOffer == 0:
            message = (offer, resource, self, status)
            country.offers.append(message)
            if status == 0:
                self.pendingOffers.append(message)
        else:
            message = []
            message.append(offer)
            message.append(prevOffer[1])
            message.append(prevOffer[2])
            message.append(status)
            message.append(self)
            country.offers.append(message)
            if status == 0:
                self.pendingOffers.append(message)
                country.pendingOffers.remove(prevOffer)

    def readOffers(self):
        """Reads incoming offers and accepts, modifies, or rejects them"""
        world = self.world
        deletedOffers = []

        for o in self.offers:
            
            status = o[3]
            country = o[2]
            resource = o[1]
            offer = o[0]
            sender = 0


            if len(o) > 4:
                sender = o[4]

            if status == 1:
                #Transfer the resources
                transferred = 0
                if resource == 'wood':
                    offer = offer / world.WOOD_VAL
                elif resource == 'ore':
                    offer = offer / world.ORE_VAL
                elif resource == 'water':
                    offer = offer / world.WATER_VAL
                elif resource == 'food':
                    offer = offer / world.FOOD_VAL
                count = 0
                while (transferred < offer and count < len(country.tiles)):
                    currentTile = country.tiles[count]
                    if resource == 'wood':
                        transferred += currentTile.woodStorage
                        if transferred > offer:
                            diff = transferred - offer
                            self.cities[0].woodStorage += diff
                            currentTile.woodStorage -= diff
                            count += 1
                        else:
                            self.cities[0].woodStorage += currentTile.woodStorage
                            currentTile.woodStorage = 0
                            count += 1
                    elif resource == 'water':
                        transferred += currentTile.water
                        if transferred > offer:
                            diff = transferred - offer
                            self.cities[0].water += diff
                            currentTile.water -= diff
                            count += 1
                        else:
                            self.cities[0].water += currentTile.water
                            currentTile.water = 0
                            count += 1
                    elif resource == 'food':
                        transferred += currentTile.foodStorage
                        if transferred > offer:
                            diff = transferred - offer
                            self.cities[0].foodStorage += diff
                            currentTile.foodStorage -= diff
                            count += 1
                        else:
                            self.cities[0].foodStorage += currentTile.foodStorage
                            currentTile.foodStorage = 0
                            count += 1
                    elif resource == 'ore':
                        transferred += currentTile.oreStorage
                        if transferred > offer:
                            diff = transferred - offer
                            self.cities[0].oreStorage += diff
                            currentTile.oreStorage -= diff
                            count += 1
                        else:
                            self.cities[0].oreStorage += currentTile.oreStorage
                            currentTile.oreStorage = 0
                            count += 1
                    elif resource == 'wealth':
                        transferred += currentTile.wealth
                        if transferred > offer:
                            diff = transferred - offer
                            self.cities[0].wealth += diff
                            currentTile.wealth -= diff
                            count += 1
                        else:
                            self.cities[0].wealth += currentTile.wealth
                            currentTile.wealth = 0
                            count += 1

                deletedOffers.append(o)
                #country.pendingOffers.remove(o)
                
            elif status == 0:
                #Evaluate the new offer
                eStrength = self.gatherIntel(country)
                odds = self.calcWarOdds(eStrength)
                costs = self.calcWarCost(eStrength)
                ourCost = costs[0]
                for e in self.enemies:
                    ourCost += self.calcWarCost(e.strength)[0]
                theirCost = costs[1]
                value = 0

                if resource == 'wood':
                    value = self.woodStorage * world.WOOD_VAL
                elif resource == 'water':
                    value = self.water * world.WATER_VAL
                elif resource == 'food':
                    value = self.foodStorage * world.FOOD_VAL
                elif resource == 'ore':
                    value = self.oreStorage * world.ORE_VAL
                elif resource == 'wealth':
                    value = self.wealth

                middleVal = odds * value
                upperBound = middleVal + theirCost
                lowerBound = middleVal - ourCost

                if offer <= upperBound:
                    #Accept the offer
                    #print('Deal accepted between', self.name, 'and', country.name)
                    status = 1
                    self.sendOffer(offer = offer, resource = resource, country = country, status = status, prevOffer = o)
                    deletedOffers.append(o)
                elif offer < upperBound + upperBound* .1 :
                    #Attempt to modify the offer
                    print(self.name, 'thinks that', country.name, 'has not offered a fair deal and is risking war to modify it')
                    status = 0
                    offer = upperBound
                    self.sendOffer(offer = offer, resource = resource, country = country, status = status, prevOffer = o)
                    deletedOffers.append(o)
                else:
                    #Reject the offer
                    status = -1
                    self.sendOffer(offer = offer, resource = resource, country = sender, status = status, prevOffer = o)
                    deletedOffers.append(o)
                
            elif status == -1:
                #Offer was rejected, declare war
                print('War declared between', self.name, 'and', sender.name)
                deletedOffers.append(o)
                self.enemies.append(sender)
                sender.enemies.append(self)
                

        for o in deletedOffers:
            self.offers.remove(o)             

    def updateReadout(self):
        """Updates the readout of a nation"""

        self.readout = '\n'

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
        self.readout += 'Water Deficit: ' + str(self.waterDeficit) + '\r\n'
        self.readout += 'Food Deficit: ' + str(self.foodDeficit) + '\r\n'
        self.readout += 'Wood Deficit: ' + str(self.woodDeficit) + '\r\n'
        self.readout += 'Ore Deficit: ' + str(self.oreDeficit) + '\r\n'

