

class piece:
    # terrain types - farm, hill, forest, mountain, swamp, sea
    # edge - whether the space is on the edge of the board and a player can enter through it
    # lostTribe - whether a space has the indigenous race on it, boolean
    # symbolType - underworld, magic source, mining
    def __init__(self, terrain, edge, lostTribe, symbolType, neighbors = []):
        self.terrain = terrain
        self.edge = edge
        self.lostTribe = lostTribe
        self.symbolType = symbolType
        self.neighbors = neighbors 
