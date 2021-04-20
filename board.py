from board_piece import piece

# terrain types - farm, hill, forest, mountain, swamp, sea
    # edge - whether the space is on the edge of the board and a player can enter through it
    # lostTribe - whether a space has the indigenous race on it, boolean
    # symbolType - underworld, magic source, mining
class board:
    def __init__(self):
        #  terrain, edge, lostTribe, symbolType, neighbors
        
        # make this an array instead 
        # but if you keep it this way, theres a magic method in a class __
        p1 = piece('sea', True, False, None)
        p2 = piece('farm', True, False, ['magic_source'])
        p3 = piece('forest', True, False, ['mining'])
        p4 = piece('swamp', True, True, ['underworld'])
        p5 = piece('hill', True, False, None)
        p6 = piece('mountain', True, False, ['mining', 'underworld'])
        p7 = piece('hill', False, True, None)
        p8 = piece('sea', False, False, None)
        p9 = piece('mountain', False, False, None)
        p10 = piece('farm', False, False, None)
        p11 = piece('forest', True, True, ['magic_source'])
        p12 = piece('farm', True, True, None)
        p13 = piece('forest', False, True, None)
        p14 = piece('farm', False, True, ['magic_source'])
        p15 = piece('hill', False, True, ['underworld'])
        p16 = piece('mountain', True, False, ['mining'])
        p17 = piece('swamp', True, True, ['magic_source'])
        p18 = piece('hill', True, False, ['underworld'])
        p19 = piece('swamp', True, True, ['mining'])
        p20 = piece('mountain', True, False, None)
        p21 = piece('swamp', True, False, None)
        p22 = piece('forest', True, False, None)
        p23 = piece('sea', True, False, None)

        p1.neighbors = [p2, p6]
        p2.neighbors = [p1, p3, p6, p7]
        p3.neighbors = [p2, p4, p7, p8, p9]
        p4.neighbors = [p3, p5, p9, p10]
        p5.neighbors = [p4, p10, p11]
        p6.neighbors = [p1, p2, p7, p12]
        p7.neighbors = [p2, p3, p6, p8, p12, p13]
        p8.neighbors = [p3, p7, p9, p13, p14]
        p9.neighbors = [p3, p4, p8, p10, p14, p15]
        p10.neighbors = [p4, p5, p9, p11, p15]
        p11.neighbors  = [p5, p10, p15, p16]
        p12.neighbors = [p6, p7, p13, p17, p18]
        p13.neighbors = [p7, p8, p12, p14, p18, p19]
        p14.neighbors = [p8, p9, p13, p15, p19, p20, p21]
        p15.neighbors = [p9, p10, p11, p14, p16, p21, p22]
        p16.neighbors = [p11, p15, p22, p23]
        p17.neighbors = [p12, p18]
        p18.neighbors = [p12, p13, p17, p19]
        p19.neighbors = [p13, p14, p18, p20]
        p20.neighbors = [p14, p19, p21]
        p21.neighbors = [p14, p15, p20, p22, p23]
        p22.neighbors = [p15, p16, p21, p23]
        p23.neighbors = [p16, p21, p22]

        self.array = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, 
        p18, p19, p20, p21, p22, p23]

    def get_piece(self, index):
        return self.array[index]





