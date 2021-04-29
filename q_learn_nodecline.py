from game_play import game_play
from game_play import player
from board import board
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, InputLayer
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, InputLayer
import random

# create the board
game_board = board()
# 10 turns in the game 
turn = 1
# create the game
game = game_play(game_board)
# randomly decide who goes first
game.start_game()
# 24 actions, 23 for the number of spaces 1 for going into decline
num_actions = 23
# 5 * number of spaces 5(23) = 115 long vector, for properties 
# 5 to represent each of ['terrain', 'lostTribe', 'numRats', 'numTrolls', 'declineRat', 'declineTroll']
num_states = 115
obs_states = game_board.get_vector()
actions = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10', 'p11', 'p12', 'p13', 'p14',
            'p15', 'p16', 'p17', 'p18', 'p19', 'p20', 'p21', 'p22', 'p23']

model_troll = Sequential()
model_troll.add(InputLayer(batch_input_shape=(1, num_states)))
model_troll.add(Dense(10, activation='sigmoid'))
model_troll.add(Dense(num_actions, activation='linear')) # final output is always linear activation
model_troll.compile(loss='mse', optimizer='adam', metrics=['mae'])

model_rat = Sequential()
model_rat.add(InputLayer(batch_input_shape=(1, num_states)))
model_rat.add(Dense(10, activation='sigmoid'))
model_rat.add(Dense(num_actions, activation='linear')) # final output is always linear activation
model_rat.compile(loss='mse', optimizer='adam', metrics=['mae'])

epsilon = 0.8
game.start_game()
# perhaps check if its legal for random move
# try both
# if np.random.random_sample() < epsilon: 
#     turns = game.whose_turn.possible_spaces()
#     action_num = random.choice(turns)
# else: 
#     # possible_moves = game.possible_moves()
#     # arg sort, go through to things check if legal
#     action_nums = np.argsort(model_troll.predict(obs_states))[::-1]
    
# action = actions[action_num]
# if action_num != 23:
#     game.take_turn(action, True)
# game.print_game()

# model - if it is the model_troll or model_rat
# firstTurn - whether they are starting on the border
def one_action(model, firstTurn):
    reward = -1
    if np.random.random_sample() < epsilon: 
        turns = game.whose_turn.possible_spaces(firstTurn)
        action_num = random.choice(turns)
    else: 
        action_num = -1
        action_nums = np.argsort(model_troll.predict(obs_states))[::-1]
        for i in range(len(action_nums)):
            possible = game.whose_turn.one_move(actions[i], firstTurn)
            print(possible)
            if possible:
                action_num = i
                break
    print(action_num)
    action = actions[action_num]
    reward = game.take_turn(action, firstTurn)
    # NEW CODE
    print(reward)
    print(np.max(model.predict(obs_states)))
    target_q = reward + np.max(model.predict(obs_states))

    target_vec = model.predict(obs_states)[0]
  
    target_vec[action_num] = target_q
    model.fit(obs_states, target_vec.reshape(-1, num_actions), epochs=1, verbose=0)
    game.print_game()
    return reward

while turn < 11:
    # trolls turn
    print('turn ' + str(turn))
    if turn == 1:
        reward = one_action(model_troll, True)
    else:
        game.start_of_turn()
    while game.whose_turn.moves_left():
        reward = one_action(model_troll, False)
    game.distribute_endturn()
    game.change_turns()
    # rats turn
    if turn == 1:
        reward= one_action(model_rat, True)
    else:
        game.start_of_turn()
    while game.whose_turn.moves_left():       
        reward = one_action(model_rat, False)
    game.distribute_endturn()
    game.change_turns()
    turn += 1

