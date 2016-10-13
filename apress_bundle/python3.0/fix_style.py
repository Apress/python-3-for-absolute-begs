#! /usr/bin/env python3.0
# -*- coding: UTF8 -*-

"""
fix_style.py
Purpose:	
	Python script style & version checker
Target System:  
	GNU/Linux
Interface:  	
	Command-line
Functional Requirements: 
	Automatically go through all lines in a Python file
	pulling out TODO comments and appending TODO file
	check & update AUTHORS file
	check for existence of README, [NEWS and ChangeLog]
	So all documentation can be auto-created from main python files.
	Print warnings and prompt before any changes are made.	
"""
__version__ = 0.1
__status__ = "Prototype"
__date__ = "16-10-2008"
__maintainer__ = "maintainer@website.com"
__credits__ = "Inspired by Duncan Parkes' remark about inline TODO comments."

import re
import time

# Datestamp
Now = time.strftime("%d-%m-%Y")

# Set up some regular expressons for later use
# Putting them all in one place makes editing and troubleshooting much easier.
filename_format = re.compile(".+?\.py")
version_format = re.compile("[\"']?(?:[0-9]+?\.)?[0-9]+?\.[0-9]+?[\"']?")
status_format = re.compile("[\"'](Prototype|Alpha|Beta|RC|Stable)[\"']")
date_format = re.compile("[\"'][0-3][0-9]-[01][0-9]-[0-9]{4}[\"']")
email_format = re.compile("[\"'].+?@.+\..+?[\"']")
todo_format = re.compile("^\s*?#\s*?(TODO|todo|FIXME|fixme):?\s*?(.+)")

# Dictionary to hold namespace variables of file
spellbook = {'version':0.0,
			'status':"",
			'date':"33-13-2023",
			'maintainer':"",
			'author':"",
			'credits':""}

def get_file():
	filename = input('Python script to be checked:-> ')
	if filename_format.match(filename):
		print("Looks like a Python file. [OK]")
	else:
		print("This file does not have a .py extension.")
		filename = ''
	return filename

def format_info(app):
	author_s = """
	Author: {0!s}
	Maintainer: {1!s}
	Credits: {2!s}
	""".format(app['author'], app['maintainer'], app['credits'])
	app_s = """
	File: {0!s}
	Version: {1!s} - {2!s}
	Last Modified: {3!s}
	""".format(app['file'], app['version'], app['status'], app['date'])
	out_str = """
#===(*)===# Application Details #===(*)===#
{0}
#===(*)===# AUTHORS #===(*)===#
{1}
#===(*)===#===(*)===#===(*)===#
	""".format(app_s, author_s)
	return out_str

###
# Main
###

# Input: get Python filename from user.
filename = ''
while not filename:
	filename = get_file()
# Store filename in spellbook.
spellbook['file'] = filename
# Open the file for reading.
script = open(filename)

# TODO: Test if file is valid python3.0; if not, run 2to3 on file.

print("\n#===(*)===# TODO #===(*)===#\n")
# Iterate through lines in script.
for line_no, line in enumerate(script):
	# Check that the script calls the correct version of the interpreter.
	if line_no == 0 and line != "#! /usr/bin/env python3.0\n":
		print("Warning: wrong interpreter invoked")
	# Check that the script declares Unicode encoding.
	if line_no == 1 and line != "# -*- coding: UTF8 -*-\n":
		print("Warning: no text encoding declaration")
	
	# Next should be a docstring
	# TODO: Turn comments into proper docstring.
	
	# Check for magic variables.
	if line.startswith('__'):
		label, value = line.split(' = ')
		# store magic variables in spellbook
		spellbook[label.strip('__')] = value.strip().strip('"')
		# Check magic vars are correctly formatted if present.
		# __version__ = "(?:[0-9]+?\.)[0-9]+?\.[0-9]+?"
		if label == '__version__' and not version_format.match(value):
			print("Warning: dodgy", label)
		# __status__ = "Prototype|Alpha|Beta|Release Candidate|Stable"
		if label == '__status__' and not status_format.match(value):
			print("Warning: dodgy", label)
		# __date__ = "[0-3][0-9]-[01][0-9]-[0-9]{4}"
		if label == '__date__' and not date_format.match(value):
			print("Warning: dodgy", label)
		# __maintainer__ = "\W+?@\W+\.\W+?"
		if label == '__maintainer__' and not email_format.match(value):
			print("Warning: dodgy", label)

	# Check rest of lines for "#\s*?TODO|todo|FIXME|fixme(.*)"
	# This should be a 'try' statement
	# ... but they aren't covered until Chapter 11.
	if todo_format.match(line):
		task = todo_format.match(line)
		label, desc = task.groups(1)
		todo_text = """
{4!s} {2!s}: {0!s} line {1!s}
    *** {3} ***
		""".format(filename, line_no, label, desc, Now)
		print(todo_text)

# We won't be needing this anymore.
script.close()

# Fill in some empty variables.
if not date_format.match(spellbook['date']):
	spellbook['date'] = Now
if spellbook['author'] == '':
	spellbook['author'] = spellbook['maintainer']

# Print out results.
print(format_info(spellbook))

# TODO: Check for existence of AUTHORS, ChangeLog, NEWS, README and TODO files in the same directory as file.
# TODO: if no AUTHORS file, write out author_s to AUTHORS.
# TODO: Check TODOs and Warnings: If fixed append Changelog, else append TODO.
