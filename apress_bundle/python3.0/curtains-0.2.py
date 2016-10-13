#! /usr/bin/python3.0

"""
Calculate how much material to buy, given the size of the windows.

Target Users: My friend who wants to make some curtains
Target System: GNU/Linux
Interface: Command-line
Functional Requirements: 
	Print out the required length of fabric in metres
	Print out the total price of the fabric
	User must be able to input the measurements of the window
Testing: Trace table 
Test values:  100x100, 100x200, 200x100, 200x200, 200x300 and 300x200
Expected results: 1.9, 3.4, 4.3, 6.45, 9.8, 9.45
"""
__version__ = 0.2
__maintainer__ = "maintainer@website.com"
__status__ = "Prototype"

# To start with, all the measurements will be in cm
# I will assume that the roll of material is going to be 140cm
# and that the price per metre will be 5 units of currency
roll_width = 140
price_per_metre = 5

# Prompt the user to input the window measurements in cm
window_height = input('Enter the height of the window (cm): ')
window_width = input('Enter the width of the window (cm): ')

# print headers for the rather basic trace table
print() 
print('\twidth\theight\twidths\ttotal\tprice\tshorter?\twider?')

# I need to add a bit for the hems
# First I must convert the string into a number  
# otherwise I will get an error if I try to perform arithmetic on a 
# text string
curtain_width = (float(window_width) * 0.75) + 20
print('\t', curtain_width)
curtain_length = float(window_height) + 15
print('\t\t', curtain_length)

# Now I need to work out how many widths of cloth will be needed
# and figure out the total length of material for each curtain (in cm still)
# If the length of the curtains is less than the roll_width, I can turn the
# whole thing on its side and just use one width of fabric, but if the curtains
# need to be both longer and wider than the roll_width, then I have a further
# problem - if the extra material required is less than half the roll_width I
# would need to buy an additional width of material at the same length; if it 
# is more than half, then I would need to buy two additional widths.
print('\t\t\t\t\t\t', curtain_length < roll_width)
print('\t\t\t\t\t\t\t', curtain_width > roll_width) 
if curtain_length < roll_width:
	total_length = round((curtain_width * 2) / 100, 2)
	print('\t\t\t\t', total_length)
elif curtain_width > roll_width:
	widths = int(curtain_width/roll_width)
	extra_material = curtain_width%roll_width
	if extra_material < (roll_width / 2):
		widths +=1
	if extra_material > (roll_width / 2):
		widths +=2
	print('\t\t\t', widths)
	total_length = round((curtain_length * widths) / 100, 2)
	print('\t\t\t\t', total_length)
else:
	total_length = round((curtain_length * 2) / 100, 2)
	print('\t\t\t\t', total_length)

print('\t\t\t\t', total_length)

# Finally I need to work out how much it will cost
# Rounded to two decimal places using the built-in round() function
price = round(total_length * price_per_metre, 2)
print('\t\t\t\t\t', price)

# And print out the result
print("You need", total_length, "metres of cloth, costing: ", price)
