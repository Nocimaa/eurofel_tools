
import tkinter
from typing import Optional, Tuple, Union
import customtkinter
from tkcalendar import DateEntry
import datetime

class Window(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x400")
        customtkinter.set_appearance_mode("Dark")
        self.title("UgoFresh Extract")
        k=datetime.datetime.now()
        customtkinter.CTkEntry(self,placeholder_text=f"{k.day}/{k.month}/{k.year}").place(relx=0.5,rely=0.4,anchor=tkinter.CENTER)

        self.f1 = customtkinter.CTkFrame(self)
        self.b1=customtkinter.CT

        


App = Window()
App.mainloop()