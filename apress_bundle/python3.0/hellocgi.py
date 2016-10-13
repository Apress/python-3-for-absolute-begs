#! /usr/bin/env python
# -*- coding: UTF8 -*-

"""Simple CGI script

"""

import time

now = strftime("%A %d %M %Y")

def print_content():
    print("Content-type: text/html")
    print()

def print_header():
    print("""<html>
	<head>
	<title>Simple CGI script</title>
	</head>
	<body>""")

def print_footer():
    print("</body></html>")

print_content()
print_header()
print("""<h1>It's {0!s}!</h1>
<p>Your server is correctly set up to run Python programs.</p>""".format(now))
print_footer()

