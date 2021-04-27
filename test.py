from game_play import game_play
from game_play import player
from board import board




# METHODS IN GAME
# start_game() - to start game
# take_turn() - for a player to take a turn, specify if its the players first turn (starting on edge)
# change_turns() - make the opponent the current player
# decline() - go into decline
# after_decline() - call this the turn after going into decline, still have to call take_turn()
# distribute_end_turn() - distribute all of the players pieces
# start_of_turn() - if its not the first turn, call this. Leaves one piece behind on each spot
# coins_earned() - how many coins the player got this turn
# print_game() - current status of the player whose turn it is

# create the board
game_board = board()
# 10 turns in the game 
turn = 1
# create the game
game = game_play(game_board)
# randomly decide who goes first
game.start_game()
game.print_game()
# possible_spaces for first move = [1, 2, 3, 4, 5, 6, 11, 12, 16, 17, 18, 19, 20, 21, 22, 23]
game.take_turn("p2", True)
game.print_game()
game.take_turn("p7", False)
game.print_game()
game.take_turn("p13", False)
game.print_game()
game.take_turn("p18", False)
game.print_game()
game.coins_earned()

game.change_turns()
game.take_turn("p2", True)
game.print_game()
game.take_turn("p7", False)
game.print_game()
game.take_turn("p6", False)
game.print_game()
game.coins_earned()
game.distribute_endturn()
game.print_game()

game.change_turns()
game.decline()
game.print_game()
game.coins_earned()

game.change_turns()
game.start_of_turn()
game.print_game()
game.take_turn("p13", False)
game.print_game()
game.take_turn("p3", False)
game.print_game()
game.take_turn("p9", False)
game.print_game()
game.distribute_endturn()
game.print_game()
game.coins_earned()

game.change_turns()
game.after_decline()
game.print_game()
game.take_turn("p4", True)
game.print_game()
game.take_turn("p9", False)
game.print_game()
game.take_turn("p10", False)
game.print_game()
game.distribute_endturn()
game.print_game()
game.coins_earned()





# for a given space, how many spaces next to it are opponents alive pieces
# space is a string "p1" represents p1
def opponent_neighbor(space):
    whose_turn = game.whose_turn
    count = 0
    piece = game_board.get_piece(space)
    for p in piece.neighbors:
        race = p.get_raceCount(whose_turn.opponent.name)
        if race > 0:
            count += 1
    return count
        
# for a given space, how many spaces next to it are opponents decline pieces
def opponent_neighbor_decline(space):
    whose_turn = game.whose_turn
    count = 0
    piece = game_board.get_piece(space)
    for p in piece.neighbors:
        boolean = p.get_decline(whose_turn.opponent.name)
        if boolean:
            count += 1
    return count

# for a given space, will you earn an extra coin return True or False
def coins(space):
    whose_turn = game.whose_turn
    piece = game_board.get_piece(space)
    # +1 coin for trolls if they are taking a non-empty region
    if whose_turn.name == 'trolls':
        bool1 = piece.get_raceCount(whose_turn.opponent.name)
        bool2 = piece.get_decline(whose_turn.opponent.name)
        bool3 = piece.lostTribe
        if bool1 or bool2 or bool3:
            return True
    else:
        if piece.terrain == 'forest':
            return True
    return False

# how many pieces you have to use to take this space
def pieces_cost(space):
    whose_turn = game.whose_turn
    piece = game_board.get_piece(space)
    return piece.pieces_required

# is an opponent's alive piece in the space you're moving into
def opponent(space):
    whose_turn = game.whose_turn
    piece = game_board.get_piece(space)
    num = piece.get_raceCount(whose_turn.opponent.name)
    return num > 0

# is an opponents decline piece in the space you're moving into
def opponent_decline(space):
    whose_turn = game.whose_turn
    piece = game_board.get_piece(space)
    return piece.get_decline(whose_turn.opponent.name)