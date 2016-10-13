#! /usr/bin/python

##
# Problem: calculate the average from an unspecified number 
# of positive user-input numerical values
##

counter = 1
total = 0
number = 0
while number > -1:
	number = float(eval(input("Enter a positive number\nor a negative to exit: ")))
	total += number
	counter += 1
average = total / counter
print(average)
	
 