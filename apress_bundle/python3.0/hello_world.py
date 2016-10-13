#! /usr/bin/python

"""
Problem: Get the computer to output a message.
Target Users: Me
Target System: GNU/Linux
Interface: Command-line
Functional Requirements: Print out a message.
			User must be able to input some text.
Testing: Simple run test - expecting a message to appear.
			 - expecting: message == input text
Maintainer: maintainer@website.com
"""

# 1. Print out a friendly message
print("Hello World!")

# 2. Input some text
some_text = eval(input('Type in some words: '))

# 3. Print out the text we just entered
print(some_text)
