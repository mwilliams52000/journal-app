import pickle
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import ttk, Listbox, Scrollbar
from tkinter import filedialog
from tkinter import messagebox
import os
import subprocess
import sys

class JournalEntry(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        
        self.back_button = ttk.Button(self, text="<", bootstyle="light")
        self.back_button.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        
        self.date_label = ttk.Label(self, text="")
        self.date_label.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        
        self.forward_button = ttk.Button(self, text=">", bootstyle="light")
        self.forward_button.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')
        
        self.text_area = tk.Text(self, undo=True)
        self.text_area.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
        self.grid_rowconfigure(1, weight=1)
        self.text_area.bind("<KeyRelease-Return>", lambda event: self.is_prev_line_bulleted(controller))

    def constructTextArea(self, text_string, int_month, int_day, year):
        self.month = int_month
        self.year = year
        self.day = int_day
        month = self.switch_month(int_month)
        day = self.switch_day(int_day)
        self.date_label.config(text=f"{month} {day}, {year}", font=("Helvetica", 16, "bold"))
        # Insert journal content into text area
        self.text_area.insert(tk.END, text_string)
        self.text_area.edit_reset()

    def switch_month(self, value):
        switcher = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December",
        }
        return switcher.get(value, "Invalid month")
    
    def switch_day(self, value):
        if 4 <= value <= 20 or 24 <= value <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][value % 10 - 1]
        return f"{value}{suffix}"

    def saveCommand(self, controller):
        from landing_page import LandingPage
        temp_frame = controller.frames[LandingPage]
        temp_frame.checkFileExistance()
        folder_path = 'app_data'
        file_path = os.path.join(folder_path, 'data.dat')
        try:
            write_dictionary = {}
            # Open file for binary reading
            with open(file_path, 'rb') as data_file:
                app_dictionary = pickle.load(data_file)
                key = str(self.month) + '/' + str(self.day) + '/' + str(self.year)
                text_content = self.text_area.get("1.0", tk.END)
                app_dictionary[key] = text_content
                write_dictionary = app_dictionary
            # Open file for writing
            with open(file_path, 'wb') as data_file:
                pickle.dump(write_dictionary, data_file)
        except:
            return
    
    def undoCommand(self, controller):
        try:
            self.text_area.edit_undo()
        except:
            return
    
    def redoCommand(self, controller):
        try:
            self.text_area.edit_redo()
        except:
            return
    
    def deleteEntryCommand(self, controller):
        from landing_page import LandingPage
        temp_frame = controller.frames[LandingPage]
        temp_frame.checkFileExistance()
        folder_path = 'app_data'
        file_path = os.path.join(folder_path, 'data.dat')
        try:
            write_dictionary = {}
            # Open file for binary reading
            with open(file_path, 'rb') as data_file:
                app_dictionary = pickle.load(data_file)
                key = str(self.month) + '/' + str(self.day) + '/' + str(self.year)
                try:
                    del app_dictionary [key]
                except:
                    pass
                write_dictionary = app_dictionary
            # Open file for writing
            with open(file_path, 'wb') as data_file:
                pickle.dump(write_dictionary, data_file)
            self.text_area.delete("1.0", tk.END)
        except:
            return
    
    def bulletCommand(self, controller):
        current_index = self.text_area.index(tk.INSERT)
        line_start_index = "{}.0".format(current_index.split('.')[0])
        self.text_area.insert(line_start_index, u'\u2022' + ' ')

    def homeCommand(self, controller):
        # Relaunch the application
        python = sys.executable
        subprocess.Popen([python] + sys.argv)
        # Close the current application
        sys.exit()
    
    def is_prev_line_bulleted(self, controller):
        current_index = self.text_area.index(tk.INSERT)
        line_start_index = "{}.0".format(current_index.split('.')[0])
        # If the line start index is not 1.0, then this current line is not the first line
        if not(line_start_index == "1.0"):
            # Get the previous line index
            prev_line_index = "{}.0".format(int(current_index.split('.')[0]) - 1)
            # Check if the first character of the previous line is a bullet point
            if self.text_area.get(prev_line_index, f"{prev_line_index} + 1 char") == u'\u2022':
                # If it is, bullet this current line as well
                self.bulletCommand(controller)

    def constructMenuBar(self, controller):
        # Create a menu bar
        menu_bar = tk.Menu(self)
        # Save button
        menu_bar.add_command(label="💾", command=lambda: self.saveCommand(controller))
        # Undo button
        menu_bar.add_command(label="↶", command=lambda: self.undoCommand(controller))
        # Redo button
        menu_bar.add_command(label="↷", command=lambda: self.redoCommand(controller))
        # Bullet button
        menu_bar.add_command(label="•--", command=lambda: self.bulletCommand(controller))
        # Trashcan button
        menu_bar.add_command(label="🗑️", command=lambda: self.deleteEntryCommand(controller))
        # Exit button
        menu_bar.add_command(label="🏠", command=lambda: self.homeCommand(controller))
        # Assign the menu bar to the window
        self.controller.config(menu=menu_bar)