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
                 biome = -1):

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

    #def updateAttrib(self, name, val):
    #    try:
    #        eval('self.' + name + ' = ' + val)
    #    except:
    #        print('Invalid name or value given')
    #        print('Name: ' + name)
    #        print('Value: ' + val)

    def calcTileColor(self):
        """Updates the color of the tile"""
        red = 0
        green = 0
        blue = 0
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
        self.color = pygame.Color(red, green, blue)