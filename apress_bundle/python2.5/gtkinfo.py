#! /usr/bin/python

"""Example windowed app.

Usage: gtkinfo.py
Target System: GNU/Linux
Interface: Gtk
Functional Requirements: Display some system information in a window.
"""

__version__ = 0.1
__maintainer__ = "maintainer@website.com"
__status__ = "Prototype"
__date__ = "12-01-2009"

# Import modules

import gtk
import pango
import os, commands

class GtkInfo:
    
    Kernel_func = '''uname -a'''
    Sound_Modules_func = '''lsmod | grep ^snd
    lsmod | egrep -q '(^usb-midi|^audio)'
    if [ $? -eq 0 ]; then
        echo "Warning: either 'audio' or 'usb-midi' OSS modules are loaded"
        echo "this may interfere with ALSA's snd-usb-audio."
        if [ ! -f /etc/hotplug/blacklist ]; then
            echo "You should create a file '/etc/hotplug/blacklist' with"
        echo "both names on it to avoid hotplug loading them."
        else
        egrep -q '(^usb-midi|^audio)' /etc/hotplug/blacklist
        if [ $? -eq 1 ]; then
            echo "You should add both modules to '/etc/hotplug/blacklist'"
            echo "to avoid hotplug loading them."
        fi
        fi
    fi
    echo'''
    Modprobe_func = '''if [ -f /etc/modprobe.conf ] ; then
        egrep '(sound|snd)' /etc/modprobe.conf
    elif [ -f /etc/modules.conf ] ; then
        egrep '(sound|snd)' /etc/modules.conf
    else
        echo "Warning: module config file does not exist"
        echo "This means any kernel modules will not be auto loaded"
        echo "See your linux distro docs on how to create this file"
    fi'''
    Asound_func = '''if [ ! -d /proc/asound ] ; then
        echo "Warning: /proc/asound does not exist"
        echo "This indicates that ALSA is not installed correctly"
        echo "Check various logs in /var/log for a clue as to why"
    else
        cat /proc/asound/{version,cards,devices,hwdep,pcm,seq/clients}
    fi'''
    Sound_Devices_func = '''if [ ! -d /dev/snd ] ; then
        echo "Warning: /dev/snd does not exist"
    else
        /bin/ls -C /dev/snd
    fi'''
    CPU_func = '''grep -e "model name" -e "cpu MHz" /proc/cpuinfo'''
    RAM_func = '''grep -e MemTotal -e SwapTotal /proc/meminfo'''
    Hardware_func = '''lspci | egrep "(Multimedia|Host bridge)"'''

    def __init__(self):
        self.boilerplate = """Multimedia Configuration Browser

a simple diagnostic tool to help with audio configuration.

Version: %s (alpha)
%s 2009""" % (__version__, __maintainer__)
        
        # Create Icons
        image = gtk.gdk.pixbuf_new_from_file
        path = '/home/tim/Projects/multimediainfo/pixmaps/'
        self.Kernel_image = image(path + 'Kernel.png')
        self.CPU_image = image(path + 'Hardware.png')
        self.RAM_image = image(path + 'Hardware.png')
        self.Sound_Modules_image = image(path + 'Sound.png')
        self.Sound_Devices_image = image(path + 'Sound.png')
        self.Asound_image = image(path + 'Alsa.png')
        self.Alsa_image = image(path + 'Alsa.png')
        self.Mixer_image = image(path + 'Mixer.png')
        self.JACK_image = image(path + 'Qjackctl.png')
        self.icon = image(path + 'mm_info.png')
        self.save_image = image(path + 'Save_As.png')
        
        # Create clipboard
        self.clipboard = gtk.Clipboard()
        
        # Create textBuffer
        self.textbuffer = gtk.TextBuffer(None)
        self.headline = self.textbuffer.create_tag('headline', 
        								weight=700, scale=pango.SCALE_LARGE)
        place = self.textbuffer.get_start_iter()
        self.textbuffer.insert_pixbuf(place, self.icon)   
        self.textbuffer.insert_at_cursor(self.boilerplate)
        iter0 = self.textbuffer.get_iter_at_line(0)
        iter1 = self.textbuffer.get_iter_at_line(1)
        self.textbuffer.apply_tag(self.headline,iter0,iter1)
        
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Gtk Info")
        self.window.set_border_width(6)
        self.window.set_default_size(600, 400)
        self.window.set_resizable(True)
        self.window.connect("delete_event", self.delete_event)
        
        # Create a vertical box to pack the widgets into.
        self.vbox1 = gtk.VBox(False, 0)
        self.window.add(self.vbox1)
        
        #Create menubar
        self.menubar1 = gtk.MenuBar()
        self.menubar1.set_pack_direction(gtk.PACK_DIRECTION_LTR)
        self.menubar1.set_child_pack_direction(gtk.PACK_DIRECTION_LTR)
        
        # FILE menu
        self.file = gtk.MenuItem(label="_File", use_underline=True)
        self.file_menu = gtk.Menu()
        
        self.save_as = gtk.ImageMenuItem(stock_id="gtk-save")
        self.save_as.connect("activate", self.on_save_as)
        self.file_menu.append(self.save_as)
        self.save_as.show()
        
        self.quit = gtk.ImageMenuItem(stock_id="gtk-quit")
        self.quit.connect("activate", self.on_quit)
        self.file_menu.append(self.quit)
        self.quit.show()
        
        self.file.set_submenu(self.file_menu)
        self.file_menu.show()
        
        # EDIT menu
        self.edit = gtk.MenuItem(label="_Edit", use_underline=True)
        self.edit_menu = gtk.Menu()
        
        self.copy = gtk.ImageMenuItem(stock_id="gtk-copy")
        self.copy.connect("activate", self.on_copy)
        self.edit_menu.append(self.copy)
        self.copy.show()
        
        self.edit.set_submenu(self.edit_menu)
        self.edit_menu.show()
        
        # HELP menu
        self.help = gtk.MenuItem(label="_Help", use_underline=True)
        self.help_menu = gtk.Menu()
        
        self.about = gtk.ImageMenuItem(stock_id="gtk-about")
        self.about.connect("activate", self.on_about)
        self.help_menu.append(self.about)
        self.about.show()
        
        self.hhelp = gtk.ImageMenuItem(stock_id="gtk-help")
        self.hhelp.connect("activate", self.on_help)
        self.help_menu.append(self.hhelp)
        self.hhelp.show()
        
        self.help.set_submenu(self.help_menu)
        self.help_menu.show()
        
        # Don't forget to add them to the menubar.
        self.menubar1.append(self.file)
        self.file.show()
        self.menubar1.append(self.edit)
        self.edit.show()
        self.menubar1.append(self.help)
        self.help.show()
        
        # Then pack the menubar into place.
        self.vbox1.pack_start(self.menubar1, False, True, 0)
        self.menubar1.show()
        
        # Create the main panels
        self.hbox1 = gtk.HBox(False, 0)
        
        # Create option list panel
        self.scrolledwindow1 = gtk.ScrolledWindow()
        self.scrolledwindow1.set_policy(gtk.POLICY_AUTOMATIC, 
                                        gtk.POLICY_AUTOMATIC)
        self.treeview1 = gtk.TreeView()
        self.treeview1.connect("cursor-changed", 
                                self.on_treeview1_cursor_changed)
        self.scrolledwindow1.add_with_viewport(self.treeview1)
        self.treeview1.show()
        self.scrolledwindow1.show()
        self.hbox1.pack_start(self.scrolledwindow1, True, True, 0)
        
        # Fill it with relevant info
        self.create_treelist()
        
        #Create text output panel
        self.scrolledwindow2 = gtk.ScrolledWindow()
        self.scrolledwindow2.set_policy(gtk.POLICY_AUTOMATIC, 
                                        gtk.POLICY_AUTOMATIC)
        self.textview1 = gtk.TextView(self.textbuffer)
        self.textview1.set_wrap_mode(gtk.WRAP_WORD)
        self.textview1.set_editable(False)
        self.textview1.set_left_margin(6)
        self.textview1.set_right_margin(6)
        self.scrolledwindow2.add_with_viewport(self.textview1)
        self.textview1.show()
        self.scrolledwindow2.show()
        self.hbox1.pack_start(self.scrolledwindow2, True, True, 0)
        self.hbox1.show()
        
        self.vbox1.pack_start(self.hbox1, True, True, 0)
        
        # Create QUIT button
        self.button2 = gtk.Button("Quit")
        self.button2.connect("clicked", self.delete_event, "the Quit button")
        self.vbox1.pack_start(self.button2, False, False, 0)
        self.button2.show()
        self.vbox1.show()
        self.window.show()

    def create_treelist(self):
        """create_treelist
        
        Create list of options
        """ 
        # Add some messages to the window
        self.liststore = gtk.ListStore(str,str,'gboolean')
        # we'll add some data now
        self.liststore.append(['Kernel', gtk.STOCK_OPEN, True])
        self.liststore.append(['CPU', gtk.STOCK_OPEN, True])
        self.liststore.append(['RAM', gtk.STOCK_OPEN, True])
        self.liststore.append(['Sound Modules', gtk.STOCK_OPEN, True])
        self.liststore.append(['Sound Devices', gtk.STOCK_OPEN, True])
        self.liststore.append(['Asound', gtk.STOCK_OPEN, True])
        
        # create the TreeViewColumn to display the data
        self.tvcolumn = gtk.TreeViewColumn('Categories')
        
        # Append liststore model to treeview
        self.treeview1.set_model(model=self.liststore)   
        
        # add tvcolumn to treeview
        self.treeview1.append_column(self.tvcolumn)
        
        # create a CellRendererText to render the data
        self.cell = gtk.CellRendererText()
        self.cell0 = gtk.CellRendererPixbuf()
        
        # add the cell to the tvcolumn and allow it to expand
        self.tvcolumn.pack_start(self.cell0, True)
        self.tvcolumn.pack_start(self.cell, True)
        
        # set the cell "text" attribute to column 0 - retrieve text
        # from that column in treestore
        self.tvcolumn.set_cell_data_func(self.cell0, self.make_pixbuf)
        self.tvcolumn.add_attribute(self.cell, 'text', 0)
        return

    def make_pixbuf(self, tvcolumn, cell, model, iter):
        """make_pixbuf
        
        Create icons for TreeView menu.
        """
        category = model.get_value(iter, 0)
        if category == 'Kernel': stock = self.Kernel_image
        elif category == 'CPU': stock = self.CPU_image
        elif category == 'RAM': stock = self.RAM_image
        elif category == 'Sound Modules': stock = self.Sound_Modules_image
        elif category == 'Sound Devices': stock = self.Sound_Devices_image
        elif category == 'Asound': stock = self.Asound_image
        else: stock = 'gtk-stop'
        cell.set_property('pixbuf', stock)
        return

    def get_selection(self):
        """get_selection
        
        Creates text appropriate to choices
        """
        # get selection from listview
        self.choice = self.treeview1.get_selection()
        self.choice.set_mode(gtk.SELECTION_SINGLE)
        self.model, self.row_reference = self.choice.get_selected()
        self.choice = self.liststore.get_value(self.row_reference, 0)
        
        # Create command line
        command_ref = "self." + self.choice.replace(' ','_') + "_func"
        command = eval(command_ref)
        
        # GUI output
        # Make clean textbuffer
        self.textbuffer = gtk.TextBuffer(None)
        # Create headline style
        self.headline = self.textbuffer.create_tag('headline', 
                            weight=700, scale=pango.SCALE_LARGE)
        # navigate to start of buffer
        place = self.textbuffer.get_start_iter()
        # Create pixbuf icon reference
        icon = eval("self." + self.choice.replace(' ','_') + "_image")
        # Insert icon at top of page
        self.textbuffer.insert_pixbuf(place, icon)
        # Print appropriate text underneath
        text = " " + self.choice + ": \n\n" + commands.getoutput(command)
        self.textbuffer.insert_at_cursor(text)
        iter0 = self.textbuffer.get_iter_at_line(0)
        iter1 = self.textbuffer.get_iter_at_line(1)
        self.textbuffer.apply_tag(self.headline,iter0,iter1)
        self.textview1.set_buffer(self.textbuffer)
        return

    def on_save_as(self, widget):
        """Save
        
        Opens a dialog asking you where you want to save the information
        as a plain text file.
        """
        print "Exporting aadebug information"
        # Create save As dialog & specify file to open for writing
        dialog = gtk.FileChooserDialog(title='Save Multimedia Info to file',
                                    action=gtk.FILE_CHOOSER_ACTION_SAVE, 
                                    buttons=(gtk.STOCK_CANCEL,
                                        gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN,
                                        gtk.RESPONSE_OK))
        dialog.set_current_name('aadebug.txt')
        response = dialog.run()
        outfile_name = dialog.get_filename()
        print "response: " + str(response)
        print "outfile: " + str(outfile_name)
        
        if response == gtk.RESPONSE_OK:
            # Write out items
            a_out = """Multimedia System Information (%s)

""" % (__version__,)
            headings = ['Kernel','CPU','RAM','Hardware','Modprobe',
                        'Sound_Modules','Sound_Devices','Asound']
            a_list = [a_out]
            for heading in headings:
                command = eval("self." + heading + "_func")
                a_ = """***** %s *****
%s

""" % (heading, commands.getoutput(command))
                a_list.append(a_)
            a_out = ''.join(a_list)
            # write out System info to file
            output_file = open(outfile_name,'w')
            output_file.write(a_out)
            output_file.close()
            print "aadebug info written out"
            
            # Create GUI output
            # Make clean textbuffer
            self.textbuffer = gtk.TextBuffer(None)
            # Create headline style
            self.headline = self.textbuffer.create_tag('headline', 
                                weight=700, scale=pango.SCALE_LARGE)
            # navigate to start of buffer
            place = self.textbuffer.get_start_iter()
            # Create pixbuf icon reference
            icon = eval("self.save_image")
            # Insert icon at top of page
            self.textbuffer.insert_pixbuf(place, icon)
            # Print appropriate text underneath
            text = """Saving Information ... 

To file: 
%s""" % (outfile_name,)
            self.textbuffer.insert_at_cursor(text)
            iter0 = self.textbuffer.get_iter_at_line(0)
            iter1 = self.textbuffer.get_iter_at_line(1)
            self.textbuffer.apply_tag(self.headline,iter0,iter1)
            self.textview1.set_buffer(self.textbuffer)
        elif response == gtk.RESPONSE_CANCEL:
            print "Save As cancelled"
        dialog.destroy()
        return

    def on_quit(self, widget):
        """Quit the application"""
        self.delete_event("Quit", "Quit")
        return

    def on_copy(self, widget):
        """Copy
        
        Copies selected information to the clipboard
        """
        self.textbuffer.copy_clipboard(self.clipboard)
        return
    
    def on_about(self, widget, *args):
        """About Dialog
        
        What it says on the box
        """
        print "About Gtk Info"
        logo = self.icon
        dialog = gtk.AboutDialog()
        dialog.set_name('Gtk Info')
        dialog.set_version(str(__version__))
        dialog.set_authors([__maintainer__])
        dialog.set_documenters([__maintainer__])
        dialog.set_logo(logo)
        comment = 'A graphical interface for displaying system information'
        dialog.set_comments(comment)
        response = dialog.run()
        if response == -6:
            dialog.destroy()
        return

    def on_help(self, widget, *args):
        """Help
        
        Not Implemented in this version
        """
        print "Opening Help file"
        return

    def on_treeview1_cursor_changed(self, widget, *args):
        """Option panel
        
        Gets the icon that received the click
        and displays relevant information
        """
        self.get_selection()

    def delete_event(self, widget, event, data=None):
        """Quits the application"""
        gtk.main_quit()
        print "Bye!"
        return False

def main():
    gtk.main()

if __name__ == "__main__":
    application = GtkInfo()
    main()
