#! /usr/bin/python3.0

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
		
	def __format__(self, formatcode):
		return str(self)

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

inventory = {"box":Thing(0, 1, 0), 
			"axe":Weapon(75, 60, 50), 
			"shield":Armour(60, 50, 23)}
print("\n::Inventory::\n-------------")
for key, item in inventory.items():
	print("{0!s}:\t{1!s}\t{2!s}.".format(key, item, repr(item)))
print()
