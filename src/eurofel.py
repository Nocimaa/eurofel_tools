import tkinter
import customtkinter
import main
import numpy as np



#Main Windows
window = customtkinter.CTk()
window.title("Eurofel Facility")
window.geometry("800x400")


#global var
excel=None
global excel_text
excel_text = customtkinter.CTkLabel(master=window, text="")
excel_text.place(relx=0.1, rely=0.25, anchor=tkinter.CENTER)
def setup_excel():
    excel = main.load_excel()
    s = "\n".join(["\t".join([str(ell) for ell in el])     for el in excel])
    excel_text.configure("feured")


#Load Excel Buttons
load_excel = customtkinter.CTkButton(master=window, text="Load Excel",command=setup_excel)
load_excel.place(anchor="nw",relx=0.05,rely=0.1)






window.mainloop()






