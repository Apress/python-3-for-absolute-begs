#! /usr/bin/python

"""Hellotk: Example windowed app.

Usage: hellotk.py
Target System: GNU/Linux
Interface: tkinter
Functional Requirements: Display a GUI window containing two buttons, 
which write a message to stout when pressed.
"""

__version__ = 0.1
__maintainer__ = "maintainer@website.com"
__status__ = "Prototype"
__date__ = "12-01-2009"

# Import modules

import Tkinter

class Hellotk:

    def __init__(self, master):

        # First create a frame
        # This represents the main window of the application
        frame = Tkinter.Frame(master)
        # Everything has to be packed into place before it can be displayed.
        frame.pack()

        # Create the 'Hello' button.
        self.hello_button = Tkinter.Button(frame, text="Hello", 
        									command=self.say_hi)
        self.hello_button.pack(side=Tkinter.LEFT)
		
        # Create the 'Quit' button.
        self.quit_button = Tkinter.Button(frame, text="QUIT", fg="red", 
        									command=frame.quit)
        self.quit_button.pack(side=Tkinter.LEFT)

    def say_hi(self):
        print "hi there, everyone!"

root = Tkinter.Tk()
app = Hellotk(root)
root.mainloop()
