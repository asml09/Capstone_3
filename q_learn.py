from game_play import game_play
from game_play import player
from board import board

# create the board
game_board = board()
# 10 turns in the game 
turn = 1
# create the game
game = game_play(game_board)
# randomly decide who goes first
first_player = game.start_game()
game.print_game()
# possible_spaces for first move = [1, 2, 3, 4, 5, 6, 11, 12, 16, 17, 18, 19, 20, 21, 22, 23]
game.take_turn("p1")
game.print_game()
