#! /usr/bin/env python

import random

players = ('Thales', 'Ez')
speeds = ('Superhero', 'Speedy', 'Mr Average', 'Slowcoach', 'Stupid')

def ziply(sides=None):
	opponents = list(sides[:])
	opponents.reverse()
	matches = [(actor, target) for actor in sides 
				for target in opponents 
				if target != actor]  
	return tuple(matches)

def roll(sides, dice = 1):
	result = 0
	for rolls in range(1,dice):
		result += random.randint(1,sides)
	return result
	
player_list = sorted([(roll(33,3), player) for player in players])
players = reversed([player_tup[1] for player_tup in player_list])

for (a_desc, player), (t_desc, target) in ziply(list(zip(speeds, players))):
	print(a_desc, player, "hits", t_desc, target)
print(player_list)
