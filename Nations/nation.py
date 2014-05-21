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
                 woodStorage = 0):

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
    
                
    def claimTile(self, t):
        if t not in self.tiles:
            if t.owner != self and t.owner != None:
                t.owner.tiles.remove(t)
            t.owner = self
            self.tiles.append(t)

    def findCities(self):
        for t in self.tiles:
            if (t.population > self.population / 30) and (t not in self.cities):
                self.cities.append(t)

    def queueRoad(self, start, end):
        road = self.chartPath(start, end)
        for t in road:
            t.jobs.append('buildRoad')
        self.roads.append(road)

    def queueRoads(self):
        
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
                        tiebreaker = int(random.random() * 100000000)
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
        while(end[2] not in path):
            for neighbor in t.neighbors.values():
                if neighbor in visited:
                    pass
                else:
                    if neighbor == end[2]:
                        path.append(neighbor)
                    elif neighbor.terrain == 4:
                        visited.append(neighbor)
                    print(end[2])
                    distance = abs(neighbor.xCoor - end[2].xCoor) + abs(neighbor.yCoor - end[2].yCoor) + (neighbor.roughness * 10)
                    tiebreaker = int(random.random() * 100000000)
                    Q.put((distance, tiebreaker, neighbor))
                    visited.append(t)
            path.append(t)            
            t = Q.get()
            if len(t) > 1:
                t = t[2]
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
            self.wealth += t.wealth
            self.energyStr += t.energyStr
            self.infra += t.infra
            self.ore += t.ore
            self.water += t.water
            self.wood += t.wood
            self.landStr += t.landStr
            self.airStr += t.airStr
            self.waterStr += t.waterStr
            self.econStr += t.econStr
            t.wealth = (t.food + t.water + 2 * t.wood + 4 * t.ore + t.foodStorage) * t.infra / (t.population + 1)
            self.wealth += t.wealth
            t.foodStorage += t.food - t.population
            self.foodStorage += t.foodStorage
            t.oreStorage += t.ore
            self.oreStorage += t.oreStorage
            t.woodStorage += t.wood
            self.woodStorage += t.woodStorage
            if t.foodStorage > 0:
                t.population += int(1 * t.wealth)


    def updateReadout(self):
        self.readout += 'Name: ' + str(self.name) + '\r\n'
        self.readout += 'Population: ' + str(self.population) + '\r\n'
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
        self.readout += 'Cities: ' + str(self.cities) + '\r\n'
        self.readout += 'Roads: ' + str(self.roads) + '\r\n'
        self.readout += 'Borders: ' + str(len(self.borders)) + '\r\n'
        self.readout += 'World: ' + str(self.world) + '\r\n'
        self.readout += 'Construction Queue: ' + str(self.consQueue) + '\r\n'
