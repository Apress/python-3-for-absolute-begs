#!c:\python\python.exe

"""Fixhash.py:  searches through the current directory (".") and
checks the suffix of every file; if a file is labelled as a
Python file (has a .py suffix), then the first line is checked.
If there is no #! line or if the #! doesn't match what it
should be for the system we're running on, then write access
to the file is checked.  If we can't write it, we let the
user know; otherwise, we call rewritefile(), which either
replaces an existing #! line or prepends a new one.  Existing
modes on the modified file are preserved, although the
existing owner may not be.

This is intended to run through all .py files in a cgi-bin
directory and make sure that the #! lines are correct for
the Apache webserver, which depends upon the path after the
#! being correct.  Naturally, you can use it to check any
directory you want.  Using this program makes the process 
of mirroring a website on two or three differing platforms
much easier.  For instance, my "official" webserver is
Windows NT running Apache, but I mirror the site at home
and at work on two different versions of Linux.  The Python
executable lives in three different places; using this script,
I can drop the whole directory in, run fixhash.py (by
typing 'python fixhash.py') and get the cgi-bin directory
fully corrected in moments.
"""

import os
import sys
import fileinput
from stat import *


pbang = "#!" + sys.executable
if sys.platform == "win32":
    sys.stderr.write("Python Version " + sys.version + " Running on Windows\n")
elif sys.platform == "linux2":
    sys.stderr.write("Python Version " + sys.version + " Running on Linux\n")
else: 
    sys.stderr.write("Python Version " + sys.version + " Running on " + sys.platform + "\n")

nm = os.path.split(sys.argv[0])[1]

def rewritefile(fip):
    """Input:  fip, filename; expected to live in the
    current directory.  If the first line begins with
    #!, the line is replaced.  If it doesn't, then
    the proper #! line is prepended to the file.
    Existing file modes are preserved (that's what
    the chmod() call does), but the owner of the
    original file may change to whoever is running
    this script; that may be root on a Unix system.
    """
    global pbang
    mode = os.stat(fip)[ST_MODE]
    for line in fileinput.input(fip, inplace = 1):
	if fileinput.isfirstline():
	    if line [: 2] == "#!":
		sys.stdout.write(pbang + "\n")
	    else:
		sys.stdout.write(pbang + "\n")
		sys.stdout.write(line)
	else:
	    sys.stdout.write(line)
    fileinput.close()
    os.chmod(fip, mode)

def fixdirectory(d):
    dlist = os.listdir(d)
    nfiles = 0
    for i in dlist:
        if i == nm:
	    continue
        if len(i)> 4:
            fname = d + "/" + i
	    if fname[-3:] == ".py":
	        sys.stderr.write("Checking " + fname + "...\n")
	        for line in fileinput.input(fname):
		    if fileinput.isfirstline():
		        if line[: -1] != pbang:
			    fileinput.close()
			    t = os.access(fname, os.W_OK)
			    if t == 0:
			        sys.stderr.write(fname + " is not writable; skipping.\n")
			    else:
			        sys.stderr.write("Modifying " + fname + "...\n")
			        rewritefile(fname)
			        nfiles = nfiles + 1
			    break
		        else:
			    fileinput.close()
			    break
    return nfiles

if __name__ == "__main__":
    nmod = 0
    if len(sys.argv)> 1:
		dirnames = sys.argv[1:]
    else:
		dirnames = ["."]
    for s in dirnames:
    	nmod = nmod + fixdirectory(s)

sys.stderr.write("Files modified: " + `nmod` + "\n")
