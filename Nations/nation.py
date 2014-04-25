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
                 roads = []):

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
         
    def scanResources(self):
        for tile in self.tiles:
            self.population += tile.population
            self.food += tile.food
            self.wealth += tile.wealth
            self.energyStr += tile.energyStr
            self.infra += tile.infra
            self.ore += tile.ore
            self.water += tile.water
            self.wood += tile.wood
            self.landStr += tile.landStr
            self.airStr += tile.airStr
            self.waterStr += tile.waterStr
            self.econStr += tile.econStr

