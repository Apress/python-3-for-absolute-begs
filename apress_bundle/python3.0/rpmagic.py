#! /usr/bin/env python3.0
# -*- coding: UTF8 -*-

"""
rpcombat.py
Purpose: Simple Role-Playing Combat Game.
Target System: GNU/Linux
Interface: Command-line
Functional Requirements: The user must be able to generate more than one
 character profile, equip those characters with suitable weapons,
 and model hand-to-hand combat between characters.
Testing methods: trace table and play testing.
Test values: (Ez, Tall, Pixie, female), (Inkon, Small, Troll, male)
Expected results: All statistics should be integers in the (1-99) range.
	Apart from that, this script needs play-testing.
Limitations: Too many to mention.
"""

__version__ = 0.5
__maintainer__ = "maintainer@website.com"
__status__ = "Prototype"

# Import modules

import random

# Preferences
# Set to 'True' to trace variables.
trace = False
reply = input('How many players?: ') or 2
max_players = int(reply)

# This is a global variable.
players = []

class Player:
	
	def setName(self, name):
		self.name = name.capitalize()
		
	def getName(self):
		return self.name
		
	def setDesc(self, desc):
		self.desc = desc.capitalize()
		
	def getDesc(self):
		return self.desc
		
	def setGender(self, gender):
		gender = gender.lower()
		if gender.startswith('f'):
			self.gender = 'female'
		elif gender.startswith('m'):
			self.gender = 'male'
		else:
			self.gender = 'neuter'
		
	def getGender(self):
		return self.gender
		
	def setRace(self, race):
		race = race.capitalize()
		if race.startswith('P'):
			self.race = 'Pixie'
		elif race.startswith('V'):
			self.race = 'Vulcan'
		elif race.startswith('G'):
			self.race = 'Gelfling'
		elif race.startswith('T'):
			self.race = 'Troll'
		else:
			self.race = 'Goblin'
		
	def getRace(self):
		return self.race
	
	def setMuscle(self):
		self.muscle = roll(33,3)

	def getMuscle(self):
		return self.muscle
		
	def setBrainz(self):
		self.brainz = roll(33,3)

	def getBrainz(self):
		return self.brainz

	def setSpeed(self):
		self.speed = roll(33,3)

	def getSpeed(self):
		return self.speed

	def setCharm(self):
		self.charm = roll(33,3) 

	def getCharm(self):
		return self.charm

	def setLife(self):
		self.life = int((self.getMuscle() + (self.getSpeed()/2) + roll(49,1))/2)
		if 0 < self.life < 100:
			pass
		else:
			self.life = int(roll(33,3))
		
	def getLife(self):
		return self.life

	def setMagic(self):
		self.magic = int((self.getBrainz() + (self.getCharm()/2) + roll(49,1))/2)
		if 0 < self.magic < 100:	
			pass
		else:
			self.magic = int(roll(33,3))
	
	def getMagic(self):
		return self.magic

	def setProt(self):
		self.prot = int((self.getSpeed() + (self.getBrainz()/2) + roll(49,1))/2)
		if 0 < self.prot < 100:
			pass
		else:
			self.prot = int(roll(33,3))
	
	def getProt(self):
		return self.prot

	def setGold(self):
		self.gold = int(roll(40,4))

	def getGold(self):
		return self.gold

	def setInv(self):
		self.inventory = []

	def getInv(self):
		return ", ".join(self.inventory)
	
	def __init__(self, store = {}):
		"""Role-Playing Character generator

		Takes no arguments
		Returns a new Player object
		"""
		if store == {}:
			print() 
			print("New Character")
			print() 

			# Prompt user for user-defined information (Name, Desc, Gender, Race)
			name = input('What is your name? ')
			desc = input('Describe yourself: ')
			gender = input('What Gender are you? (male/female/unsure): ')
			race = input('What Race are you? - (Pixie/Vulcan/Gelfling/Troll): ')

			self.setName(name)
			self.setDesc(desc)
			self.setGender(gender)
			self.setRace(race)
			self.setMuscle()
			self.setBrainz()
			self.setSpeed()
			self.setCharm()
			self.setLife()
			self.setMagic()
			self.setProt()
			self.setGold()
			self.setInv()
		else:
			self.__dict__ = store
	
	def __repr__(self):
		return str(vars(self))
	
	def __str__(self):
		# Output the character sheet
		rpcharacter_sheet = """
	<~~==|#|==~~++**\@/**++~~==|#|==~~>
		{name!s}
		{race!s}, {gender!s}
		{desc!s}
	<~~==|#|==~~++**\@/**++~~==|#|==~~>
		Muscle: {muscle: <2}    life:       {life: <3}
		Brainz: {brainz: <2}    magic:      {magic: <3}
		Speed:  {speed: <2}    protection: {prot: <3}
		Charm:  {charm: <2}    gold:  {gold: >7}
	<~~==|#|==~~++**\@/**++~~==|#|==~~>
		::Inventory::
		-------------
		{0!s}
		""".format(self.getInv(), **vars(self))
		return rpcharacter_sheet
		
	def __len__(self):
		return len(vars(self))
		
	def __getitem__(self, key):
		names = vars(self)
		item = names[key]
		return item
		
	def __setitem__(self, key, value):
		self.__dict__[key] = value
		return
	
	def strike(self, target):
		"""Calculate velocity of hit (or miss)

		Takes one argument:
		target is another Player object
		This method looks up values from the players
		and returns a weighted semi-random integer 
		representing the velocity of the strike.
		"""
		weapon = self.weapon
		armour = target.armour
		attack_chance = roll(100)
		attack_velocity = self.getSpeed() + weapon['speed'] + attack_chance
		target_velocity = target.getProt() + armour['speed'] + roll(target.getBrainz())
		velocity = (attack_velocity - target_velocity)
		return int(velocity)

class Thing:
	def __init__(self, price, strength, speed):
		self.price = price
		self.strength = strength
		self.speed = speed
	
	def __str__(self):
		stats = """\tPrice\tStr\tSpeed
	{price!s}\t{strength!s}\t{speed!s}\t""".format(**vars(self))
		return stats
	
	def __repr__(self):
		stats = 'Thing({price!s}, {strength!s}\
, {speed!s})'.format(**vars(self))
		return stats
	
	def __len__(self):
		return len(vars(self))
		
	def __getitem__(self, key):
		names = vars(self)
		try:
			item = names[key]
		except:
			item = 0
		return item

class Weapon(Thing):
	def __init__(self, price, strength, speed):
		self.price = price
		self.strength = strength
		self.damage = strength
		self.speed = speed
	
	def __str__(self):
		stats = """\tPrice\tDamage\tSpeed
	{price!s}\t{damage!s}\t{speed!s}\t""".format(**vars(self))
		return stats
	
	def __repr__(self):
		stats = 'Weapon({price!s}, {strength!s}\
, {speed!s})'.format(**vars(self))
		return stats

class Armour(Thing):
	def __repr__(self):
		stats = 'Armour({price!s}, {strength!s}\
, {speed!s})'.format(**vars(self))
		return stats

# set up constant data.

stock = {'shield':Armour(15,25,50),
		'sword':Weapon(60,60,50),
		'dagger':Weapon(25,40,60),
		'halberd':Weapon(80,75,40),
		'club':Weapon(15,40,40),
		'flail':Weapon(50,60,55),
		'hammer':Weapon(99,100,40),
		'cuirass':Armour(30,50,20),
		'armour':Armour(101,100,0),
		'lantern':Thing(10,5,30),
		'pole':Thing(10,5,50),
		'rope':Thing(10,5,70),
		'box':Thing(5,1,90)}
armour_types = set(['shield','cuirass','armour'])
hits = ('strokes','licks','fingers','caresses','squeezes','spanks',
		'sucks','wanks','takes','screws','fucks')
misses = ('stares at', 'dribbles over', 'is filled with longing for',
		'touches themself up in front of', 'plays with themself whilst watching',
		'gets themself horny for', 'wanks themself off over',
		'makes themself even hornier, to the arousal of')
damage_report = ('moan','tingle with excitement','groan deeply',
				'gasp for breath',
				'ecstatically aroused','ache to reach a climax',
				'tortured with passion','cum to a juddering climax')
life_changing = ('become tantalisingly erect.','blush.','sweat.','tingle',
				'get feverishly aroused.', 'throb with desire.','become filled with longing.',
				'achieve multiple orgasms.','has an earth-shaking orgasm.')

def roll(sides, dice = 1):
	"""Dice rolling simulator
	
	sides: Number of sides the die has
	dice: number of dice to be rolled (defaults to 1)
	Returns a random number between dice and dice * sides 
	weighted towards the average.
	"""
	result = 0
	for rolls in range(1,dice):
		result += random.randint(1,sides)
	return result

def ziply(seq=None):
	"""Create a matrix of matches from a sequence
	
	Takes one argument seq, which should be a sequence of length > 1
	Returns a tuple of tuples - matches.
	"""
	opponents = list(seq[:])
	opponents.reverse()
	matches = [(actor, target) for target in opponents
				for actor in seq  
				if target != actor]
	random.shuffle(matches)  
	return tuple(matches)

def join_with_and(sequence):
	"""Join up a list with commas and 'and' between last two items
	
	Takes a sequence and returns a sentence.
	"""
	if len(sequence) > 1:
		last_item = sequence[-1]
		sentence = ", ".join(sequence[:-1])
		sentence = sentence + " and " + last_item
	elif len(sequence) < 1:
		sentence = "whole lot of nothing"
	else:
		sentence = sequence[0]
	return sentence

def fix_gender(gender, phrase):
	"""Replace the word 'them' with gender-specific pronoun
	
	Takes two arguments:
	gender - a string which can be 'male', 'female' or something else.
	phrase - the string to be modified.
	Returns a string with non-gender specific pronouns replaced by
	gender specific ones.
	"""
	if gender == 'female':
		phrase = phrase.replace('them','her')
		phrase = phrase.replace('their','her')
	elif gender == 'male':
		phrase = phrase.replace('them','him')
		phrase = phrase.replace('their','his')
	else:
		phrase = phrase.replace('them','it')
		phrase = phrase.replace('their','its')
	return phrase

def buy_equipment():
	"""Purchase an item of equipment
	
	Takes no arguments.
	This function modifies the current character profile dictionary in place.
	It returns a value which evaluates as either True or False 
	intended to control the shopping loop.
	"""
	# Display shop stock list with prices.
	stock_list = ["    {0!s:10}{1: >3}".format(item, stock[item]['price']) 
				for item in stock]
	shop = """
<==|#|==\SHOP/==|#|==>
{0}
<==|#|==\@@@@/==|#|==>

You have {1} gold
""".format('\n'.join(stock_list), profile['gold'])
	print(shop)
	
	# Prompt user to make a purchase.
	purchase = input('Please choose an item or type "done" to quit. ')
	# If the item is in stock and the player has enough gold, buy it.
	if purchase in stock:
		if stock[purchase]['price'] <= profile['gold']:
			test_phrase = profile['name'] + " buys themself some equipment"
			print(fix_gender(profile['gender'],test_phrase))
			print("You buy a", purchase, "for",stock[purchase]['price'], \
					"gold pieces.") 
			profile['gold'] -= stock[purchase]['price']
			profile['inventory'].append(purchase)
			print("You have a", join_with_and(profile['inventory']), \
					"in your bag.")
			print("You have", profile['gold'], "left.")
		else:
			print("You don't have enough gold to buy that.")
	elif purchase == 'done' or purchase == "":
		return profile['inventory'] == [] and profile['gold'] > 10
	else:
		print("We don't have", purchase, "in stock.")
	return purchase

def calc_damage(attacker, target, velocity):
	"""Calculate the damage of the hit
	
	Takes three arguments:
	attacker and target are Player objects
	velocity is an integer representing the velocity of the strike.
	Returns a tuple of two integers - damage and potential damage
	"""
	attack_strength = int(attacker['muscle'])
	weapon_damage = int(attacker['weapon']['damage'])
	attack_damage = attack_strength + weapon_damage + int(velocity) - roll(172)
	target_strength = int(target['muscle'])
	armour_strength = int(target['armour']['strength'])
	target_chance = roll(int(target['brainz']) * 3)
	target_defence = target_strength + armour_strength + target_chance
	potential_damage = int((attack_damage - target_defence) * 0.3)
	if potential_damage < 1:
		potential_damage = 2
	damage = random.randint(1,potential_damage)
	return int(damage), int(potential_damage)

def write_out(players):
	print("Saving character sheets")
	data_file = open('rpcharacters.rpg', 'w')
	lines = []
	for player in players:
		lines.append(repr(player) + '\n')
	data_file.writelines(lines)
	data_file.close
	return

def read_in():
	print("Reading in data")
	data_file = open('rpcharacters.rpg')
	for line in data_file:
		stored = eval(line)
		player = Player(stored)
		players.append(player)
	data_file.close()
	#print(players)
	return

##
# The main body of the program starts here,
# So this is where the flow of execution begins.
##
# Generate characters
# Read player stats in from file
read_in()
if len(players) > max_players:
	players = players[:max_players]
while len(players) < max_players:
	# Call character generation function.
	profile = Player()
	# Go shopping if the inventory is empty
	shopping = profile['inventory'] == []
	while shopping:
		shopping = buy_equipment()
	handbag = join_with_and(profile['inventory'])
	print("You own a", handbag)
	
	# Choose a weapon
	print(profile['name'] + ", prepare for mortal combat!!!")
	# See if player has any weapons
	weapon_stats = [stock[item] for item in profile['inventory']
					if item not in armour_types]
	if len(weapon_stats) == 1:
		profile['weapon'] = weapon_stats[0]
	elif len(weapon_stats) < 1:
		profile['weapon'] = Weapon(0,20,50)
	else:
		weapon = input("And choose your weapon: ")
		# The weapon must be in player's inventory.
		# Default to fist if weapon not available.
		weapon = weapon.lower()
		if weapon in profile['inventory']:
			profile['weapon'] = stock[weapon]
		else:
			profile['weapon'] = Weapon(0,20,50)
	# See if player has any armor
	armour_stats = [stock[item] for item in profile['inventory'] 
					if item in armour_types]
	if armour_stats:
		profile['armour'] = armour_stats[0]
	else:
		profile['armour'] = Armour(0,0,50)
			
	print(profile['name'], "is now ready for battle. ")
	# Add new player to list of players
	players.append(profile)

# Save rpcharacters to file
write_out(players)

# Combat

print() 
print("Then let the combat begin!")
print() 

vel_max = 23
vel_min = 1
dam_max = 23
dam_min = 1

# Loop while more than one player is still alive
while len(players) > 1:
	# Seed random generator
	random.seed()
	random.shuffle(players)
	# create list of matches using ziply function
	matches = ziply(list(range(0,len(players))))
	if trace:
		print(matches)
	for attack, targ in matches:
		attacker = players[attack]
		target = players[targ]
		life_left = target.getLife()
		
		# Calculate velocity of blow
		#velocity = calc_velocity(attacker, target)
		velocity = attacker.strike(target)
		if trace:
			print("\tvel\thit\tdam\tchange")
			print("\t", velocity)
		if velocity > 0:
			size = len(hits) - 1
			# Print sutable Hit message
			if velocity > vel_max:
				vel_max = velocity
			hit_type = int(size * velocity / vel_max)
			if hit_type > size:
				hit_type = size
			if trace:
				print("\t\t#", hit_type)
			print(attacker.getName(), hits[hit_type], \
					target.getName(), end=' ')
		else:
			size = len(misses) - 1
			# Print suitable Miss message
			if velocity < vel_min:
				vel_min = velocity
			miss_type = int(size * velocity / vel_max)
			if miss_type > size:
				miss_type = roll(7)
			if miss_type < 0:
				miss_type = roll(7) - 1
			if trace:
				print("\t\t@", miss_type)
			print(attacker.getName(), \
					fix_gender(attacker.getGender(),misses[miss_type]), \
					target.getName())
			# End player turn
			continue
		
		# Calculate damage inflicted by blow
		damage, potential_damage = calc_damage(attacker, target, velocity)
		if trace:
			print()
			print("\t\tDamage:", damage, potential_damage)
		if damage > dam_max:
			dam_max = damage
		elif damage < dam_min:
			dam_min = damage
		# Print damage report
		size = len(damage_report) - 1
		damage_type = int(size * damage / dam_max)
		if damage_type > size:
			damage_type = size
		elif damage_type < 0:
			damage_type = 0
		if trace:
			print("\t\t\t", damage, "#", damage_type)
		size = len(life_changing) - 1
		change_type = int(size * damage / life_left)
		if change_type > size:
			change_type = size
		elif change_type < 0:
			change_type = 0
		if trace:
			print("\t\t\t\t#", change_type)
		outstring = ' '.join(["making them", damage_report[damage_type],"and", life_changing[change_type]])
		output = fix_gender(target.getGender(), outstring)
		print(output)
		
		# Inflict damage on target.
		target['life'] -= damage
		# Check whether target is still alive or not.
		if target.getLife() <= 0:
			# Print loser
			print() 
			print(target.getName(), "collapses in a pool of cum")
			#print(target)
			# Remove loser from players list
			del players[targ]
			print() 
			# End this round of combat immediately.
			break

if trace:
	print() 
	print("\tmax damage | velocity\n\t\t", dam_max, vel_max, "\n\tmin  :: ", dam_min, vel_min)
	print() 

# Print winner
#print(players[0])
print(players[0]['name'], "finally shudders into orgasm.")
# That's all folks!!!
