#! /usr/bin/python

"""
chargen.py
Simple Character generator
"""
app_version = 0.2

import random

shop = {'shield':25,'sword':75,'dagger':25}
players = []
while len(players) < 2:

	profile = {'Name':"", 'Desc':"", 'Gender':"", 'Race':"", 'Muscle':0,
				 'Brainz':0, 'Speed':0, 'Charm':0, 'life':0, 'magic':0,
				  'prot':0, 'gold':0, 'inventory':[]}

	# Prompt user for user-defined information
	profile['Name'] = eval(input('What is your name? '))
	profile['Desc'] = eval(input('Describe yourself: '))
	profile['Gender'] = eval(input('What Gender are you? (male / female / unsure): '))
	profile['Race'] = eval(input('What Race are you? - (Pixie / Vulcan / Gelfling / Troll): '))

	# Generate stats
	profile['Muscle'] = random.randint(3,33) + random.randint(3,33) + random.randint(3,33)
	profile['Brainz'] = random.randint(3,33) + random.randint(3,33) + random.randint(3,33)
	profile['Speed'] = random.randint(3,33) + random.randint(3,33) + random.randint(3,33)
	profile['Charm'] = random.randint(3,33) + random.randint(3,33) + random.randint(3,33)

	# Modify stats according to user-defined info

	# Work out combat stats

	profile['life'] = (profile['Muscle'] + (profile['Speed']/2) + random.randint(1,49))/2
	profile['magic'] = (profile['Brainz'] * profile['Charm']) / (random.randint(3,33) + random.randint(3,33) + random.randint(3,33))
	profile['prot'] = (profile['Speed'] + (profile['Brainz']/2) + random.randint(1,49))/2
	profile['gold'] = random.randint(1,49) + random.randint(1,49) + random.randint(1,49)
	
	# Test values

	# Output the character sheet
	fancy_line = "<~~==|#|==~~++**\@/**++~~==|#|==~~>"
	print()
	print(fancy_line)
	print(("\t", profile['Name']))
	print(("\t", profile['Race'], profile['Gender']))
	print(("\t", profile['Desc']))
	print(fancy_line)
	print()
	print(("\tMuscle: ", profile['Muscle'], "\tlife: ", profile['life'], 1 < profile['life'] < 100))
	print(("\tBrainz: ", profile['Brainz'], "\tmagic: ", profile['magic'], 1 < profile['magic'] < 100))
	print(("\tSpeed: ", profile['Speed'], "\tprotection: ", profile['prot'], 1 < profile['prot'] < 100))
	print(("\tCharm: ", profile['Charm'], "\tgold: ", profile['gold'], 1 < profile['prot'] < 150))
	print()  
	
	purchase = eval(input('Would you like to buy some equipment? '))
	while purchase != 'no':
		for item in shop:
			print((item, shop[item]))
		purchase = eval(input('Please choose one item or type no to quit. '))
		if purchase in shop:
			if shop[purchase] <= profile['gold']:
				print(("You buy a", purchase, "for",shop[purchase], "gold pieces.")) 
				profile['gold'] -= shop[purchase]
				profile['inventory'].append(purchase)
				print(("You own a", " ".join(profile['inventory'])))
				print(("You have", profile['gold'], "left."))
			elif purchase == 'no':
				break
			else:
				print("You don't have enough gold to buy that.")
		else:
			print(("We don't have", purchase, "in stock."))
	print(("You own a", " ".join(profile['inventory'])))
	players.append(profile)
print(players) 

# Combat

consent = eval(input("Are you ready for mortal combat? "))



