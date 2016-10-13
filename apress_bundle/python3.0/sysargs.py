#! /usr/bin/python3.0
# -*- coding: UTF8 -*-

"""Using command-line arguments

This script can receive command line arguments
and data from stdin. 
The output of any command can be fed into the script via | the pipe command.

$ echo "Foo" | ./sysargs.py bar baz
Datestamp: 
2008-11-12

Command-line arguments: 
0	./sysargs.py
1	bar
2	baz

Stdin: 
Foo
"""

import sys
import time

now = time.strftime("%Y-%m-%d")

def get_args():
	result = ['\t'.join([str(i), str(arg)]) for i, arg in enumerate(sys.argv)]	
	return result

def get_input():
	result = sys.stdin.read()
	return result

def output(args, data):
	arguments = "\n".join(args)
	output_string = '\n'.join(["Datestamp: ", now, 
					"\nCommand-line arguments: ", arguments, "\nStdin: ",data])
	sys.stdout.write(output_string)
	return

if __name__ == '__main__':
	arguments = get_args()
	data = get_input()
	output(arguments, data)
	
