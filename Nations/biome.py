class biome():
    """Large section of tiles sharing similar geographical features"""

    def __init__(self,
                 center=(0, 0),
                 type=-1,
                 tiles={},
                 size=100,
                 neighbors=[]):
        self.center = center
        self.type = type
        self.tiles = tiles
        self.size = size
        self.neighbors = neighbors

