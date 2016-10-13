#! /usr/bin/env python3.0
# -*- coding: UTF8 -*-

"""RPCombat: Simple Role-Playing Combat Game.

Usage: rpcombat.py
First you are prompted to enter the number of players you want and then you 
are taken through character generation where you get the chance to equip your 
character with a suitable weapon at our fabulous Emporium.
Available commands: *look*, *buy <item>*
The characters then engage in hand-to-hand combat in the arena until one is 
victorious!
Available commands: *look*, *attack*, *say*
Target System: GNU/Linux
Interface: Command-line
Functional Requirements: The user must be able to generate more than one
 character profile, equip those characters with suitable weapons,
 and model hand-to-hand combat between characters.
Testing methods: trace table and play testing.
Expected results: All statistics should be integers in the (1-99) range.
	Apart from that, this script needs play-testing.
Limitations: Too many to mention.
"""

__version__ = 0.6
__maintainer__ = "maintainer@website.com"
__status__ = "Prototype"
__date__ = "16-12-2008"

# Import modules

import random
import time

# Preferences
###
Boilerplate = """
<==|#|==\@@@@/==|#|==>
  Cloud Cuckoo Land
  A simple role-playing game
  version: {0!s}
<==|#|==\@@@@/==|#|==>
""".format(__version__)

# Set to 'True' to trace variables.
trace_on = False

# Set amount of delay between combat strikes
# Higher numbers make combat slower
drag = 23

# Create players list
players = []

# Constants
armour_types = set(['shield','cuirass','armour'])
hits = ('hits','bashes','smites','whacks',
		'shreds','stabs','mutilates','lunges at','slashes', 'lacerates',
		'carves up','wipes the floor using')
misses = ('misses', 'nearly hits', 'tickles', 'fumbles', 'fails to connect with',
		'swipes wildly at', 'flails ineffectually at', 'gets nowhere near', 
		'hurts themself badly as a result of gross stupidity',
		'nearly decapitates themself instead of',
		'hits themself on the foot, to the amusement of')
damage_report = ('a small insult','a flesh wound','a deep gouge','ragged tearing of skin',
				'blood to spurt everywhere', 'massive head injuries','savage laceration',
				'a fractured rib-cage','facial mutilation','the skull to split in two')
life_changing = ('a scar.','internal bruising.','serious blood-loss.',
				'other debilitating injuries.', 'chronic concussion.',
				'leaving a severed limb dangling at a horrible angle.',
				'multiple fractures.','a broken neck.',
				'the rupturing of internal organs.','a decisive mortal blow.')

class GameObject:
	"""Generic Game Object
	
	One class to rule them all.
	The class sets up the properties which are available to all GameObject
	sub-classes. It has no methods of its own. The idea is that the other
	game objects, Players, Things and Locations are all sub-classes of
	GameObject; features shared by all GameObjects should go here.
	Text properties: name, desc, gender and race. 
	Base stats: strength, brainz, speed and charm. 
	Derived stats: life, magic, prot and gold.
	Plus an inventory list.
	"""
	
	def setName(self, name):
		self._name = name.title()
		
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
	"""Role-Playing Character

	Takes an optional dictionary as an argument.
	The dictionary must contain the output of repr(Player)
	Player([dict]), if dict is not provided, the Player will self-generate,
	prompting for name, desc, gender and race.
	Player has two methods: 
	Player.buy(purchase)
	Player.strike(target)
	"""
	
	def __init__(self, store = {}):
		if store == {}:
			print("\nNew Character\n") 

			# Prompt user for user-defined information (Name, Desc, Gender, Race)
			name = input('What is your name? ')
			desc = input('Describe yourself: ')
			gender = input('What Gender are you? (male/female/unsure): ')
			race = input('What Race are you? - (Pixie/Vulcan/Gelfling/Troll): ')
			
			# Set game statistics
			self.setName(name)
			self.setDesc(desc)
			self.setGender(gender)
			self.setRace(race)
			self.setStrength()
			self.setBrainz()
			self.setSpeed()
			self.setCharm()
			
			# Calculate derived statistics
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
			
			# Equip player if the inventory is empty
			shopping = self.inventory == []
			if shopping:
				# Display shop stock list with prices in gold.
				print("You have", self.gold, "gold.")
				shop.enter(self)
			handbag = join_with_and(self.inventory)
			print("You own a", handbag)

			# Choose a weapon
			print(self.name + ", prepare for mortal combat!!!")
			# See if player has any weapons
			available_weapons = [item for item in self.inventory
							if issubclass(type(item), Weapon)]
			available_weapons.append(Weapon('Fist', 0, 20, 50))
			self.weapon = available_weapons[0]

			# See if player has any armor
			available_armour = [item for item in self.inventory 
							if issubclass(type(item), Armour)]
			available_armour.append(Armour('None', 0, 0, 50))
			self.armour = available_armour[0]

		else:
			# Load character from stored value.
			self.__dict__ = store
		
		print(self.name, "is now ready for battle. ")
	
	def __repr__(self):
		# Output class constructor string.
		stats = 'Player({0!s})'.format(vars(self))
		return stats
	
	def __str__(self):
		# Output the character sheet.
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
		# Return the number of attributes
		return len(vars(self))
		
	def __getitem__(self, key):
		# Retrieve values by index
		names = vars(self)
		item = names[key]
		return item
		
	def __setitem__(self, key, value):
		# Set values by index
		self.__dict__[key] = value
		return
	
	def buy(self, purchase):
		""" Buy item
		
		If the item is in the shop and the player has enough gold, buy it.
		Takes one argument, purchase, which is the name of the item you want
		to buy.
		"""
		items = [item for item in shop.inventory 
				if issubclass(type(item), Thing) and item.name == purchase.capitalize()]
		if items == []:
			print("We don't have a", purchase, "for sale.")
		elif 0 < items[0].gold <= self.gold:
			item = items[0]
			msg = fix_gender(self.gender, self.name + " buys themself some equipment")
			print(msg)
			print("You buy a", purchase, "for",item.gold, "gold pieces.") 
			self.gold -= item.gold
			self.inventory.append(item)
			print("You have a", self.strInv(), "in your bag.")
			print("You have", self.gold, "gold left.")
		else:
			print("You don't have enough gold to buy that.")
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
		attack_chance = roll(99)
		attack_velocity = self.speed + weapon.speed + attack_chance
		target_velocity = target.prot + armour.speed + roll(target.brainz)
		velocity = (attack_velocity - target_velocity)
		return int(velocity)

class Thing(GameObject):
	"""Tools and Treasure
	
	Takes four mandatory arguments:
	Thing(name, gold, strength, speed)
	where name is a string and gold, strength speed are integers between 0-99.
	Things are largely immutable and have no public methods.
	Attributes may be retrieved using index notation.
	"""
	
	def setStrength(self, value):
		self._strength  = value
		
	def getStrength(self):
		return self._strength
		
	strength = property(getStrength)
	
	def setSpeed(self, value):
		self._speed = value
		
	def getSpeed(self):
		return self._speed
		
	speed = property(getSpeed)
	
	def __init__(self, name, gold, strength, speed):
		self.setGold(gold)
		self.setStrength(strength)
		self.setSpeed(speed)
		self.setName(name)
		self.setDesc('')
	
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
	"""Weapon - subclass of Thing"""
	
	def __repr__(self):
		stats = 'Weapon({_name!r}, {_gold!s}, {_strength!s}\
, {_speed!s})'.format(**vars(self))
		return stats

class Armour(Thing):
	"""Armour - subclass of Thing"""
	
	def __repr__(self):
		stats = 'Armour({_name!r}, {_gold!s}, {_strength!s}\
, {_speed!s})'.format(**vars(self))
		return stats
		
class Location(GameObject):
	"""Game Location
	
	Takes two optional arguments, either:
	Location([name]) - which creates a new location called *name*.
	Location([dict]) - which loads a stored location from a dictionary
	Locations provide the environment in which game-play can occur.
	Locations have several public methods:
	Location.enter(player) - adds player to location and provides prommpt.
	Location.interpret(command, player) - executes in-game commands.
	Location.combat() - initializes comabt sequence.
	Location.resolve_conflict(attacker, target) - resolves comabt rounds.
	Location.exit(player) - removes player from location.
	"""
	
	def __init__(self, name = 'Somewhere', store = {}):
		if store == {}:
			self._name = name.capitalize()
			self._desc = "It looks like a building site, nothing much to see yet."
			self.setInv([])
			self.commands = {'look':'print({0!s})',
							'attack':'self.combat()',
							'say':'print(me.name, "says", {0!r})'}
		else:
			self.__dict__ = store		
		
	def __str__(self):
		rpcs = [item.name for item in self.inv if issubclass(type(item), Player)]
		stuff = [str(item) for item in self.inv if issubclass(type(item), Thing)]
		view = """
<==|#|==\{_name!s}/==|#|==>
 {_desc!s}
 Contents:
 {0!s}
 Players:
 {1!s}
<==|#|==\@@@@/==|#|==>
 """.format(join_with_and(stuff), join_with_and(rpcs), **vars(self))
		return view
	
	def __repr__(self):
		# Output class constructor string.
		stats = 'Location({0!s})'.format(vars(self))
		return stats
		
	def __contains__(self, item):
		# *in* checks contents of inventory
		# Can match against strings or Things (ie. GameObjects)
		objects = [str(i) for i in self.inv]
		if item in self.inv:
			return True
		elif item in objects:
			return True
		else:
			return False
	
	def interpret(self, command, player):
		"""Game Command interpreter
		
		Takes two arguments:
		command - the command string
		player - a player object
		Executes the command string by retrieving string from
		self.commands, formatting it and sending to exec().
		It returns no value.
		Note: There are probably more secure ways of doing this. ;-)
		"""
		here = self
		me = player
		command_list = command.split()
		if command != '' and command_list[0] in self.commands:
			command = self.commands[command_list[0]]
			if len(command_list) > 1:
				command = command.format(' '.join(command_list[1:]), target = player)
			else:
				command = command.format('self', target = player)
			trace("Command:", command)
			try:
				exec(command)
			except:
				print("No can do.")
		return
	
	def enter(self, player):
		"""Commands run when the player enters a location
		
		Takes a player object as an argument.
		Adds Player to the location's inventory
		Provides a command-line prompt until 'exit' is called.
		No return value.
		"""
		command = 'enter'
		self.inventory.append(player.name)
		print(self)
		print("You enter the", self.name)
		while command != 'exit':
			command = input(":-> ")
			self.interpret(command, player)
		self.exit(player)
		return
	
	def damage(self, attacker, target, velocity):
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
	
	def resolve_conflict(self, attacker, target):
		"""Conflict Resolution
		
		Takes two Player objects as arguments, relating to the *attacker* and *target*.
		Calculates velocity, hit or miss, calculates and inflicts appropriate damage.
		Prints out a commentary on the action to the world.
		Returns True if the blow resulted in fatality, False if the blow misses.
		"""
		life_left = target.life
		# Calculate velocity of blow
		velocity = attacker.strike(target)
		
		if velocity > 0:
			size = len(hits) - 1
			# Print sutable Hit message
			if velocity > self._vel_max:
				self._vel_max = velocity
			hit_type = int(size * velocity / self._vel_max)
			if hit_type > size:
				hit_type = size
			strike_msg = ''.join(['#', str(hit_type)])
			print(attacker.name, hits[hit_type], \
					target.name, end=' ')
		else:
			size = len(misses) - 1
			# Print suitable Miss message
			if velocity < self._vel_min:
				self._vel_min = velocity
			miss_type = int(size * velocity / self._vel_max)
			if miss_type > size:
				miss_type = roll(7)
			if miss_type < 0:
				miss_type = roll(7) - 1
			strike_msg = ''.join(['@', str(miss_type)])
			print(attacker.name, \
					fix_gender(attacker.gender, misses[miss_type]), \
					target.name)
			# End player turn
			return False
		
		# Calculate damage inflicted by blow
		damage, potential_damage = self.damage(attacker, target, velocity)
		
		if damage > self._dam_max:
			self._dam_max = damage
		elif damage < self._dam_min:
			self._dam_min = damage
		# Print damage report
		size = len(damage_report) - 1
		damage_type = int(size * damage / self._dam_max)
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
		outstring = ' '.join(["with their", attacker['weapon'].name.lower(),
							"causing", damage_report[damage_type],
							"and", life_changing[change_type]])
		output = fix_gender(attacker.gender, outstring)
		print(output)
		trace("""vel[{0}] :: hit[{1}] :: dam[{2}/{3}] :: type[#{4}] :: change[#{5}] 
		""".format(velocity, strike_msg, damage, potential_damage, damage_type, change_type))
		
		# Inflict damage on target.
		target.life -= damage
		# Pause slightly to stop this all scrolling past too fast.
		gap = +(drag / velocity)
		time.sleep(gap)
		# Check whether target is still alive or not.
		if target.life <= 0:
			# Print loser
			print('\n', target.name, "collapses in a pool of blood", '\n') 
			# End this round of combat immediately.
			return True		
	
	def combat(self):
		"""Initialize combat sequence
		
		Takes no arguments. Creates a list of matches, iterating through them
		until one Player is victorious. Returns False if no victory is achieved.
		"""
		print('\n', "Let the combat begin!", '\n')
		self._vel_max = self._dam_max = 23
		self._vel_min = self._dam_min = 1
		# Loop while more than one player is still alive
		players = [item for item in self.inventory 
					if issubclass(type(item), Player)]
		miss_counter = 0
		while len(players) > 1:
			# Seed random generator
			random.seed()
			random.shuffle(players)
			# create list of matches using ziply function
			matches = ziply(list(range(0,len(players))))
			trace("Matches:", matches)
			for attack, targ in matches:
				winner = self.resolve_conflict(players[attack], players[targ])
				if winner == False:
					miss_counter += 1
					if miss_counter > 6:
						print("\n", players[attack].name, "and", players[targ].name, "declare a truce.\n")
						return False
				elif winner: 
					# Remove loser from players list
					del players[targ]
					self.inventory = players
					break
				else:
					miss_counter = 0
		# Print winner
		trace("Winner:", players[0])
		print(players[0].name, "is victorious!")
		trace("""max damage | velocity
		{0} | {1}
		 {2} | {3}
		""".format(self._dam_max, self._vel_max, self._dam_min, self._vel_min))
		return
	
	def exit(self, player):
		"""Commands run when a player exits a Location
		
		Takes one argument - a Player object.
		Removes Player from Location's inventory.
		If the player in question is Dead, gives 'Game Over' message.
		Doesn't return anything either.
		"""
		if player.name in self.inventory:
			self.inventory.remove(player.name)
			print("You leave the", self.name)
		else:
			print("Game Over")
		return
		
class Shop(Location):
	"""Sub-class of Location, which allows trading.
	
	Same as Location but Shop.commands allows different game commands.
	The str() output is different to allow a price-list to be displayed.
	"""
	
	def __init__(self, name = 'Somewhere', store = {}):
		super().__init__(name, store)
		self.commands = {'look':'print({0!s})',
						'buy':'player.buy("{0}")'}
	
	def __str__(self):
		stock_list = ["    {0!s:10}{1: >3}".format(item, item.gold) 
						for item in self.inventory
						if issubclass(type(item), Thing)]
		view = """
<==|#|==\{_name!s}/==|#|==>
 {_desc!s}
	Stock List:
{0!s}
<==|#|==\@@@@/==|#|==>
 """.format('\n'.join(stock_list), **vars(self))
		return view

def trace(*text):
	"""Verbose output for trouble-shooting purposes
	
	Takes same arguments as print()
	"""
	if trace_on:
		print(" <<-::", *text)
	return

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
		phrase = phrase.replace('them','her')
		phrase = phrase.replace('their','her')
		phrase = phrase.replace('themself','herself')
	elif gender == 'male':
		phrase = phrase.replace('them','him')
		phrase = phrase.replace('their','his')
		phrase = phrase.replace('themself','himself')
	else:
		phrase = phrase.replace('them','it')
		phrase = phrase.replace('their','its')
		phrase = phrase.replace('themself','itself')
	return phrase

def write_out(players):
	"""Save Players
	
	Write Player stats out to file."""
	print("Saving character sheets")
	data_file = open('rpcharacters.rpg', 'w')
	lines = []
	for player in players:
		lines.append(repr(player) + '\n')
	data_file.writelines(lines)
	data_file.close
	return

def read_in():
	"""Open Players
	
	Read in Player stats from file."""
	print("Reading in data")
	data_file = open('rpcharacters.rpg')
	for line in data_file:
		player = eval(line)
		players.append(player)
	data_file.close()
	trace("Data:", players)
	return

##
# The main body of the program starts here,
##

if __name__ == '__main__':
	print(Boilerplate)

	# Prompt to set number of players
	reply = input('How many players?: ') or 2
	max_players = int(reply)
	
	# Set up locations
	arena = Location('Main Arena')
	arena.desc = """Welcome to Cloud Cuckoo Land,
 this is where all the action takes place. You can type 
 *look here* if you want to look around; 
 *say* stuff if you want or just type 
 *attack* if you want to fight and
 *exit* when you want to quit.
"""
	arena.inventory = []
	shop = Shop('The Emporium')
	shop.desc = """Welcome to your friendly local equipment store!
 You can *buy* something if you want or type
 *look* to see the Stock List or
 *look me* to check your stats and
 *exit* when you want to quit.
"""
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
	
	# Set up players
	read_in()
	if len(players) > max_players:
		players = players[:max_players]
	while len(players) < max_players:
		profile = Player()
		# Add new player to list of players
		players.append(profile)
	write_out(players)
	
	# Start the game 
	# by placing the players in the combat arena
	arena.inventory = players
	arena.enter(players[0])
	del reply
	
	# That's all folks!!!
