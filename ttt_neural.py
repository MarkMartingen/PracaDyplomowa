# class Nueral2Player(NueralPlayer):
# def move(train):
# - pick move with highest reward
# - don't train the network. Instead. If train:
# - update global_training (boards and rewards) after ech move in a global list
#
#
#
# global training_set = []
# for i in range(M):
# play(RandomPlayer, Neural2Player, visible= False)
#
# for element in training_set:
# if first_move(element):
# counter = 1
# elif last_move(element):
# # reward = get_reward(element) <- this will be in the training set
# for i=conter+1 down to 1:
# update_elements_traget(reward, alpha)
# else:s
# counter+=1
# network_train(training_set)

import neural
import ttt
NUM_GAMES = 5 # number of games played in a training session
GLOBAL_TRAINING = []


