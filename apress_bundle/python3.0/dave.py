#! /usr/bin/env python

"""Dave the cardboard box

A simple scope example.
"""
print("dave\tfred\tpete")
dave = 0
fred = 1
pete = 2
def cardboard_box():
	dave = fred + pete
	print("Inside the box")
	print((dave, '\t', fred, '\t',  pete))
	return
cardboard_box()
print("Outside the box:")
print((dave, '\t', fred, '\t',  pete))

