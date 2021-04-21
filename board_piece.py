class piece:
    # terrain types - farm, hill, forest, mountain, swamp, sea
    # edge - whether the space is on the edge of the board and a player can enter through it
    # lostTribe - whether a space has the indigenous race on it, boolean
    # symbolType - underworld, magic source, mining
    # numPieces - how many pieces on this space
    def __init__(self, terrain, edge, lostTribe, symbolType, neighbors = []):
        self.terrain = terrain
        self.edge = edge
        self.lostTribe = lostTribe
        self.symbolType = symbolType
        self.neighbors = neighbors 
        self.numRats = 0
        self.numTrolls = 0
        self.declineRat = False
        self.declineTroll = False

    # After a player makes a move on their turn, how many pieces of a race are on that space
    def update_numPieces(self, num, race):
        if race == 'ratmen':
            self.numRats = num
        else:
            self.numTrolls = num

    # The number of pieces needed to conquer this region
    # Number pieces needed is a base of 2 + 1 addition for mountains or lostTribes + 1 additional for each
        # opponent on the space
    def pieces_required(self):
        count = 0
        if self.terrain == 'mountain':
            count += 1
        if self.lostTribe == True:
            count += 1
        count += self.numRats
        count += self.numTrolls
        return count + 2

    def get_raceCount(self, race):
        if race == 'ratmen':
            return self.numRats
        else:
            return self.numTrolls

    # All the pieces in this space go into decline 
    def decline_space(self, race):
        if race == 'ratmen':
            self.numRats = 0
            self.declineRat = True
        else:
            self.numTrolls = 0
            self.declineTroll = True

    # takes in name - 'ratmen' or 'trolls' and returns a boolean of if their declined race 
    # occupies that spot
    def get_decline(self, name):
        if name == 'ratmen':
            return self.declineRat
        else:
            return self.declineTroll

    def remove_decline(self, name):
        if name == 'ratmen':
            self.declineRat = False
        else:
            self.declineTroll = False

    


    
