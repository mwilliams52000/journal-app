# Journal App
# Author: Matthew Williams

import tkinter as tk
from journal_entry import JournalEntry
from landing_page import LandingPage

class MainDriver(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)  
        container.pack(side = "top", fill = "both", expand = True) 
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}  
        for F in (LandingPage, JournalEntry):
            frame = F(container, self)
            # Store the frame in the frames array
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
        self.show_frame(LandingPage)
    
    # Display the current frame passed as a parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# Driver Code
app = MainDriver()
app.mainloop() 