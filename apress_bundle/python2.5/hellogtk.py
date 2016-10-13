#!/usr/bin/env python

"""Hellogtk: Example windowed app.

Usage: hellogtk.py
Target System: GNU/Linux
Interface: Gtk
Functional Requirements: Display a GUI window containing two buttons, 
which write a message to stout when pressed.
"""

__version__ = 0.1
__maintainer__ = "maintainer@website.com"
__status__ = "Prototype"
__date__ = "12-01-2009"

# Import modules

import gtk

class Hellogtk:

    # This is a callback. The data passed to this method is printed to stdout.
    def callback(self, widget, data):
        print "Hello again - %s was pressed" % data

    # This is another callback, which exits the application.
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        print "Bye!"
        return gtk.FALSE

    def __init__(self):
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        
        # Set the title of the window to "Graphic User Interface"
        self.window.set_title("Graphic User Interface")

        # Create a handler for delete_event that immediately quits GTK.
        self.window.connect("delete_event", self.delete_event)

        # Set the border width of the window.
        self.window.set_border_width(6)

        # Create a box to pack the widgets into. The box is an invisible 
        # container, which is used to arrange the widgets inside it.
        self.box1 = gtk.HBox(gtk.FALSE, 0)

        # Put the box into the main window.
        self.window.add(self.box1)

        # Create a new button with the label "Hello".
        self.button1 = gtk.Button("Hello")

        # Now when the button is clicked, we call the self.callback method 
        # with a pointer to "the Hello button" as its argument.
        self.button1.connect("clicked", self.callback, "the Hello button")

        # Instead of add(), we pack this button into the invisible box, 
        # which has been packed into the window.
        self.box1.pack_start(self.button1, gtk.TRUE, gtk.TRUE, 0)

        # Always remember this step, this tells GTK to actually display the 
        # button.
        self.button1.show()

        # Do these same steps again to create a second button
        self.button2 = gtk.Button("Quit")

        # This time, delete_event is called and the window exits.
        self.button2.connect("clicked", self.delete_event, "the Quit button")
        self.box1.pack_start(self.button2, gtk.TRUE, gtk.TRUE, 0)

        # The order in which the buttons are shown is not really important, 
        # but it is recommended to show the window last, so that everything 
        # displays at once.
        self.button2.show()
        self.box1.show()
        self.window.show()

def main():
    gtk.main()

if __name__ == "__main__":
    hello = Hellogtk()
    main()
