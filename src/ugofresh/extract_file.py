#%%
import tkinter
from tkinter import filedialog
import customtkinter
import datetime
import requests
import datetime

class UgoFresh():
    def __init__(self,loc) -> None:
        self.s = requests.Session()
        self.s.get("https://app.ugo-fresh.com/accounts/login/?next=%2Fmarket%2Fmy-offers")
        self.data = {"csrfmiddlewaretoken":self.s.cookies.get_dict()['csrftoken'],"login":"dlahbib@hotmail.fr","password":"TANTAN78"}
        self.s.post("https://app.ugo-fresh.com/accounts/login/?next=%2Fmarket%2Fmy-offers",allow_redirects=True,data=self.data)
        self.date = datetime.datetime.now()
        self.loc=loc



    def str_format(self,s):
        s=str(s)
        if len(s)==1:return "0"+s
        if len(s)==4:return s[:2]
        return s


    def get_proxy(self):
        date=self.date-datetime.timedelta(days=1)  
        if date.weekday()!=6:
            file=self.s.get(f"https://app.ugo-fresh.com/api/1.6/orders/export?datetime_from={date.year}-{self.str_format(date.month)}-{self.str_format(date.day)}T08%3A00%3A00.000Z&datetime_to={date.year}-{self.str_format(date.month)}-{self.str_format(date.day)}T19%3A00%3A00.000Z&date_scope=order&state=accepted&template=carrefour.magasin.xlsx&download=true&warehouse=82cc3c95-5653-402a-a71d-6faee2a234ad&warehouse=990b15d5-c89c-47f5-9179-ab06d0c234ec&warehouse=74a0615b-3bbe-4164-a4e8-ae14dda59529&warehouse=d7cbc7ad-12fb-4669-90b5-60e13cd45805")
            open(f"carrefour.magasin.proxy {date.strftime('%d%m%y')}.xlsx","wb").write(file.content)
            file=self.s.get(f"https://app.ugo-fresh.com/api/1.6/orders/export?datetime_from={date.year}-{self.str_format(date.month)}-{self.str_format(date.day)}T08%3A00%3A00.000Z&datetime_to={date.year}-{self.str_format(date.month)}-{self.str_format(date.day)}T19%3A00%3A00.000Z&date_scope=order&state=accepted&template=carrefour.fournisseur.xlsx&download=true&warehouse=82cc3c95-5653-402a-a71d-6faee2a234ad&warehouse=990b15d5-c89c-47f5-9179-ab06d0c234ec&warehouse=74a0615b-3bbe-4164-a4e8-ae14dda59529&warehouse=d7cbc7ad-12fb-4669-90b5-60e13cd45805")
            open(f"carrefour.fournisseur.proxy {date.strftime('%d%m%y')}.xlsx","wb").write(file.content)
        else:
            print("TO DO")
    def get_hyper(self):
        date=self.date
        file=self.s.get(f"https://app.ugo-fresh.com/api/1.6/orders/export?datetime_from={date.year}-{self.str_format(date.month)}-{self.str_format(date.day)}T01%3A00%3A00.000Z&datetime_to={date.year}-{self.str_format(date.month)}-{self.str_format(date.day)}T05%3A15%3A00.000Z&date_scope=order&state=accepted&template=carrefour.magasin.xlsx&download=true&warehouse=82cc3c95-5653-402a-a71d-6faee2a234ad&warehouse=990b15d5-c89c-47f5-9179-ab06d0c234ec&warehouse=74a0615b-3bbe-4164-a4e8-ae14dda59529&warehouse=d7cbc7ad-12fb-4669-90b5-60e13cd45805")
        open(f"carrefour.magasin.hyper {date.strftime('%d%m%y')}.xlsx","wb").write(file.content)
        file=self.s.get(f"https://app.ugo-fresh.com/api/1.6/orders/export?datetime_from={date.year}-{self.str_format(date.month)}-{self.str_format(date.day)}T01%3A00%3A00.000Z&datetime_to={date.year}-{self.str_format(date.month)}-{self.str_format(date.day)}T05%3A15%3A00.000Z&date_scope=order&state=accepted&template=carrefour.fournisseur.xlsx&download=true&warehouse=82cc3c95-5653-402a-a71d-6faee2a234ad&warehouse=990b15d5-c89c-47f5-9179-ab06d0c234ec&warehouse=74a0615b-3bbe-4164-a4e8-ae14dda59529&warehouse=d7cbc7ad-12fb-4669-90b5-60e13cd45805")
        open(f"carrefour.fournisseur.hyper {date.strftime('%d%m%y')}.xlsx","wb").write(file.content)
    def get_dep(self):
        date=self.date
        file=self.s.get(f"https://app.ugo-fresh.com/api/1.6/orders/export?datetime_from={date.year}-{self.str_format(date.month)}-{self.str_format(date.day)}T05%3A15%3A00.000Z&datetime_to={date.year}-{self.str_format(date.month)}-{self.str_format(date.day)}T7%3A30%3A00.000Z&date_scope=order&state=accepted&template=carrefour.magasin.xlsx&download=true&warehouse=82cc3c95-5653-402a-a71d-6faee2a234ad&warehouse=990b15d5-c89c-47f5-9179-ab06d0c234ec&warehouse=74a0615b-3bbe-4164-a4e8-ae14dda59529&warehouse=d7cbc7ad-12fb-4669-90b5-60e13cd45805")
        open(f"carrefour.magasin.dep {date.strftime('%d%m%y')}.xlsx","wb").write(file.content)
        file=self.s.get(f"https://app.ugo-fresh.com/api/1.6/orders/export?datetime_from={date.year}-{self.str_format(date.month)}-{self.str_format(date.day)}T05%3A15%3A00.000Z&datetime_to={date.year}-{self.str_format(date.month)}-{self.str_format(date.day)}T7%3A30%3A00.000Z&date_scope=order&state=accepted&template=carrefour.fournisseur.xlsx&download=true&warehouse=82cc3c95-5653-402a-a71d-6faee2a234ad&warehouse=990b15d5-c89c-47f5-9179-ab06d0c234ec&warehouse=74a0615b-3bbe-4164-a4e8-ae14dda59529&warehouse=d7cbc7ad-12fb-4669-90b5-60e13cd45805")
        open(f"carrefour.fournisseur.dep {date.strftime('%d%m%y')}.xlsx","wb").write(file.content)




class Window(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x400")
        customtkinter.set_appearance_mode("Dark")
        self.title("UgoFresh Extractor")
        self.loc = "./"
        #######self.ugo = UgoFresh()


        self.ul = customtkinter.CTkLabel(self,text="UgoFresh Extractor",text_color="red",font=("ARIAL",20)).place(relx=0.5,rely=0.25,anchor=tkinter.CENTER)
        
        
        
        self.pb = customtkinter.CTkButton(self,text="Proxi",command=lambda:self.proxi()).place(relx=0.25,rely=0.5,anchor=tkinter.CENTER)
        self.pt = customtkinter.CTkLabel(self,text="").place(relx=0.25,rely=0.60,anchor=tkinter.CENTER)
        self.hb = customtkinter.CTkButton(self,text="Hyper",command=lambda:self.hyper()).place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)
        self.ht = customtkinter.CTkLabel(self,text="").place(relx=0.5,rely=0.60,anchor=tkinter.CENTER)
        self.db = customtkinter.CTkButton(self,text="Depannage",command=lambda:self.dep()).place(relx=0.75,rely=0.5,anchor=tkinter.CENTER)
        self.dt = customtkinter.CTkLabel(self,text="").place(relx=0.75,rely=0.60,anchor=tkinter.CENTER)

        self.cdb = self.db = customtkinter.CTkButton(self,text="Choose directory",command=lambda:self.choose_directory()).place(relx=0.5,rely=0.85,anchor=tkinter.CENTER)

    def proxi(self):
        self.winfo_children()[2].configure(text="Downloading...")
        #appel ugo
        self.winfo_children()[2].configure(text="Downloaded")
    
    def hyper(self):
        self.winfo_children()[4].configure(text="Downloading...")
        #appel ugo
        self.winfo_children()[4].configure(text="Downloaded")

    def dep(self):
        self.winfo_children()[6].configure(text="Downloading...")
        #appel ugo
        self.winfo_children()[6].configure(text="Downloaded")

    def choose_directory(self):
        self.loc = filedialog.askdirectory(initialdir="./")+"/"
App = Window()
App.mainloop()
# %%
