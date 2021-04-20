from board import board
import random

# player 1 - ratmen and forest
# 12 player pieces, +1 for every forest region occupied

# player 2 - trolls and pillaging
# 10 player pieces, +1 for every non-empty region conquered. +1 defense for every region occupied

game_board = board()

class game_play:
    def __init__(self):
        self.Ratmen = player(12, 'forest_power', 'lots_of_people', 'ratmen')
        self.Trolls = player(10, 'one_extra_defense', 'one_coin_non_empty', 'trolls')
        self.Ratmen.opponent = self.Trolls
        self.Trolls.opponent = self.Ratmen
        self.rat_spaces_occupied = []
        self.troll_spaces_occupied = []
        

    # first move for both the players
    def start(self):
        number = random.randint(0, 1)
        self.whose_turn = None
        # Ratmen first
        if number == 0:
            self.whose_turn = self.Ratmen
        else:
            self.whose_turn = self.Trolls  

    # make one move within a turn (a turn consists of multiple moves)
    def take_turn(self, space):
        player = self.whose_turn
        opponent = self.whose_turn.opponent
        piece = game_board.get_piece(space)
        self.whose_turn.one_move(piece)
        player.spaces_occupied.append(piece)
        num_opponent = piece.get_raceCount(opponent)
        # If this player is attacking an opponent, the piece is updated to no longer store the opponent
        # The player class for the opponent is updated so that they no longer occupy that space 
        # 1 is subtracted from the number of pieces this player has
        if num_opponent > 0:
            piece.update_numPieces(0, opponent)
            opponent.spaces_occupied.remove(piece)
            opponent.num_pieces -= 1

    def decline(self):
        pieces_declined = []
        if self.whose_turn == self.Ratmen:
            pieces_declined = self.rat_spaces_occupied
        else:
            pieces_declined = self.troll_spaces_occupied
        for piece in pieces_declined:
            piece.decline_space(self.whose_turn.name)



    # At the start of a players turn, one piece is left behind in each of the areas they own. 
    # def start_turn(self):


# def one_turn(whose_turn):


class player:
    def __init__(self, num_pieces, race_power, special_power, name):
        self.num_pieces = num_pieces
        self.race_power = race_power
        self.special_power = special_power
        self.name = name
        self.opponent = None
        self.spaces_occupied = []


    # possible_spaces for first move = [1, 2, 3, 4, 5, 6, 11, 12, 16, 17, 18, 19, 20, 21, 22, 23]
    # space is a number - 3 would represent p3
    def one_move(self, space):
        self.pieces_left = self.num_pieces
        boolean = self.is_a_move(space)
        piece = game_board.get_piece(space)
        pieces_required = piece.pieces_required()
        if boolean:
            self.pieces_left -= pieces_required
            piece.update_numPieces(pieces_required, self.name)
            if piece.lostTribe == True:
                piece.lostTribe = False
            

    # returns true or false depending on if the move is legal
    def is_a_move(self, space):
        piece = game_board.get_piece(space)
        pieces_required = piece.pieces_required()
        return self.pieces_left < pieces_required




        

        
