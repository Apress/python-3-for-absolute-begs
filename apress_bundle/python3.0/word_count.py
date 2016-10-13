#! /usr/bin/python

##
# Problem: Process a line of text to find the average length of the words it contains
# constraints: The words must be separated by spaces
##

counter = 1
total_characters = 0
text = input("Enter a line of text: ")
text_list = text.split()
print(text)
print(text_list)
for word in text_list:
	print(word)
	total_characters += len(word)
	print('\t', total_characters)
	counter +=1
	print('\t\t', counter)
average_length = total_characters / counter
print(average_length)
	