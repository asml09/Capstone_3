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

    # make one move within a turn (a turn consists of multiple moves)
    # space is string representation of piece such as 'p3' 
    # possible_spaces for first move = [1, 2, 3, 4, 5, 6, 11, 12, 16, 17, 18, 19, 20, 21, 22, 23]
    def take_turn(self, space, firstTurn):
        player = self.whose_turn
        opponent = self.whose_turn.opponent
        piece = self.game_board.get_piece(space)
        legal = False
        if firstTurn: 
            legal = self.whose_turn.one_move(space, True)
        else:
            legal = self.whose_turn.one_move(space, False)
        if legal:
            player.spaces_occupied.append(piece)
            num_opponent = piece.get_raceCount(opponent.name)
            # If this player is attacking an opponent, the piece is updated to no longer store the opponent
            # The player class for the opponent is updated so that they no longer occupy that space 
            # 1 is subtracted from the number of pieces this player has
            if num_opponent > 0:
                piece.update_numPieces(0, opponent.name)
                opponent.spaces_occupied.remove(piece)
                opponent.num_pieces -= 1
            # Does this spot have the opponents decline race in it. If it does, remove the decline piece
            # from both the board and from the opponents decline_spaces
            if piece.get_decline(opponent.name):
                piece.remove_decline(opponent.name)
                opponent.decline_spaces.remove(piece)
            return player.pieces_left
        else:
            print('not a move')

    # def one_move(self, space):
    #     self.pieces_left = self.num_pieces
    #     boolean = self.is_a_move(space)
    #     piece = game_board.get_piece(space)
    #     pieces_required = piece.pieces_required()
    #     if boolean:
    #         self.pieces_left -= pieces_required
    #         piece.update_numPieces(pieces_required, self.name)
    #         if piece.lostTribe == True:
    #             piece.lostTribe = False

    # it's the next players turn
    def change_turns(self):
        if self.whose_turn.name == 'ratmen':
            self.whose_turn = self.Trolls
        else:
            self.whose_turn = self.Ratmen

    def decline(self):
        player = self.whose_turn
        # remove any remaining declined pieces from the board
        player.decline_spaces = []
        pieces_declined = player.spaces_occupied
        # if self.whose_turn == self.Ratmen:
        #     pieces_declined = self.rat_spaces_occupied
        # else:
        #     pieces_declined = self.troll_spaces_occupied
        for piece in pieces_declined:
            piece.decline_space(player.name)
            player.decline_spaces.append(piece)
            player.spaces_occupied.remove(piece)
        player.num_pieces = 0

    # the turn after decline
    def after_decline(self):
        player = self.whose_turn
        if player.name == 'ratmen':
            player.num_pieces = 12
        else:
            player.num_pieces = 10

    # At the start of a players turn, one of their pieces is left behind in each area 
    def start_of_turn(self):
        player = self.whose_turn
        spaces_occupied = player.spaces_occupied
        # how many pieces the player has to play with
        free_pieces = player.num_pieces - len(spaces_occupied)
        for piece in spaces_occupied: 
            piece.update_numPieces(1, player.name)
        return free_pieces

    # At the end of a players turn, distribute all the pieces evenly
    def distribute_endturn(self):
        player = self.whose_turn
        # leave at least this many pieces in each of the players spaces occupied
        piece_perspot = player.num_pieces / len(player.spaces_occupied)
        for piece in player.spaces_occupied:
            piece.update_numPieces(piece_perspot, player.name)
        remaining_pieces = player.num_pieces % len(player.spaces_occupied)
        # distribute the remaining pieces randomly (evenly as possible)
        for i in len(remaining_pieces):
            player.spaces_occupied[i].update_numPieces(piece_perspot + 1, player.name)

    # print for whose turn it is, what board pieces have their people and how many 
    def print_game(self):
        player = self.whose_turn
        message = ''
        if player.name == 'ratmen':
            message += 'It is the ' + player.name + '\'s turn\n'
            message += 'They have ' + str(player.num_pieces) + ' pieces\n'
            for piece in player.spaces_occupied:
                message += piece.name + ' has ' + str(piece.numRats) + ' ratmen on it\n'
            for piece in player.decline_spaces:
                message += piece.name + 'has a ratman in decline on it\n'
        else:
            message += 'It is the ' + player.name + ' turn\n'
            message += 'They have ' + str(player.num_pieces) + ' pieces\n'
            for piece in player.spaces_occupied:
                message += piece.name + ' has ' + str(piece.numTrolls) + ' trolls on it\n'
            for piece in player.decline_spaces:
                message += piece.name + 'has a troll in decline on it\n'
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


    # possible_spaces for first move = [1, 2, 3, 4, 5, 6, 11, 12, 16, 17, 18, 19, 20, 21, 22, 23]
    # space is a number - 3 would represent p3
    def one_move(self, space, firstmove):
        bool1 = self.is_a_move(space)
        bool2 = self.enough_pieces(space)
        piece = self.game_board.get_piece(space)
        pieces_required = piece.pieces_required()
        boolean = False
        if firstmove:
            boolean = bool2
        else:
            boolean = bool1 and bool2
        if boolean:
            self.pieces_left -= pieces_required
            piece.update_numPieces(pieces_required, self.name)
            if piece.lostTribe:
                piece.lostTribe = False
        return boolean
            
    # player can only go into neighboring spaces, returns true if a neighboring space
    def is_a_move(self, space):
        piece = self.game_board.get_piece(space)
        possible_spaces = set()
        for p in self.spaces_occupied:
            for neighbor in p.neighbors:
                possible_spaces.add(neighbor)
        return piece in possible_spaces

    # player must have enough pieces left, returns true if so
    def enough_pieces(self, space):
        piece = self.game_board.get_piece(space)
        pieces_required = piece.pieces_required()
        return pieces_required <= self.pieces_left 
            





        

        
