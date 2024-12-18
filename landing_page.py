import ttkbootstrap as ttk
import os
import pickle
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import DatePickerDialog
from ttkbootstrap.dialogs import Querybox
from datetime import datetime
import tkinter as tk
from tkinter import ttk, Listbox, Scrollbar
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk, Menu, font
import tkinter.font as tkFont
from journal_entry import JournalEntry

# Font for landing page title
LARGEFONT =("Verdana", 25)

class LandingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.checkFileExistance()
        # set full window automatically
        controller.state('zoomed')
        # sets min size of window
        controller.minsize(350, 200)
        # window title
        controller.title("Journal App")
        self.month, self.day, self.year = self.getCurrentDate()

        # Label of frame layout
        label = ttk.Label(self, text="Journal App", font=LARGEFONT)
        label.grid(row=0, column=0, padx=10, pady=10)
        self.date_label = ttk.Label(self, text=f"Selected Date: {self.month}/{self.day}/{self.year}")
        self.date_label.grid(row=1, column=0, padx=10, pady=10)

        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, padx=10, pady=10)
        # Button texts and commands placed in a list
        buttons = [
            ("Change Date", lambda: self.navigateDatePicker(controller)),
            ("Open Journal", lambda: self.navigateLoadEntry(controller)),
        ]
        for i, (text, command) in enumerate(buttons):
            button = ttk.Button(button_frame, text=text, command=command)
            button.pack(padx=10, pady=5)
    
    def getCurrentDate(self):
        return datetime.now().date().month, datetime.now().day, datetime.now().year

    def navigateLoadEntry(self, controller):
        textString = self.checkDate()
        if textString == False:
            textString = ''
        journal_entry_frame = controller.frames[JournalEntry]
        journal_entry_frame.constructMenuBar(controller)
        journal_entry_frame.constructTextArea(textString, self.month, self.day, self.year)
        controller.show_frame(JournalEntry)

    def navigateDatePicker(self, controller):
        date = Querybox.get_date()
        self.year = date.year
        self.month = date.month
        self.day = date.day
        self.date_label.config(text=f"Selected Date: {self.month}/{self.day}/{self.year}")
    
    def checkFileExistance(self):
        # Check for folder called app_data
        folder_path = 'app_data'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Check for 'DATA.DAT' file in path 'app_data/data.dat'
        file_path = os.path.join(folder_path, 'data.dat')
        if not os.path.exists(file_path):
            # Create a blank dictionary and put into pickle file
            app_dictionary = {}
            with open(file_path, 'wb') as file:
                pickle.dump(app_dictionary, file)
            return False
        else:
            return True

    def checkDate(self):
        folder_path = 'app_data'
        file_path = os.path.join(folder_path, 'data.dat')
        key = str(self.month) + '/' + str(self.day) + '/' + str(self.year)
        try:
            # Open file for binary reading
            with open(file_path, 'rb') as data_file:
                app_dictionary = pickle.load(data_file)
                date_tuple = app_dictionary.keys()
                if key in date_tuple:
                    return app_dictionary[key]
                else:
                    return False
        except:
            return False