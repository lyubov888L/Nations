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
                 consQueue = []):

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
    
                
    def claimTile(self, t):
        if t in self.tiles:
            print('Tried to claim tile that already belongs to owner')
        else:
            t.owner = self
            self.tiles.append(t)

    def findCities(self):
        for t in self.tiles:
            if t.population > self.population / 30:
                self.cities.append(t)

    def queueRoad(self, start, end):
        road = chartPath(start, end)
        for t in road:
            t.jobs.append('buildRoad')
        self.roads.append(road)
        return 0

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
                        break
                    else:
                        distance = abs(c.xCoor - ci.xCoor) + abs(c.yCoor - ci.yCoor)
                        Q.put((distance, ci))

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
        while(end not in Q):
            for neighbor in t.neighbors:
                if neighbor in visited:
                    pass
                else:
                    if neighbor == end:
                        path.append(neighbor)
                    elif neighbor.terrain == 4:
                        visited.append(neighbor)
                    distance = abs(neighbor.xCoord - end.xCoord) + abs(neighbor.yCoord - end.yCoord) + (neighbor.roughness * 10)
                    Q.put((distance, neighbor))
                    visited.append(t)
            path.append(t)            
            t = Q.get()
        return path

    def updateReadout(self):
        self.readout += 'Name: ' + str(self.name) + '\r\n'
        self.readout += 'Population: ' + str(self.population) + '\r\n'
        self.readout += 'Color: ' + str(self.food) + '\r\n'
        self.readout += 'Wealth: ' + str(self.wealth) + '\r\n'
        self.readout += 'Energy Strength: ' + str(self.energyStr) + '\r\n'
        self.readout += 'Infrastructure: ' + str(self.infra) + '\r\n'
        self.readout += 'Ore: ' + str(self.ore) + '\r\n'
        self.readout += 'Water: ' + str(self.water) + '\r\n'
        self.readout += 'Wood: ' + str(self.wood) + '\r\n'
        self.readout += 'Land Strength: ' + str(self.landStr) + '\r\n'
        self.readout += 'Air Strength: ' + str(self.airStr) + '\r\n'
        self.readout += 'Water Strength: ' + str(self.waterStr) + '\r\n'
        self.readout += 'Nationality: ' + str(self.nationality) + '\r\n'
        self.readout += 'Economy Strength: ' + str(self.econStr) + '\r\n'
        self.readout += 'Tiles: ' + str(self.tiles) + '\r\n'
        self.readout += 'Cities: ' + str(self.cities) + '\r\n'
        self.readout += 'Roads: ' + str(self.roads) + '\r\n'
        self.readout += 'Borders: ' + str(self.borders) + '\r\n'
        self.readout += 'World: ' + str(self.world) + '\r\n'
        self.readout += 'Construction Queue: ' + str(self.consQueue) + '\r\n'
        self.readout += 'Tile Count: ' + str(len(self.tiles)) + '\r\n'