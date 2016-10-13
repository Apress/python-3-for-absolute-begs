#! /usr/bin/env python3.0
# -*- coding: UTF8 -*-

"""RPCombat: Simple Role-Playing Combat Game.

Usage: rpcombat.py
You will be prompted to enter a number of players and then you are be taken 
through the character set-up sequence and equip your character with a suitable
weapon.
The characters all engage in hand-to-hand combat until one is victorious!
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
__date__ = "14-12-2008"

# Import modules

import random

# Preferences
# Set to 'True' to trace variables.
trace = False
reply = input('How many players?: ') or 2
max_players = int(reply)

# This is a global variable.
players = []

# Constants
armour_types = set(['shield','cuirass','armour'])
hits = ('hits','bashes','smites','whacks',
		'shreds','stabs','mutilates','lunges at','slashes', 'lacerates',
		'carves up','wipes the floor with')
misses = ('misses', 'nearly hits', 'tickles', 'fumbles', 'fails to connect with',
		'swipes wildly at', 'flails ineffectually at', 'gets nowhere near', 
		'hurts themself badly as a result of gross stupidity',
		'nearly decapitates themself instead of',
		'hits themself on the foot, to the amusement of')
damage_report = ('small insult','flesh wound','deep slash','ragged gash',
				'head butt','savage laceration','fractured rib-cage',
				'smashed-up face','split skull')
life_changing = ('a scar.','bruising.','serious blood-loss.',
				'debilitating force.', 'chronic concussion.',
				'a severed limb left horribly dangling.',
				'multiple fractures.','a broken neck.',
				'a stab to the heart.','a decisive mortal blow.')

def join_with_and(sequence):
	"""Join up a list with commas and 'and' between last two items
	
	Takes a sequence and returns a sentence.
	"""
	# Make sure all the list items are in string format.
	sequence = [str(item) for item in sequence]
	if len(sequence) > 1:
		last_item = sequence[-1]
		sentence = ", ".join(sequence[:-1])
		sentence = sentence + " and " + last_item
	elif len(sequence) < 1:
		sentence = "whole lot of nothing"
	else:
		sentence = sequence[0]
	return sentence

class GameObject:
	"""Generic Game Object
	
	One class to rule them all
	"""
	
	def setName(self, name):
		self._name = name.capitalize()
		
	def getName(self):
		return self._name
		
	name = property(getName, setName)
	
	def setDesc(self, desc):
		self._desc = desc.capitalize()
		
	def getDesc(self):
		return self._desc
		
	desc = property(getDesc, setDesc)
			
	def setGender(self, gender):
		gender = gender.lower()
		if gender.startswith('f'):
			self._gender = 'female'
		elif gender.startswith('m'):
			self._gender = 'male'
		else:
			self._gender = 'neuter'
		
	def getGender(self):
		return self._gender
		
	gender = property(getGender, setGender)
		
	def setRace(self, race):
		race = race.capitalize()
		if race.startswith('P'):
			self._race = 'Pixie'
		elif race.startswith('V'):
			self._race = 'Vulcan'
		elif race.startswith('G'):
			self._race = 'Gelfling'
		elif race.startswith('T'):
			self._race = 'Troll'
		else:
			self._race = 'Goblin'
		
	def getRace(self):
		return self._race
		
	race = property(getRace, setRace)
	
	def setStrength(self):
		self._strength  = roll(33,3)
		
	def getStrength(self):
		return self._strength
		
	strength = property(getStrength)
		
	def setBrainz(self):
		self._brainz = roll(33,3)
		
	def getBrainz(self):
		return self._brainz
		
	brainz = property(getBrainz)
	
	def setSpeed(self):
		self._speed = roll(33,3)
		
	def getSpeed(self):
		return self._speed
		
	speed = property(getSpeed)
	
	def setCharm(self):
		self._charm = roll(33,3)
		
	def getCharm(self):
		return self._charm
		
	charm = property(getCharm)
	
	def setLife(self, value):
		self._life = int(value)
		
	def getLife(self):
		return self._life
		
	life = property(getLife, setLife)
	
	def setMagic(self, value):
		self._magic = int(value)
		
	def getMagic(self):
		return self._magic
		
	magic = property(getMagic, setMagic)
	
	def setProt(self, value):
		self._prot = int(value)
		
	def getProt(self):
		return self._prot
		
	prot = property(getProt, setProt)
	
	def setGold(self, value):
		self._gold = int(value)
		
	def getGold(self):
		return self._gold
		
	gold = property(getGold, setGold)
	
	def setInv(self, contents):
		self.inv = contents
	
	def getInv(self):
		return self.inv
		
	def strInv(self):
		flatlist = [str(item) for item in self.inv]
		text = join_with_and(flatlist)
		return text
		
	inventory = property(getInv, setInv)

class Player(GameObject):
	
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
			self.setStrength()
			self.setBrainz()
			self.setSpeed()
			self.setCharm()
			self._life = int((self.strength + (self.speed / 2) + roll(49,1))/2)
			if 0 < self._life < 100:
				pass
			else:
				self._life = int(roll(33,3))
			self._magic = int((self.brainz + (self.charm / 2) + roll(49,1))/2)
			if 0 < self._magic < 100:	
				pass
			else:
				self._magic = int(roll(33,3))
			self._prot = int((self.speed + (self.brainz / 2) + roll(49,1))/2)
			if 0 < self._prot < 100:
				pass
			else:
				self._prot = int(roll(33,3))
			self._gold = int(roll(40,4))
			self.setInv([])
		else:
			self.__dict__ = store
	
	def __repr__(self):
		return str(vars(self))
	
	def __str__(self):
		# Output the character sheet
		rpcharacter_sheet = """
	<~~==|#|==~~++**\@/**++~~==|#|==~~>
		{_name!s}
		{_race!s}, {_gender!s}
		{_desc!s}
	<~~==|#|==~~++**\@/**++~~==|#|==~~>
		Strength: {_strength: <2}    life:       {_life: <3}
		Brainz:   {_brainz: <2}    magic:      {_magic: <3}
		Speed:    {_speed: <2}    protection: {_prot: <3}
		Charm:    {_charm: <2}    gold: {_gold: >7}
	<~~==|#|==~~++**\@/**++~~==|#|==~~>
		::Equipment::
		{0!s}
		""".format(self.strInv(), **vars(self))
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
		
	def equip(self):
		"""Purchase an item of equipment

		Takes no arguments.
		This function modifies the current character profile dictionary in place.
		It returns a value which evaluates as either True or False 
		intended to control the shopping loop.
		"""
		# Display shop stock list with golds.
		stock_list = ["    {0!s:10}{1: >3}".format(item, stock[item]['gold']) 
					for item in stock]
		shop = """
	<==|#|==\SHOP/==|#|==>
	{0}
	<==|#|==\@@@@/==|#|==>

	You have {1} gold
	""".format('\n'.join(stock_list), profile.gold)
		print(shop)

		# Prompt user to make a purchase.
		purchase = input('Please choose an item or type "done" to quit. ')
		# If the item is in stock and the player has enough gold, buy it.
		if purchase in stock:
			if stock[purchase].gold <= profile.gold:
				test_phrase = profile.name + " buys themself some equipment"
				print(fix_gender(profile.gender, test_phrase))
				print("You buy a", purchase, "for",stock[purchase].gold, \
						"gold pieces.") 
				profile.gold -= stock[purchase].gold
				profile.inventory.append(stock[purchase])
				print("You have a", join_with_and(profile.inventory), \
						"in your bag.")
				print("You have", profile.gold, "left.")
			else:
				print("You don't have enough gold to buy that.")
		elif purchase == 'done' or purchase == "":
			return profile.inventory == [] and profile.gold > 10
		else:
			print("We don't have", purchase, "in stock.")
		return purchase
	
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
		attack_velocity = self.speed + weapon['speed'] + attack_chance
		target_velocity = target.prot + armour['speed'] + roll(target.brainz)
		velocity = (attack_velocity - target_velocity)
		return int(velocity)

class Thing(GameObject):
	def __init__(self, name, gold, strength, speed):
		self._gold = gold
		self._strength = strength
		self._speed = speed
		self._name = name
		self._desc = ''
	
	def __str__(self):
		return str(self.name)
	
	def __repr__(self):
		stats = 'Thing({_name!r}, {_gold!s}, {_strength!s}\
, {_speed!s})'.format(**vars(self))
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
	
	def __repr__(self):
		stats = 'Weapon({_name!r}, {_gold!s}, {_strength!s}\
, {_speed!s})'.format(**vars(self))
		return stats

class Armour(Thing):
	
	def __repr__(self):
		stats = 'Armour({_name!r}, {_gold!s}, {_strength!s}\
, {_speed!s})'.format(**vars(self))
		return stats
		
class Location(GameObject):
	
	def __init__(self, name = 'Somewhere'):
		self._name = name.capitalize()
		self._desc = "It looks like a building site, nothing much to see yet."
		self.setInv([])
		
	def __str__(self):
		view = """<==|#|==\{_name!s}/==|#|==>
 {_desc!s}
 contents:
 {0!s}
 <==|#|==\@@@@/==|#|==>
 """.format(self.strInv(), **vars(self))
		return view
	
	def __repr__(self):
		return str(vars(self))

# Set up locations
shop = Location('shop')
shop.inventory = [Armour('shield',15,25,50),
		Weapon('sword',60,60,50),
		Weapon('dagger',25,40,60),
		Weapon('halberd',80,75,40),
		Weapon('club',15,40,40),
		Weapon('flail',50,60,55),
		Weapon('hammer',99,100,40),
		Armour('cuirass',30,50,20),
		Armour('armour',101,100,0),
		Thing('lantern',10,5,30),
		Thing('pole',10,5,50),
		Thing('rope',10,5,70),
		Thing('box',5,1,90)]
stock_list = ["    {0!s:10}{1: >3}".format(item, item.gold) 
					for item in shop.inventory]
shop.desc = """Welcome to your friendly local equipment store.
Price List:
{0}
""".format('\n'.join(stock_list))
		
print(shop)

# set up constant data.

stock = {'shield':Armour('shield',15,25,50),
		'sword':Weapon('sword',60,60,50),
		'dagger':Weapon('dagger',25,40,60),
		'halberd':Weapon('halberd',80,75,40),
		'club':Weapon('club',15,40,40),
		'flail':Weapon('flail',50,60,55),
		'hammer':Weapon('hammer',99,100,40),
		'cuirass':Armour('cuirass',30,50,20),
		'armour':Armour('armour',101,100,0),
		'lantern':Thing('lantern',10,5,30),
		'pole':Thing('pole',10,5,50),
		'rope':Thing('rope',10,5,70),
		'box':Thing('box',5,1,90)}


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

def fix_gender(gender, phrase):
	"""Replace the word 'them' with gender-specific pronoun
	
	Takes two arguments:
	gender - a string which can be 'male', 'female' or something else.
	phrase - the string to be modified.
	Returns a string with non-gender specific pronouns replaced by
	gender specific ones.
	"""
	if gender == 'female':
		sentence = phrase.replace('themself','herself')
	elif gender == 'male':
		sentence = phrase.replace('themself','himself')
	else:
		sentence = phrase.replace('themself','itself')
	return sentence

def calc_damage(attacker, target, velocity):
	"""Calculate the damage of the hit
	
	Takes three arguments:
	attacker and target are Player objects
	velocity is an integer representing the velocity of the strike.
	Returns a tuple of two integers - damage and potential damage
	"""
	attack_strength = int(attacker.strength)
	weapon_damage = int(attacker['weapon'].strength)
	attack_damage = attack_strength + weapon_damage + int(velocity) - roll(172)
	target_strength = int(target.strength)
	armour_strength = int(target['armour'].strength)
	target_chance = roll(int(target.brainz) * 3)
	target_defence = target_strength + armour_strength + target_chance
	potential_damage = int((attack_damage - target_defence) * 0.3)
	if potential_damage < 1:
		potential_damage = 2
	damage = random.randint(1,potential_damage)
	return int(damage), int(potential_damage)

def trace(text):
	if trace:
		print(text)

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
if __name__ == '__main__':
	# Set up players
	# Read player stats in from file
	read_in()
	if len(players) > max_players:
		players = players[:max_players]
	while len(players) < max_players:
		# Generate new player.
		profile = Player()
		# Equip player if the inventory is empty
		shopping = profile.inventory == []
		while shopping:
			shopping = profile.equip()
		handbag = join_with_and(profile.inventory)
		print("You own a", handbag)

		# Choose a weapon
		print(profile.name + ", prepare for mortal combat!!!")
		# See if player has any weapons
		available_weapons = [stock[item] for item in profile.inventory
						if type(item) is 'Weapon']
		if len(available_weapons) == 1:
			profile['weapon'] = available_weapons[0]
		elif len(available_weapons) < 1:
			profile['weapon'] = Weapon('fist',0,20,50)
		else:
			weapon = input("And choose your weapon: ")
			# The weapon must be in player's inventory.
			# Default to fist if weapon not available.
			weapon = weapon.lower()
			if weapon in profile.inventory:
				profile['weapon'] = stock[weapon]
			else:
				profile['weapon'] = Weapon('fist',0,20,50)
		# See if player has any armor
		available_armour = [stock[item] for item in profile.inventory 
						if type(item) is 'Armour']
		if available_armour:
			profile['armour'] = available_armour[0]
		else:
			profile['armour'] = Armour('none',0,0,50)
		
		print(profile.name, "is now ready for battle. ")
		# Add new player to list of players
		players.append(profile)
	
	# Save rpcharacters to file
	write_out(players)
	
	#TODO: Create a command-line, let player initiate combat.
	#TODO: Abstract combat into separate function
	# Combat
	
	print() 
	print("Let the combat begin!")
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
		trace(matches)
		for attack, targ in matches:
			attacker = players[attack]
			target = players[targ]
			life_left = target.life
			
			# Calculate velocity of blow
			velocity = attacker.strike(target)
			
			if velocity > 0:
				size = len(hits) - 1
				# Print sutable Hit message
				if velocity > vel_max:
					vel_max = velocity
				hit_type = int(size * velocity / vel_max)
				if hit_type > size:
					hit_type = size
				strike_msg = ''.join(['#', str(hit_type)])
				print(attacker.name, hits[hit_type], \
						target.name, end=' ')
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
				strike_msg = ''.join(['@', str(miss_type)])
				print(attacker.name, \
						fix_gender(attacker.gender, misses[miss_type]), \
						target.name)
				# End player turn
				continue

			# Calculate damage inflicted by blow
			damage, potential_damage = calc_damage(attacker, target, velocity)
			
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
			
			size = len(life_changing) - 1
			change_type = int(size * damage / life_left)
			if change_type > size:
				change_type = size
			elif change_type < 0:
				change_type = 0
			print("causing a", damage_report[damage_type], \
					"with", life_changing[change_type])
			trace("""
 >: vel[{0}] :: hit[{1}] :: dam[{2}/{3}] :: type[#{4}] :: change[#{5}] :< 
""".format(velocity, strike_msg, damage, potential_damage, damage_type, change_type))

			# Inflict damage on target.
			target.life -= damage
			# Check whether target is still alive or not.
			if target.life <= 0:
				# Print loser
				print() 
				print(target.name, "collapses in a pool of blood")
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
	print(players[0])
	print(players[0].name, "wins the fight.")
	# That's all folks!!!
