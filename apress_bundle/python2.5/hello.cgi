#! /usr/bin/env python
# -*- coding: UTF8 -*-

"""Simple CGI script

"""

import cgitb
import time

cgitb.enable()
now = time.strftime("%A %d %B %Y")

def print_content():
    print "Content-type: text/html" 
    print 

def print_header():
    print """<html>
	<head>
	<title>Simple CGI script</title>
	</head>
	<body>""" 

def print_footer():
    print "</body></html>" 

print_content()
print_header()
print """<h1>It's %s!</h1>
<p>Your server is correctly set up to run Python programs.</p>""" % (now) 
print_footer()