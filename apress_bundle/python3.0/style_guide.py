#! /usr/bin/python3.0
# -*- coding: UTF8 -*-

"""Docstring: Short title and summary on first line followed by a new line

style_guide.py
A Docstring should be usable as a 'Usage:' message. It should contain:
A description of the script's function;
command-line syntax and parameters;
notes about the algoritm used
and a decent usage example.

The closing triple quote should be on a line by itself.
"""

# Version information goes immediately after the docstring
# with a blank line before and after.
# These variables with double leading and trailing underscores
# are 'magic' objects, which can only be used as documented.
__version__ = 0.1
__status__ = "Prototype"
__date__ = "31-10-2008"
__maintainer__ = "maintainer@website.com"
__credits__ = "Thanks to everyone."

# Import any modules we might need.
# Standard library imports
import sys
import time

# Related third party imports

# local application / library specific imports

# Globals and constants
# Set variables whose values won't change before any others.
Global = ""
_private_global = "This variable is only used inside the program"

# Class declarations would normally happen about here
# Classes are covered in the next chapter.

def code_layout():
	"""Indentation
	
	Use 4 spaces per indentation level
		Never mix tabs and spaces
			In fact, just use spaces.
	"""
	line_length = "Limit all lines to a maximum of 79 characters, for \
		big blocks of text 72 chars is recommended. You can use the \
		implied line continuation inside () [] and {} or a backslash \
		to wrap long lines of text."
	
	# Always keep comments up to date when the code changes,
	# delete old and irrelevant comments.
	# Comments should be complete grammatical statements.
	
	###
	## Stub or development note
	## to be removed before the program is released.
	## This function doesn't do anything.
	###
	
	return

def naming_conventions(functions = "lower case with underscores"):
	"""Variable naming
	
	Choose names that people might be likely to guess, whole words are
	good, but don't make it too long. Use singular names to describe
	individual things, use plurals for collections. Single letters are
	only useful for throw-away variables.
	"""
	variable_names = "lower case with underscores"
	a, b, c = 0, 1, 2
	int_variables = [a, b, c]
	x, y ,z = 0.5, 1.65, 2.42
	float_variables = [x, y, z]
	result = [i + j for i in int_variables for j in float_variables]
	if result is not None:
		return result

def main_func():
	"""Docstring: The title should make sense by itself.
	
	A function's docstring should:
	Summarize the function's behaviour;
	Document its arguments;
	Return values;
	Side-effects;
	Exceptions raised;
	and restrictions on when the function can & cannot be called.
	Optional arguments and keywords should also be explained if they are
	part of the interface.
	"""
	result = naming_conventions()
	return result

def get_args():
	print("Command-line arguments: ")
	for i, arg in enumerate(sys.argv):
		print(i, arg)
		
	return

if __name__ == '__main__':
	results = main_func()
	get_args()
	print("\nPoints awarded for style: ")
	for result in reversed(sorted(results)):
		print('\t', result)
	print()
