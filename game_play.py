from board import board
import random

# player 1 - ratmen and forest
# 12 player pieces, +1 for every forest region occupied

# player 2 - trolls and pillaging
# 10 player pieces, +1 for every non-empty region conquered. +1 defense for every region occupied

class game_play:
    
    def __init__(self, board):
        self.game_board = board
        self.Ratmen = player(12, 'forest_power', 'lots_of_people', 'ratmen', self.game_board)
        self.Trolls = player(10, 'one_extra_defense', 'one_coin_non_empty', 'trolls', self.game_board)
        self.Ratmen.opponent = self.Trolls
        self.Trolls.opponent = self.Ratmen

        # self.rat_spaces_occupied = []
        # self.troll_spaces_occupied = []

    # first move for both the players
    def start_game(self):
        number = random.randint(0, 1)
        # self.whose_turn = None
        self.whose_turn = self.Trolls
        # Ratmen first
        # if number == 0:
        #     self.whose_turn = self.Ratmen
        # else:
        #     self.whose_turn = self.Trolls  
        # return self.whose_turn.name

    # just get the coins earned from one step of a turn
    def reward_1step(self, piece):
        coin = 1
        player = self.whose_turn
        if player.name == 'ratmen':
            # you get one extra coin this turn if its a forest, but you get +1 for every turn that 
            # you still have this forest, so +2 is an estimate
            if piece.terrain == 'forest':
                coin += 2
            if piece.numTrolls > 0:
                coin += 1
            elif piece.declineTroll is True:
                coin += 1
        # for trolls if you take a rat or decline rat, you get +1 from your special power, 
        # and also +1 for taking 1 coin away from your opponent
        else:
            if piece.numRats > 0:
                coin += 2
            elif piece.declineRat is True:
                coin += 2
            elif piece.lostTribe is True:
                coin += 1
        return coin

        
    # make one move within a turn (a turn consists of multiple moves)
    # space is string representation of piece such as 'p3' 
    # possible_spaces for first move = [1, 2, 3, 4, 5, 6, 11, 12, 16, 17, 18, 19, 20, 21, 22, 23]
    def take_turn(self, space, firstTurn):
        opponent = self.whose_turn.opponent
        player = self.whose_turn
        piece = self.game_board.get_piece(space)
        legal = False
        if firstTurn: 
            legal = player.one_move(space, True)
        else:
            legal = player.one_move(space, False)
        if legal:
            reward = self.reward_1step(piece)
            pieces_required = piece.pieces_required()
            if player.name == 'ratmen':
                reward = reward * (10 / pieces_required)
            else:
                reward = reward * (12 / pieces_required)
            player.spaces_occupied.append(piece)
            num_opponent = piece.get_raceCount(opponent.name)
            self.take_turn_helper(piece, num_opponent)  
            return reward     
        else:
            return 'not a move'

    def take_turn_helper(self, piece, num_opponent):
        player = self.whose_turn
        opponent = self.whose_turn.opponent
        pieces_required = piece.pieces_required()
        # If this player is attacking an opponent, the piece is updated to no longer store the opponent
        # The player class for the opponent is updated so that they no longer occupy that space 
        # 1 is subtracted from the number of pieces this player has
        if num_opponent > 0:
            piece.update_numPieces(0, opponent.name)
            opponent.spaces_occupied.remove(piece)
            opponent.num_pieces -= 1
            # trolls have an extra defense so 1 more piece is required
            if player.name == 'ratmen':
                pieces_required += 1
            # trolls special power is extra coin for attacking non-empty regions
            else:
                player.coins_1turn += 1
        # Does this spot have the opponents decline race in it. If it does, remove the decline piece
        # from both the board and from the opponents decline_spaces
        if piece.get_decline(opponent.name):
            piece.remove_decline(opponent.name)
            opponent.decline_spaces.remove(piece)
            # trolls have extra defense even in decline
            if player.name == 'ratmen':
                pieces_required += 1
            # +1 coin for non-empty
            else:
                player.coins_1turn += 1
        player.pieces_left -= (pieces_required)
        piece.update_numPieces(pieces_required, player.name)
        if piece.lostTribe:
            piece.lostTribe = False
            if player.name == 'trolls':
                player.coins_1turn += 1

    # it's the next players turn
    def change_turns(self):
        if self.whose_turn.name == 'ratmen':
            self.whose_turn = self.Trolls
            self.whose_turn.coins_1turn = 0
        else:
            self.whose_turn = self.Ratmen
            self.whose_turn.coins_1turn = 0

    def decline(self):
        player = self.whose_turn
        # remove any remaining declined pieces from the board
        player.decline_spaces = []
        for piece in player.spaces_occupied:
            if player.name == 'ratmen':
                piece.declineRat = True
                piece.numRats = 0
            else:
                piece.declineTroll = True
                piece.numTrolls = 0
            player.decline_spaces.append(piece)
        player.spaces_occupied = []
        player.num_pieces = 0

    # the turn after decline
    def after_decline(self):
        player = self.whose_turn
        if player.name == 'ratmen':
            player.num_pieces = 12
            player.pieces_left = 12
        else:
            player.num_pieces = 10
            player.pieces_left = 10

    # At the start of a players turn, one of their pieces is left behind in each area 
    def start_of_turn(self):
        player = self.whose_turn
        spaces_occupied = player.spaces_occupied
        # how many pieces the player has to play with
        free_pieces = player.num_pieces - len(spaces_occupied)
        for piece in spaces_occupied: 
            piece.update_numPieces(1, player.name)
        player.pieces_left = free_pieces
        return free_pieces

    # At the end of a players turn, distribute all the pieces evenly
    def distribute_endturn(self):
        player = self.whose_turn
        # leave at least this many pieces in each of the players spaces occupied
        if len(player.spaces_occupied) == 0:
            return
        piece_perspot = player.num_pieces // len(player.spaces_occupied)
        for piece in player.spaces_occupied:
            piece.update_numPieces(piece_perspot, player.name)
        remaining_pieces = player.num_pieces % len(player.spaces_occupied)
        # distribute the remaining pieces randomly (evenly as possible)
        for i in range(remaining_pieces):
            player.spaces_occupied[i].update_numPieces(piece_perspot + 1, player.name)
        player.pieces_left = 0

    # call this method and not the field player.coins_1turn
    def coins_earned(self):
        player = self.whose_turn
        player.coins_1turn += len(player.spaces_occupied) + len(player.decline_spaces)
        if player.name == 'ratmen':
            for piece in player.spaces_occupied:
                if piece.terrain == 'forest':
                    player.coins_1turn += 1
        print(player.name + ' recieved ' + str(player.coins_1turn) + ' coins this turn\n')
        return player.coins_1turn

    # print for whose turn it is, what board pieces have their people and how many 
    def print_game(self):
        player = self.whose_turn
        message = ''
        if player.name == 'ratmen':
            message += 'It is the ' + player.name + '\'s turn\n'
            message += 'They have ' + str(player.num_pieces) + ' pieces total\n'
            for piece in player.spaces_occupied:
                message += piece.name + ' has ' + str(piece.numRats) + ' ratmen on it\n'
            for piece in player.decline_spaces:
                message += piece.name + ' has a ratman in decline on it\n'
        else:
            message += 'It is the ' + player.name + ' turn\n'
            message += 'They have ' + str(player.num_pieces) + ' pieces total\n'
            for piece in player.spaces_occupied:
                message += piece.name + ' has ' + str(piece.numTrolls) + ' trolls on it\n'
            for piece in player.decline_spaces:
                message += piece.name + ' has a troll in decline on it\n'
        message += 'They have ' + str(player.pieces_left) + ' pieces left to play with\n'  
        print(message)



class player:
    def __init__(self, num_pieces, race_power, special_power, name, board):
        self.num_pieces = num_pieces
        self.race_power = race_power
        self.special_power = special_power
        self.name = name
        self.pieces_left = num_pieces
        self.opponent = None
        self.spaces_occupied = []
        self.decline_spaces = []
        self.game_board = board
        self.coins_1turn = 0


    # possible_spaces for first move = [1, 2, 3, 4, 5, 6, 11, 12, 16, 17, 18, 19, 20, 21, 22, 23]
    # space is a string, 'p3' for example
    def one_move(self, space, firstmove):
        bool1 = self.is_a_move(space)
        bool2 = self.enough_pieces(space)
        boolean = False
        if firstmove:
            boolean = bool2
        else:
            boolean = bool1 and bool2
        return boolean
            
    # player can only go into neighboring spaces, returns true if a neighboring space
    def is_a_move(self, space):
        piece = self.game_board.get_piece(space)
        possible_spaces = set()
        for p in self.spaces_occupied:
            for neighbor in p.neighbors:
                if neighbor not in self.spaces_occupied:
                    possible_spaces.add(neighbor)
        return piece in possible_spaces

    # checks if a players turn is over
    def moves_left(self):
        possible_spaces = set()
        for p in self.spaces_occupied:
            for neighbor in p.neighbors:
                if neighbor not in self.spaces_occupied:
                    possible_spaces.add(neighbor)
        for piece in possible_spaces:
            if piece.pieces_required() <= self.pieces_left:
                return True
        return False

    # list of spaces a player can move into 
    # firstmove - whether its the first move ever or a player is coming back from decline
    def possible_spaces(self, firstmove):
        # first moves are [p1, p2, p3, p4, p5, p6, p11, p12, p16, p17, p18, p19, p20, p21, p22, p23]
        if firstmove: 
            return [0, 1, 2, 3, 4, 5, 10, 11, 15, 16, 17, 18, 19, 20, 21, 22]
        possible_spaces = set()
        for p in self.spaces_occupied:
            for neighbor in p.neighbors:
                if neighbor not in self.spaces_occupied:
                    possible_spaces.add(neighbor)
        indexes = []
        for piece in possible_spaces:
            name = piece.name
            name = int(name[1:])
            indexes.append(name - 1)
        return indexes

    # player must have enough pieces left, returns true if so
    def enough_pieces(self, space):
        piece = self.game_board.get_piece(space)
        pieces_required = piece.pieces_required()
        return pieces_required <= self.pieces_left 
            





        

        
