import py_cui
import os
import sys
import subprocess
interfaces = []
selected_interface = ""
selected_interface_monitor = ""
class aircrackngTUI:

    def get_Interfaces(self):
        global interfaces
        command_interface = "iw dev | awk '$1==\"Interface\" {print $2}'"
        output_interface = os.popen(command_interface).read()
        repeat = False
        for x in range(len(interfaces)):
            if (str(output_interface) == str(interfaces[x])):
                repeat = True
        if (repeat ==  False):
            interfaces.append(output_interface)
            self.interface_list.add_item(output_interface)
        else:
            self.master.show_error_popup('ALERT', 'No New Interfaces')


        
    def put_in_mon(self):
        in_prog = self.interface_list.get()
        if in_prog is None:
            self.master.show_error_popup('No Item', 'There is no item in the list to mark as in progress')
            return
        global selected_interface
        global selected_interface_monitor
        if (in_prog != selected_interface):
            self.airmon_menu.clear()
            selected_interface = in_prog
            if (selected_interface[(len(selected_interface)-3):]=="mon"):
                selected_interface_monitor = selected_interface
            else:
                selected_interface_monitor = selected_interface+"mon"
            self.airmon_menu.add_item(str("Selected Interface: "+in_prog))
            self.airmon_menu.add_item("Airmon check interferance")
            self.airmon_menu.add_item("Airmon kill  interferance")
            self.airmon_menu.add_item("Airmon start interferance")
            self.airmon_menu.add_item("Airmon stop  interferance")
            self.airmon_menu.add_item("Airodump start listing APs")
            self.airmon_menu.add_item("Airodump stop listing APs")
        else:
            self.master.show_message_popup('ERROR', 'This interface is already selected') 

    def airmon_menu_manager(self):
        done = self.airmon_menu.get()
        if done is None:
            self.master.show_error_popup('FALIED OPERATION', 'An error has occured, please try again')
            return
        if (done[:12] == "Airmon check"):
            self.airmon_CHECK()
        if (done[:12] == "Airmon start"):
            self.master.show_yes_no_popup('Do you want to start monitor mode for '+selected_interface, self.airmon_START)
        if (done[:11] == "Airmon stop"):
            self.master.show_yes_no_popup('Do you want to stop monitor mode for '+selected_interface, self.airmon_STOP)
        elif (done[:11] == "Airmon kill"):
            self.master.show_yes_no_popup('Do you want to kill interfering processes?', self.airmon_KILL)

    def airmon_CHECK(self):
        try:
            command = "airmon-ng check"
            output = os.popen(command).read()
            self.master.show_message_popup("Checking interfering processes", str(output))
        except:
            self.master.show_error_popup('FALIED OPERATION', 'An error has occured, please try again')

    def airmon_START(self, to_start):
        if to_start:
            command = "airmon-ng start "+selected_interface_monitor
            output = os.popen(command).read()
            self.master.show_message_popup("Starting monitor mode", str(output))
            self.list_APs()
        else:
            self.master.show_error_popup('FALIED OPERATION', 'An error has occured, please try again')

    def airmon_STOP(self, to_stop):
        if to_stop:
            command = "airmon-ng stop "+selected_interface_monitor
            output = os.popen(command).read()
            self.master.show_message_popup("Stopping monitor mode", str(output))
        else:
            self.master.show_error_popup('FALIED OPERATION', 'An error has occured, please try again')

    def airmon_KILL(self, to_kill):
        if to_kill:
            command = "airmon-ng check kill"
            output = os.popen(command).read()
            self.master.show_message_popup("Killing interfering processes", str(output))
        else:
            self.master.show_error_popup('FALIED OPERATION', 'An error has occured, please try again')

    def list_APs(self):
        command = "airodump-ng "+selected_interface_monitor
        output = os.popen(command).read()
        self.airodump_display.add_item(output)


    def __init__(self, master):

        self.master = master
        
        # The scrolled list cells that will contain our tasks in each of the three categories
        self.interface_list =         self.master.add_scroll_menu('Interfaces',   0, 0, row_span=2, column_span=1)
        self.airmon_menu =  self.master.add_scroll_menu('Airmon Menu',  0, 1, row_span=3, column_span=2)
        self.airodump_display =         self.master.add_scroll_menu('Access Points',         3, 0, row_span=4, column_span=3)

        # Textbox for entering new items
        self.List_Interfaces = self.master.add_button('List Interfaces', 2, 0, command=self.get_Interfaces)

        # Keybindings for controlling our CUI.
        # We bind the enter key for each of the widgets
        self.interface_list.add_key_command(          py_cui.keys.KEY_ENTER, self.put_in_mon)
        self.airmon_menu.add_key_command(   py_cui.keys.KEY_ENTER, self.airmon_menu_manager)

        ## Color Rules
        self.airmon_menu.add_text_color_rule('Selected Interface: ', py_cui.GREEN_ON_BLACK, "startswith")
        self.airmon_menu.add_text_color_rule('Airmon', py_cui.BLUE_ON_BLACK, "startswith")
        self.airmon_menu.add_text_color_rule('Airodump', py_cui.CYAN_ON_BLACK, "startswith")
        self.interface_list.set_color(py_cui.RED_ON_BLACK)
        self.interface_list.set_border_color(py_cui.WHITE_ON_BLACK)
        self.List_Interfaces.set_color(py_cui.RED_ON_BLACK)
        self.List_Interfaces.set_border_color(py_cui.WHITE_ON_BLACK)
# Create the CUI with 7 rows 6 columns, pass it to the wrapper object, and start it
root = py_cui.PyCUI(7, 7)
root.set_title('Aircrack-ng TUI')
s = aircrackngTUI(root)
root.start()