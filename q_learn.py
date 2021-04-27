from game_play import game_play
from game_play import player
from board import board
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, InputLayer
import numpy as np



# create the board
game_board = board()
# 10 turns in the game 
turn = 1
# create the game
game = game_play(game_board)
# randomly decide who goes first
game.start_game()

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, InputLayer

# model.predict(vector_from_game)
# one dimensional vector that has same number of values as neural network so 115 long


# count coins (reward) for every step, how many coins you got for that particular area taken
# 24 actions, 23 for the number of spaces 1 for going into decline
num_actions = 
# number of spaces, number in state representing it +5 if 5 rats, -5 is 5 trolls
# 5 * number of spaces 5(23) = 115 long vector ACTUALLLY NO just do 24, one for each state
num_states = 

model = Sequential()
model.add(InputLayer(batch_input_shape=(1, 10)))
model.add(Dense(10, activation='sigmoid'))
model.add(Dense(20, activation='linear'))
model.compile(loss='mse', optimizer='adam', metrics=['mae'])
print(model.predict(obs_states[1:2]))


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

