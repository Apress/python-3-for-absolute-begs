#! /usr/bin/python3.0

"""
curtains.py
Problem: Calculate how much material to buy, given the size of the windows.
Target Users: My friend who wants to make some curtains
Target System: GNU/Linux
Interface: Command-line
Functional Requirements: 
	Print out the required length of fabric in metres
	Print out the total price of the fabric
	User must be able to input the measurements of the window
Testing: Simple run test 
Maintainer: maintainer@website.com
"""
app_version = 0.1

# To start with, all the measurements will be in cm
# I will assume that the roll of material is going to be 140cm
# and that the price per metre will be 5 units of currency
roll_width = 140
price_per_metre = 5

# Prompt the user to input the window measurements in cm
window_height = input('Enter the height of the window (cm): ')
window_width = input('Enter the width of the window (cm): ')

# print headers for the basic trace table
print() 
print('\twidth\theight\twidths\ttotal\tprice')

# I need to add a bit for the hems
# First I must convert the string into a number
# otherwise I will get an error if I try to perform arithmetic on a text string
curtain_width = (float(window_width) * 0.75) + 20
print('\t', curtain_width)
curtain_length = float(window_height) + 15
print('\t\t', curtain_length)

# Now I need to work out how many widths of cloth will be needed
# and figure out the total length of material for each curtain (in cm still)
widths = curtain_width / roll_width
print('\t\t\t', widths)
total_length = curtain_length * widths
print('\t\t\t\t', total_length)

# Actually I have two curtains, so I must double the amount of material
# and then divide by 100 to get the number of metres	
total_length = round((total_length * 2) / 100, 2)
print('\t\t\t\t', total_length)

# Finally I need to work out how much it will cost
price = round(total_length * price_per_metre, 2)
print('\t\t\t\t\t', price)

# And print out the result
print("You need", total_length, "metres of cloth for ", price)
