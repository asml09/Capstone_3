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
num_actions = 24
# 5 * number of spaces 5(23) = 115 long vector, for properties 
# 5 to represent each of ['terrain', 'lostTribe', 'numRats', 'numTrolls', 'declineRat', 'declineTroll']
num_states = 115
obs_states = game_board.get_vector()
actions = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10', 'p11', 'p12', 'p13', 'p14',
            'p15', 'p16', 'p17', 'p18', 'p19', 'p20', 'p21', 'p22', 'p23', 'decline']

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
    decline = False
    if np.random.random_sample() < epsilon: 
        turns = game.whose_turn.possible_spaces(firstTurn)
        action_num = random.choice(turns)
        print(action_num)
    else: 
        action_num = -1
        action_nums = np.argsort(model_troll.predict(obs_states))[::-1]
        for i in range(len(action_nums)):
            possible = game.whose_turn.one_move(actions[i], firstTurn)
            if possible == True:
                action_num = i
                print(action_num)
            break
    action = actions[action_num]
    print(action)
    if action != 'decline':
        reward = game.take_turn(action, firstTurn)
    else:
        game.decline()
        # CHANGE THIS
        reward = -1
        decline = True
    game.print_game()
    return reward, decline

just_declined_rat = False
just_declined_troll = False
while turn < 11:
    # trolls turn
    print('turn ' + str(turn))
    if turn == 1:
        reward, decline = one_action(model_troll, True)
        if decline:
            just_declined_troll = True
    if just_declined_troll:
        game.after_decline()
        just_declined_troll = False
        reward, decline = one_action(model_troll, True)
        if decline:
            just_declined_troll = True
    while game.whose_turn.moves_left():
        if turn != 1 and not just_declined_troll:
            game.start_of_turn()
        reward, decline = one_action(model_troll, False)
        if decline:
            just_declined_troll = True
    game.distribute_endturn()
    game.change_turns()
    # rats turn
    if turn == 1:
        reward, decline = one_action(model_rat, True)
        if decline:
            just_declined_rat = True
    if just_declined_troll:
        game.after_decline()
        just_declined_rat = False
        reward, decline = one_action(model_rat, True)
        if decline:
            just_declined_rat = True
    while game.whose_turn.moves_left():
        if turn != 1 and not just_declined_rat:
            game.start_of_turn()
        reward, decline = one_action(model_rat, False)
        if decline:
            just_declined_rat = True
    game.distribute_endturn()
    game.change_turns()
    turn += 1








# Q value - state, action
# Training neural network to predict, given a particular state (defined by features), what the value 

# you make a move, the opponent makes a move. Manager creates two agents, each agent has its own neural 
# network. Create a game, figure out what the state of the game is. When it asks an agent to move, 
# moving consists of two parts. Updates state based on last move, then chooses the best move for the
# future (easy part). Each agent has a neura network, predicts q values for different actions 
# chooses which is best. Follow epsilon-greedy strategy (10% of time, do a random thing), (as game goes on
# simulated annealing) start with 10%. Won't start as all 0's, will start as random number
# so doing 10% will still be basically random
# time choose whichever action corresponds to highest q value
# Before it does that, update the network based on

# Environment is game board
# Manager is saying it's your turn, this is what the state is, this is what you want to do (q_learn)

# Someone does something, game tells you how successful you are 
# (how many coins that turn - how many coins opponent got) - reward r
# Manager tells them current state, reward they just got. Also tell them where they were the previous
# and the current state's Q is how good the previous --> present state was
# put present state through neural network, look at all possible results, look at q_max (which is
# value of present state) 
# value of last state = vlue of present state * discount (maybe 0.9 - 1) + reward from previous state

# Q - state, action pairs

# Q(st+ 1) - where you are now, max over this is all tbe actions you could take from there 
# Q(st) - where you were previously
# alpha - 

# some kind of input
# If someone takes a tur n, directly return how many coins

# function that returns state of system. Integer for every territory, 
# maybe add these features into a state

# coins that you get that turn are reward, features + state are q values
# negative reward for doing illegal move. 
# another idea (prob not) - reward could be whether you win or lose 

# 2 -3 hidden layers

# Q value - (2, 3, 5, 4, ) = w1(2) + w2(3) 
# Q values are created each time, even the old value

# keras save model, saves it for each time you run
# methods for save, load model

# model.predict(vector_from_game)
# one dimensional vector that has same number of values as neural network so 115 long


# count coins (reward) for every step, how many coins you got for that particular area taken

