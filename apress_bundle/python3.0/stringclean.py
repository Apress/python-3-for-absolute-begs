#! /usr/bin/env python3.0

"""Clean up text string, replacing punctuation with spaces.

Target System: GNU/Linux
Interface: Command-line
Functional Requirements: 
	Loop through the characters in a string
	Removing all non-alpha-numeric characters
	Lines break at full stops
	It would be great to have a single space between each word.
Testing: Trace table 
Test values: 
(One long string)*+with various punctuation - like this / this: and a list; of < arithmetic = and comparison symbols> including, dubious? email@addresses and [Stuff \ that] might be ^ Python_code, which `evaluates` as {something|other}~ you don't want. Another sentence. Blah97635o98q6v4ib5uq. test
Expected results:  
	One long string with various punctuation like this this and a list of 
    arithmetic and comparison symbols including dubious email addresses and 
    Stuff that might be Python code which evaluates as something other you 
    don't want
	Another sentence
	Blah97635o98q6v4ib5uq
"""

__version__ = "0.1"
__maintainer__ = "maintainer@website.com"
__status__ = "Prototype"


punctuation = "#()*+,-/:;<=>? \\@^_`{|}~[]"
output_string = ' '
space_flagged = False
input_string = input("Enter a text string: ")
print()
print("***")
print()
for char in input_string:
    if char == '.':
        print(output_string)
        output_string = ' '			
    elif char not in punctuation:
        output_string += char
        space_flagged = False 
    else:
        if not space_flagged:
            output_string += ' '
            space_flagged = True 
print(output_string)
print()
print("***")
print()	
