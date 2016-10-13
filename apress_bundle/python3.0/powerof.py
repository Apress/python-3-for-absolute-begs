#! /usr/bin/python

###
# Power of calculator
###

for loop_controller in range(1, 8):
	print((2 ** loop_controller))
	
loop_controller = 1
while loop_controller < 8:
	print((2 ** loop_controller))
	loop_controller += 1
	
text = eval(input("Type in some words: "))
for character in text:
	print(character)
	
sequence = ['Just','a','list','of','words']
for word in sequence:
	print(word)
	
var = 'longword'
var == 'Something else'
'black' = 'white'
