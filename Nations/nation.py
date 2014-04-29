import random

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
                 readout = ''):

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
    
                
    def claimTile(self, t):
        t.owner = self
        self.tiles.append(t)

    def updateReadout(self):
        self.readout += 'Name: ' + str(self.name) + '\r\n'
        self.readout += 'Population: ' + str(self.population) + '\r\n'
        self.readout += 'Food: ' + str(self.food) + '\r\n'
